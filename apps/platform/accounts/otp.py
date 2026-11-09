from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from apps.platform.accounts.models import CodigoOTP
from apps.platform.accounts.sms import get_sms_backend
from core.exceptions import DomainError

# Motivos de validación 
OK = "OK"
SIN_CODIGO = "SIN_CODIGO"
VENCIDO = "VENCIDO"
DEMASIADOS_INTENTOS = "DEMASIADOS_INTENTOS"
INVALIDO = "INVALIDO"


def _destino(user=None, pendiente=None) -> tuple:
    """Exige exactamente un destino: usuario o registro pendiente."""
    if (user is None) == (pendiente is None):
        raise ValueError("Debes indicar exactamente un destino OTP.")
    return user, pendiente


def _filtro(user=None, pendiente=None) -> Q:
    _destino(user, pendiente)
    if user is not None:
        return Q(user=user)
    return Q(registro_pendiente=pendiente)


def _celular(user=None, pendiente=None) -> str:
    _destino(user, pendiente)
    return user.celular if user is not None else pendiente.celular


def generar_codigo() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def _activos(user=None, pendiente=None, proposito: str = CodigoOTP.Proposito.REGISTRO):
    return CodigoOTP.objects.filter(
        _filtro(user=user, pendiente=pendiente),
        proposito=proposito,
        consumido_en__isnull=True,
    )


def crear_codigo(
    user=None,
    proposito: str = CodigoOTP.Proposito.REGISTRO,
    *,
    pendiente=None,
    ip: str | None = None,
) -> str:
    #Invalida los códigos activos anteriores y crea uno nuevo
    celular = _celular(user=user, pendiente=pendiente)
    if not celular:
        raise DomainError("No hay un celular para enviar el código.", code="SIN_CELULAR")

    ahora = timezone.now()
    _activos(user=user, pendiente=pendiente, proposito=proposito).update(
        consumido_en=ahora,
        actualizado_en=ahora,
    )

    codigo = generar_codigo()
    CodigoOTP.objects.create(
        user=user,
        registro_pendiente=pendiente,
        celular=celular,
        codigo_hash=make_password(codigo),
        proposito=proposito,
        expira_en=ahora + timedelta(minutes=settings.OTP_CODE_TTL_MINUTES),
        ip=ip,
    )
    return codigo


def enviar_codigo(destino, codigo: str) -> None:
    #Envía el código a un User, RegistroPendiente o string de celular
    celular = getattr(destino, "celular", None)
    if not celular and isinstance(destino, str):
        celular = destino
    if not celular:
        raise DomainError("El destino no tiene un celular registrado.", code="SIN_CELULAR")

    mensaje = (
        f"Oruro Trabaja: tu código es {codigo}. "
        f"Vence en {settings.OTP_CODE_TTL_MINUTES} minutos. No lo compartas."
    )
    get_sms_backend().enviar(celular, mensaje)


def ultimo_codigo(
    user=None,
    proposito: str = CodigoOTP.Proposito.REGISTRO,
    *,
    pendiente=None,
):
    return (
        CodigoOTP.objects.filter(
            _filtro(user=user, pendiente=pendiente),
            proposito=proposito,
        )
        .order_by("-creado_en")
        .first()
    )


@dataclass(frozen=True)
class EstadoReenvio:
    ultimo: CodigoOTP | None
    activo: bool
    segundos: int
    limite_alcanzado: bool

    @property
    def puede_reenviar(self) -> bool:
        return not self.limite_alcanzado and self.segundos == 0


def estado_reenvio(
    user=None,
    proposito: str = CodigoOTP.Proposito.REGISTRO,
    *,
    pendiente=None,
) -> EstadoReenvio:
    """Estado real del último código: vigencia, cooldown y límite por hora."""
    ahora = timezone.now()
    ultimo = ultimo_codigo(user=user, proposito=proposito, pendiente=pendiente)

    activo = bool(
        ultimo
        and ultimo.consumido_en is None
        and ultimo.expira_en > ahora
        and ultimo.intentos < settings.OTP_MAX_ATTEMPTS
    )

    segundos = 0
    if activo and ultimo is not None:
        transcurrido = (ahora - ultimo.creado_en).total_seconds()
        segundos = max(0, int(settings.OTP_RESEND_SECONDS - transcurrido))

    desde = ahora - timedelta(hours=1)
    envios = CodigoOTP.objects.filter(
        _filtro(user=user, pendiente=pendiente),
        proposito=proposito,
        creado_en__gte=desde,
    ).count()

    return EstadoReenvio(
        ultimo=ultimo,
        activo=activo,
        segundos=segundos,
        limite_alcanzado=envios >= settings.OTP_MAX_SENDS_PER_HOUR,
    )


def segundos_para_reenviar(
    user=None,
    proposito: str = CodigoOTP.Proposito.REGISTRO,
    *,
    pendiente=None,
) -> int:
    return estado_reenvio(user=user, proposito=proposito, pendiente=pendiente).segundos


def puede_reenviar(
    user=None,
    proposito: str = CodigoOTP.Proposito.REGISTRO,
    *,
    pendiente=None,
) -> tuple[bool, int, str]:
    """Devuelve (permitido, segundos_restantes, motivo)."""
    estado = estado_reenvio(user=user, proposito=proposito, pendiente=pendiente)
    if estado.segundos > 0:
        return False, estado.segundos, "COOLDOWN"
    if estado.limite_alcanzado:
        return False, 0, "LIMITE_ENVIOS"
    return True, 0, OK


def estado_envio(
    celular: str | None,
    ip: str | None = None,
    proposito: str = CodigoOTP.Proposito.REGISTRO_PENDIENTE,
) -> tuple[bool, int, str]:
    """Límites por celular e IP, independientes del pendiente concreto.

    Cuenta el historial de CodigoOTP, por eso sobrevive a que se borre o
    reemplace un RegistroPendiente.
    """
    if not celular:
        return False, 0, "SIN_CELULAR"

    ahora = timezone.now()

    ultimo = (
        CodigoOTP.objects.filter(celular=celular, proposito=proposito)
        .order_by("-creado_en")
        .first()
    )
    if ultimo is not None:
        transcurrido = (ahora - ultimo.creado_en).total_seconds()
        segundos = max(0, int(settings.OTP_RESEND_SECONDS - transcurrido))
        if segundos > 0:
            return False, segundos, "COOLDOWN"

    desde_celular = ahora - timedelta(hours=settings.OTP_PHONE_WINDOW_HOURS)
    envios_celular = CodigoOTP.objects.filter(
        celular=celular,
        proposito=proposito,
        creado_en__gte=desde_celular,
    ).count()
    if envios_celular >= settings.OTP_PHONE_MAX_SENDS:
        return False, 0, "LIMITE_CELULAR"

    if ip:
        desde_ip = ahora - timedelta(hours=settings.OTP_IP_WINDOW_HOURS)
        envios_ip = CodigoOTP.objects.filter(
            ip=ip,
            proposito=proposito,
            creado_en__gte=desde_ip,
        ).count()
        if envios_ip >= settings.OTP_IP_MAX_SENDS:
            return False, 0, "LIMITE_IP"

    return True, 0, OK


def validar_envio(
    celular: str | None,
    ip: str | None = None,
    proposito: str = CodigoOTP.Proposito.REGISTRO_PENDIENTE,
) -> None:
    permitido, segundos, motivo = estado_envio(celular, ip, proposito)
    if permitido:
        return

    if motivo == "SIN_CELULAR":
        raise DomainError(
            "No hay un celular para enviar el código.",
            code="SIN_CELULAR",
        )
    if motivo == "COOLDOWN":
        raise DomainError(
            f"Espera {segundos} segundos antes de pedir otro código.",
            code="OTP_COOLDOWN",
        )
    if motivo == "LIMITE_CELULAR":
        raise DomainError(
            "Se alcanzó el límite de "
            f"{settings.OTP_PHONE_MAX_SENDS} códigos por celular en "
            f"{settings.OTP_PHONE_WINDOW_HOURS} horas. Intenta más tarde.",
            code="OTP_LIMITE_CELULAR",
        )
    raise DomainError(
        "Se alcanzó el límite de "
        f"{settings.OTP_IP_MAX_SENDS} envíos por hora desde esta conexión. "
        "Intenta más tarde.",
        code="OTP_LIMITE_IP",
    )


def crear_y_enviar(
    user=None,
    proposito: str = CodigoOTP.Proposito.REGISTRO,
    *,
    pendiente=None,
    ip: str | None = None,
) -> str:
    celular = _celular(user=user, pendiente=pendiente)
    validar_envio(celular=celular, ip=ip, proposito=proposito)

    permitido, segundos, motivo = puede_reenviar(
        user=user,
        proposito=proposito,
        pendiente=pendiente,
    )
    if not permitido:
        if motivo == "COOLDOWN":
            raise DomainError(
                f"Espera {segundos} segundos antes de pedir otro código.",
                code="OTP_COOLDOWN",
            )
        raise DomainError(
            "Se alcanzó el límite de códigos por hora. Intenta más tarde.",
            code="OTP_LIMITE",
        )

    codigo = crear_codigo(
        user=user,
        proposito=proposito,
        pendiente=pendiente,
        ip=ip,
    )
    enviar_codigo(user or pendiente, codigo)
    return codigo


def validar_codigo(
    user=None,
    codigo: str = "",
    proposito: str = CodigoOTP.Proposito.REGISTRO,
    *,
    pendiente=None,
) -> tuple[bool, str]:
    """Valida el último código activo. Devuelve (es_valido, motivo)."""
    with transaction.atomic():
        otp = (
            _activos(user=user, pendiente=pendiente, proposito=proposito)
            .select_for_update()
            .order_by("-creado_en")
            .first()
        )
        if otp is None:
            return False, SIN_CODIGO

        ahora = timezone.now()
        if otp.expira_en <= ahora:
            otp.consumido_en = ahora
            otp.save(update_fields=["consumido_en", "actualizado_en"])
            return False, VENCIDO

        if otp.intentos >= settings.OTP_MAX_ATTEMPTS:
            otp.consumido_en = ahora
            otp.save(update_fields=["consumido_en", "actualizado_en"])
            return False, DEMASIADOS_INTENTOS

        if not check_password(codigo, otp.codigo_hash):
            otp.intentos += 1
            update_fields = ["intentos", "actualizado_en"]
            if otp.intentos >= settings.OTP_MAX_ATTEMPTS:
                otp.consumido_en = ahora
                update_fields.append("consumido_en")
            otp.save(update_fields=update_fields)
            if otp.intentos >= settings.OTP_MAX_ATTEMPTS:
                return False, DEMASIADOS_INTENTOS
            return False, INVALIDO

        otp.consumido_en = ahora
        otp.save(update_fields=["consumido_en", "actualizado_en"])
        return True, OK
