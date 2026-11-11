from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from apps.platform.accounts.models import Role, User
from apps.platform.audit import service as audit
from apps.platform.audit.models import AuditLog
from apps.recruitment.postulantes.models import PostulanteProfile

CV_EJEMPLO = Path(settings.BASE_DIR) / "assets" / "seed" / "cv-ejemplo.pdf"


ROLES = [
    (Role.Code.SUPERADMIN, "SuperAdmin GADOR"),
    (Role.Code.EMPRESA, "Empresa"),
    (Role.Code.POSTULANTE, "Postulante"),
]


class Command(BaseCommand):
    help = "Crea roles y usuarios por defecto para desarrollo."

    def handle(self, *args, **options):
        # 1. Roles
        for codigo, nombre in ROLES:
            Role.objects.get_or_create(
                codigo=codigo,
                defaults={"nombre": nombre},
            )

        # 2. Usuarios
        seeds = [
            (
                Role.Code.SUPERADMIN,
                settings.SEED_ADMIN_EMAIL,
                settings.SEED_ADMIN_PASSWORD,
                True,
            ),
            (
                Role.Code.EMPRESA,
                settings.SEED_EMPRESA_EMAIL,
                settings.SEED_EMPRESA_PASSWORD,
                False,
            ),
            (
                Role.Code.POSTULANTE,
                settings.SEED_POSTULANTE_EMAIL,
                settings.SEED_POSTULANTE_PASSWORD,
                False,
            ),
        ]

        for role_code, email, password, is_admin in seeds:
            if not password:
                raise CommandError(
                    f"Configura la contraseña para {role_code} en tu .env."
                )

            role = Role.objects.get(codigo=role_code)
            user = User.objects.filter(email__iexact=email).first()

            if user is None:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    role=role,
                    is_staff=is_admin,
                    is_superuser=is_admin,
                    celular_verificado=True,
                ) # type: ignore
                audit.registrar(
                    None,
                    AuditLog.Accion.CREAR,
                    user,
                    despues={"rol": role_code},
                    usuario=user,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Usuario {email} creado con rol {role_code}."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Usuario {email} ya existe; se omite.")
                )

            if user.role.codigo == Role.Code.POSTULANTE:
                perfil, _ = PostulanteProfile.objects.get_or_create(
                    user=user,
                    defaults={"ci": settings.SEED_POSTULANTE_CI},
                )
                if not perfil.presentacion:
                    perfil.presentacion = (
                        "Soy una persona comprometida con el aprendizaje continuo. "
                        "Busco aportar en proyectos donde pueda combinar formación "
                        "técnica, experiencia y trabajo en equipo."
                    )
                    perfil.save(update_fields=["presentacion"])
                if not perfil.cv:
                    if CV_EJEMPLO.exists():
                        perfil.cv.save(
                            "cv-ejemplo.pdf",
                            ContentFile(CV_EJEMPLO.read_bytes()),
                            save=True,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"CV de ejemplo asignado a {email}."
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                "No se encontró assets/seed/cv-ejemplo.pdf; "
                                "el postulante seed queda sin CV."
                            )
                        )