from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone

from apps.platform.accounts import otp
from apps.platform.accounts.models import CodigoOTP, RegistroPendiente, Role, User
from apps.platform.accounts.usecases.crear_usuario import (
    CrearUsuario,
    CrearUsuarioInput,
)
from apps.recruitment.postulantes.models import PostulanteProfile
from apps.recruitment.postulantes.normalizers import normalizar_celular, normalizar_ci
from core.exceptions import DomainError

ERRORES_CODIGO = {
    otp.SIN_CODIGO: "No hay un código activo. Solicita uno nuevo.",
    otp.VENCIDO: "El código venció. Solicita uno nuevo.",
    otp.DEMASIADOS_INTENTOS: "Demasiados intentos. Solicita un nuevo código.",
    otp.INVALIDO: "Código incorrecto. Intenta nuevamente.",
}


def _validar_disponibilidad(*, ci: str, email: str, celular: str) -> None:
    """Comprueba que CI, email y celular no pertenezcan a un usuario real."""
    if PostulanteProfile.objects.filter(ci=ci).exists():
        raise DomainError(
            "Ya existe un postulante con esa CI. "
            "Si crees que es un error, contacta a GADOR.",
            code="CI_TAKEN",
        )
    if User.objects.filter(email__iexact=email).exists():
        raise DomainError(
            "Ya existe una cuenta con ese correo. "
            "Si crees que es un error, contacta a GADOR.",
            code="EMAIL_TAKEN",
        )
    if User.objects.filter(celular=celular).exists():
        raise DomainError(
            "Ya existe una cuenta con ese celular. "
            "Inicia sesión o usa otro número.",
            code="CELULAR_TAKEN",
        )


@dataclass(frozen=True)
class IniciarRegistroPostulanteInput:
    ci: str
    nombres: str
    apellidos: str
    celular: str
    email: str
    password: str
    ip: str | None = None


class IniciarRegistroPostulante:
    """Valida datos y deja un RegistroPendiente. No crea User todavía."""

    @transaction.atomic
    def execute(self, data: IniciarRegistroPostulanteInput):
        ci = normalizar_ci(data.ci)
        celular = normalizar_celular(data.celular)
        email = data.email.strip().lower()

        _validar_disponibilidad(ci=ci, email=email, celular=celular)

        otp.validar_envio(
            celular=celular,
            ip=data.ip,
            proposito=CodigoOTP.Proposito.REGISTRO_PENDIENTE,
        )

        try:
            validate_password(
                data.password,
                user=User(
                    email=email,
                    first_name=data.nombres,
                    last_name=data.apellidos,
                ),
            )
        except DjangoValidationError as exc:
            raise DomainError(" ".join(exc.messages), code="WEAK_PASSWORD") from exc

        ahora = timezone.now()

        # Limpieza perezosa: pendientes vencidos no deben estorbar.
        RegistroPendiente.objects.filter(expira_en__lte=ahora).delete()

        # Un solo pendiente por celular: el nuevo reemplaza al anterior.
        RegistroPendiente.objects.filter(celular=celular).delete()

        pendiente = RegistroPendiente.objects.create(
            ci=ci,
            nombres=data.nombres.strip(),
            apellidos=data.apellidos.strip(),
            celular=celular,
            email=email,
            password_hash=make_password(data.password),
            expira_en=ahora
            + timedelta(minutes=settings.PENDING_REGISTRATION_TTL_MINUTES),
            ip=data.ip,
        )

        codigo = otp.crear_codigo(
            pendiente=pendiente,
            proposito=CodigoOTP.Proposito.REGISTRO_PENDIENTE,
            ip=data.ip,
        )
        transaction.on_commit(lambda: otp.enviar_codigo(pendiente, codigo))
        return pendiente, codigo


@dataclass(frozen=True)
class VerificarRegistroPostulanteInput:
    pendiente_id: str
    codigo: str
    ip: str | None = None


class VerificarRegistroPostulante:
    """Valida el OTP y recién ahí crea User + PostulanteProfile."""

    def execute(self, data: VerificarRegistroPostulanteInput) -> User:
        try:
            pendiente = RegistroPendiente.objects.get(pk=data.pendiente_id)
        except (RegistroPendiente.DoesNotExist, ValueError) as exc:
            raise DomainError(
                "El registro no existe o venció. Vuelve a empezar.",
                code="PENDING_NOT_FOUND",
            ) from exc

        if pendiente.expira_en <= timezone.now():
            raise DomainError(
                "El registro venció. Vuelve a empezar.",
                code="PENDING_EXPIRED",
            )

        # Revisión temprana para no consumir el OTP si ya está tomado.
        _validar_disponibilidad(
            ci=pendiente.ci,
            email=pendiente.email,
            celular=pendiente.celular,
        )

        valido, motivo = otp.validar_codigo(
            pendiente=pendiente,
            codigo=data.codigo,
            proposito=CodigoOTP.Proposito.REGISTRO_PENDIENTE,
        )
        if not valido:
            raise DomainError(
                ERRORES_CODIGO.get(motivo, "Código inválido."),
                code=motivo,
            )

        try:
            with transaction.atomic():
                try:
                    pendiente = RegistroPendiente.objects.select_for_update().get(
                        pk=data.pendiente_id
                    )
                except (RegistroPendiente.DoesNotExist, ValueError) as exc:
                    raise DomainError(
                        "El registro fue reemplazado o venció. Vuelve a empezar.",
                        code="PENDING_REPLACED",
                    ) from exc

                if pendiente.expira_en <= timezone.now():
                    raise DomainError(
                        "El registro venció. Vuelve a empezar.",
                        code="PENDING_EXPIRED",
                    )

                # Revalidación dentro de la transacción por si alguien ganó la carrera.
                _validar_disponibilidad(
                    ci=pendiente.ci,
                    email=pendiente.email,
                    celular=pendiente.celular,
                )

                user = CrearUsuario().execute(
                    CrearUsuarioInput(
                        email=pendiente.email,
                        password_hash=pendiente.password_hash,
                        role_code=Role.Code.POSTULANTE,
                        celular=pendiente.celular,
                        first_name=pendiente.nombres,
                        last_name=pendiente.apellidos,
                        is_active=True,
                        celular_verificado=True,
                    )
                )

                PostulanteProfile.objects.create(user=user, ci=pendiente.ci)

                # La creación y la limpieza de pendientes ocurren juntas.
                RegistroPendiente.objects.filter(
                    Q(celular=pendiente.celular)
                    | Q(email__iexact=pendiente.email)
                    | Q(ci=pendiente.ci)
                ).delete()

                return user
        except IntegrityError as exc:
            raise DomainError(
                "Otro registro tomó tus datos mientras verificabas. "
                "Vuelve a intentarlo.",
                code="REGISTRATION_CONFLICT",
            ) from exc


@dataclass(frozen=True)
class CambiarCelularPendienteInput:
    pendiente_id: str
    celular: str
    ip: str | None = None


class CambiarCelularPendiente:
    """Permite corregir el celular sin perder los demás datos pendientes."""

    @transaction.atomic
    def execute(self, data: CambiarCelularPendienteInput):
        celular = normalizar_celular(data.celular)

        try:
            pendiente = RegistroPendiente.objects.select_for_update().get(
                pk=data.pendiente_id
            )
        except (RegistroPendiente.DoesNotExist, ValueError) as exc:
            raise DomainError(
                "El registro no existe o venció. Vuelve a empezar.",
                code="PENDING_NOT_FOUND",
            ) from exc

        if pendiente.expira_en <= timezone.now():
            raise DomainError(
                "El registro venció. Vuelve a empezar.",
                code="PENDING_EXPIRED",
            )

        if User.objects.filter(celular=celular).exists():
            raise DomainError(
                "Ya existe una cuenta con ese celular. "
                "Inicia sesión o usa otro número.",
                code="CELULAR_TAKEN",
            )

        otp.validar_envio(
            celular=celular,
            ip=data.ip,
            proposito=CodigoOTP.Proposito.REGISTRO_PENDIENTE,
        )

        # Si otro pendiente tenía ese celular, se reemplaza.
        RegistroPendiente.objects.filter(celular=celular).exclude(
            pk=pendiente.pk
        ).delete()

        pendiente.celular = celular
        pendiente.save(update_fields=["celular", "actualizado_en"])

        codigo = otp.crear_codigo(
            pendiente=pendiente,
            proposito=CodigoOTP.Proposito.REGISTRO_PENDIENTE,
            ip=data.ip,
        )
        transaction.on_commit(lambda: otp.enviar_codigo(pendiente, codigo))
        return pendiente, codigo
