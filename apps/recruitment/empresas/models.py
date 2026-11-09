from django.conf import settings
from django.db import models

from apps.recruitment.empresas.validators import validar_logo, validar_tamano_logo
from core.models import TimeStampedModel


class Empresa(TimeStampedModel):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE_VALIDACION", "Pendiente de validación"
        APROBADA = "APROBADA", "Aprobada"
        RECHAZADA = "RECHAZADA", "Rechazada"
        SUSPENDIDA = "SUSPENDIDA", "Suspendida"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="empresa",
        verbose_name="Usuario",
    )
    nit = models.CharField("NIT", max_length=20, unique=True)
    razon_social = models.CharField("Razón social", max_length=200)
    rubro = models.ForeignKey(
        "catalogos.Rubro",
        on_delete=models.PROTECT,
        related_name="empresas",
        verbose_name="Rubro",
    )
    representante_nombres = models.CharField("Nombres del representante", max_length=150)
    representante_apellidos = models.CharField(
        "Apellidos del representante", max_length=150
    )
    representante_ci = models.CharField("CI del representante", max_length=20)
    direccion = models.CharField("Dirección", max_length=255)
    logo = models.FileField(
        "Logo",
        upload_to="empresas/logos/",
        blank=True,
        validators=[validar_logo, validar_tamano_logo],
    )
    descripcion = models.TextField("Descripción", blank=True)
    estado = models.CharField(
        "Estado",
        max_length=30,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        db_index=True,
    )
    motivo_rechazo = models.TextField("Motivo de rechazo", blank=True)
    revisada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="empresas_revisadas",
        verbose_name="Revisada por",
    )
    revisada_en = models.DateTimeField("Revisada en", null=True, blank=True)

    class Meta:
        db_table = "empresas"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.razon_social} · {self.nit}"

    @property
    def aprobada(self) -> bool:
        return self.estado == self.Estado.APROBADA
