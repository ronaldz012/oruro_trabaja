from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from apps.platform.accounts.models import Role, User
from apps.platform.audit import service as audit
from apps.platform.audit.models import AuditLog
from apps.recruitment.catalogos.models import Rubro
from apps.recruitment.empresas.models import Empresa


class Command(BaseCommand):
    help = "Crea una empresa aprobada y otra pendiente para desarrollo."

    def handle(self, *args, **options):
        role = Role.objects.get(codigo=Role.Code.EMPRESA)
        admin = User.objects.filter(role__codigo=Role.Code.SUPERADMIN).first()

        if not settings.SEED_EMPRESA_PASSWORD:
            raise CommandError("Configura SEED_EMPRESA_PASSWORD en tu .env.")
        if not settings.SEED_EMPRESA_PENDIENTE_PASSWORD:
            raise CommandError(
                "Configura SEED_EMPRESA_PENDIENTE_PASSWORD "
                "o SEED_EMPRESA_PASSWORD en tu .env."
            )

        tecnologia, _ = Rubro.objects.get_or_create(nombre="Tecnología")
        comercio, _ = Rubro.objects.get_or_create(nombre="Comercio")

        aprobada = self._usuario(
            role=role,
            email=settings.SEED_EMPRESA_EMAIL,
            password=settings.SEED_EMPRESA_PASSWORD,
            nombres="Empresa",
            apellidos="Aprobada",
            celular="+59170000010",
        )
        empresa_aprobada, creada_aprobada = Empresa.objects.update_or_create(
            user=aprobada,
            defaults={
                "nit": "1000001",
                "razon_social": "Empresa Demo Aprobada S.R.L.",
                "rubro": tecnologia,
                "representante_nombres": "Ana",
                "representante_apellidos": "Aprobada",
                "representante_ci": "1111111 LP",
                "direccion": "Av. Demo 123, Oruro",
                "descripcion": "Empresa de ejemplo ya validada por GADOR.",
                "estado": Empresa.Estado.APROBADA,
                "motivo_rechazo": "",
                "revisada_por": admin,
                "revisada_en": timezone.now(),
            },
        )
        if creada_aprobada:
            audit.registrar(
                None,
                AuditLog.Accion.CREAR,
                empresa_aprobada,
                despues={"estado": Empresa.Estado.PENDIENTE},
                usuario=aprobada,
            )
            audit.registrar(
                None,
                AuditLog.Accion.CAMBIO_ESTADO,
                empresa_aprobada,
                antes={"estado": Empresa.Estado.PENDIENTE, "motivo": ""},
                despues={"estado": Empresa.Estado.APROBADA, "motivo": ""},
                usuario=admin,
            )

        pendiente = self._usuario(
            role=role,
            email=settings.SEED_EMPRESA_PENDIENTE_EMAIL,
            password=settings.SEED_EMPRESA_PENDIENTE_PASSWORD,
            nombres="Empresa",
            apellidos="Pendiente",
            celular="+59170000011",
        )
        empresa_pendiente, creada_pendiente = Empresa.objects.update_or_create(
            user=pendiente,
            defaults={
                "nit": "1000002",
                "razon_social": "Empresa Demo Pendiente S.R.L.",
                "rubro": comercio,
                "representante_nombres": "Luis",
                "representante_apellidos": "Pendiente",
                "representante_ci": "2222222 OR",
                "direccion": "Calle Pendiente 456, Oruro",
                "descripcion": "Empresa de ejemplo esperando validación de GADOR.",
                "estado": Empresa.Estado.PENDIENTE,
                "motivo_rechazo": "",
                "revisada_por": None,
                "revisada_en": None,
            },
        )
        if creada_pendiente:
            audit.registrar(
                None,
                AuditLog.Accion.CREAR,
                empresa_pendiente,
                despues={"estado": Empresa.Estado.PENDIENTE},
                usuario=pendiente,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Empresas seed listas: 1 aprobada y 1 pendiente de validación."
            )
        )

    def _usuario(
        self,
        *,
        role,
        email: str,
        password: str,
        nombres: str,
        apellidos: str,
        celular: str,
    ) -> User:
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            user = User.objects.create_user(
                email=email,
                password=password,
                role=role,
                first_name=nombres,
                last_name=apellidos,
                celular=celular,
                celular_verificado=True,
            ) # type: ignore
            return user

        cambios = []
        if not user.first_name:
            user.first_name = nombres
            cambios.append("first_name")
        if not user.last_name:
            user.last_name = apellidos
            cambios.append("last_name")
        if not user.celular:
            user.celular = celular
            cambios.append("celular")
        if cambios:
            user.save(update_fields=cambios)
        return user
