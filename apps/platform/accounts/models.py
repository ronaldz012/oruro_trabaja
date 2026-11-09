import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from core.models import TimeStampedModel


class Role(models.Model):
    class Code(models.TextChoices):
        SUPERADMIN = "SUPERADMIN", "SuperAdmin"
        EMPRESA = "EMPRESA", "Empresa"
        POSTULANTE = "POSTULANTE", "Postulante"

    codigo = models.CharField("Código", max_length=20, choices=Code.choices, unique=True)
    nombre = models.CharField("Nombre", max_length=80)

    class Meta:
        db_table = "roles"
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if "role" not in extra_fields:
            extra_fields["role"] = Role.objects.get(codigo=Role.Code.SUPERADMIN)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("Correo electrónico", unique=True)
    celular = models.CharField(
        "Celular",
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="users",
        verbose_name="Rol",
    )
    celular_verificado = models.BooleanField("Celular verificado", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager() # type: ignore

    class Meta:
        db_table = "users"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email


class RegistroPendiente(TimeStampedModel):
    """Datos temporales de un registro que aún no tiene usuario."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ci = models.CharField("Cédula de identidad", max_length=20)
    nombres = models.CharField("Nombres", max_length=150)
    apellidos = models.CharField("Apellidos", max_length=150)
    celular = models.CharField("Celular", max_length=20, unique=True)
    email = models.EmailField("Correo electrónico")
    password_hash = models.CharField("Contraseña (hash)", max_length=128)
    expira_en = models.DateTimeField("Expira en")
    ip = models.GenericIPAddressField("IP", null=True, blank=True)

    class Meta:
        db_table = "registros_pendientes"
        verbose_name = "Registro pendiente"
        verbose_name_plural = "Registros pendientes"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["ci"]),
            models.Index(fields=["expira_en"]),
        ]

    def __str__(self):
        return f"{self.celular} · {self.email}"


class CodigoOTP(TimeStampedModel):
    class Proposito(models.TextChoices):
        REGISTRO = "REGISTRO", "Registro"
        REGISTRO_PENDIENTE = "REGISTRO_PENDIENTE", "Registro pendiente"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="codigos_otp",
        verbose_name="Usuario",
    )
    registro_pendiente = models.ForeignKey(
        RegistroPendiente,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="codigos_otp",
        verbose_name="Registro pendiente",
    )
    celular = models.CharField("Celular", max_length=20)
    codigo_hash = models.CharField("Código (hash)", max_length=128)
    proposito = models.CharField(
        "Propósito",
        max_length=20,
        choices=Proposito.choices,
        default=Proposito.REGISTRO,
    )
    expira_en = models.DateTimeField("Expira en")
    intentos = models.PositiveSmallIntegerField("Intentos", default=0)
    consumido_en = models.DateTimeField("Consumido en", null=True, blank=True)
    ip = models.GenericIPAddressField("IP", null=True, blank=True)

    class Meta:
        db_table = "codigos_otp"
        verbose_name = "Código OTP"
        verbose_name_plural = "Códigos OTP"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["user", "proposito", "creado_en"]),
            models.Index(
                fields=["registro_pendiente", "proposito", "creado_en"],
            ),
            models.Index(fields=["celular", "proposito", "creado_en"]),
            models.Index(fields=["ip", "proposito", "creado_en"]),
        ]

    def __str__(self):
        destino = self.user or self.registro_pendiente or self.celular
        return f"{destino} · {self.proposito}"
