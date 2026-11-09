from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from apps.recruitment.postulantes.validators import (
    validar_cv,
    validar_foto,
    validar_tamano_cv,
    validar_tamano_foto,
)
from core.models import TimeStampedModel
from core.storage import private_storage

ci_validator = RegexValidator(
    regex=r"^\d{6,8}(?:[- ]?[A-Z]{2})?$",
    message="Ingresa una CI válida (ej. 1234567 LP).",
)


class PostulanteProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="postulante_profile",
        verbose_name="Usuario",
    )
    ci = models.CharField(
        "Cédula de identidad",
        max_length=20,
        unique=True,
        validators=[ci_validator],
    )
    foto = models.FileField(
        "Foto de perfil",
        upload_to="postulantes/fotos/",
        blank=True,
        validators=[validar_foto, validar_tamano_foto],
    )
    direccion = models.CharField("Dirección", max_length=255, blank=True)
    fecha_nacimiento = models.DateField(
        "Fecha de nacimiento",
        null=True,
        blank=True,
    )
    presentacion = models.TextField(
        "Presentación",
        max_length=600,
        blank=True,
        help_text="Contá brevemente quién sos, qué buscás y qué podés aportar.",
    )
    profesion = models.ForeignKey(
        "catalogos.Profesion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="postulantes",
        verbose_name="Profesión",
    )
    cv = models.FileField(
        "CV en PDF",
        upload_to="postulantes/cv/",
        storage=private_storage,
        blank=True,
        validators=[validar_cv, validar_tamano_cv],
    )

    class Meta:
        db_table = "postulante_profiles"
        verbose_name = "Perfil de postulante"
        verbose_name_plural = "Perfiles de postulantes"

    def __str__(self):
        return f"{self.user} · {self.ci}"


class Nivel(models.TextChoices):
    BASICO = "BASICO", "Básico"
    INTERMEDIO = "INTERMEDIO", "Intermedio"
    AVANZADO = "AVANZADO", "Avanzado"
    EXPERTO = "EXPERTO", "Experto"


class Formacion(TimeStampedModel):
    profile = models.ForeignKey(
        PostulanteProfile,
        on_delete=models.CASCADE,
        related_name="formaciones",
        verbose_name="Perfil",
    )
    titulo = models.CharField("Título", max_length=160)
    institucion = models.CharField("Universidad o instituto", max_length=160)
    anio_titulacion = models.PositiveSmallIntegerField(
        "Año de titulación",
        validators=[MinValueValidator(1950), MaxValueValidator(2100)],
    )
    nro_titulo = models.CharField(
        "Nro. de título nacional",
        max_length=60,
        blank=True,
    )

    class Meta:
        db_table = "formaciones"
        verbose_name = "Formación académica"
        verbose_name_plural = "Formaciones académicas"
        ordering = ["-anio_titulacion", "-creado_en"]

    def __str__(self):
        return f"{self.titulo} · {self.institucion}"


class Experiencia(TimeStampedModel):
    profile = models.ForeignKey(
        PostulanteProfile,
        on_delete=models.CASCADE,
        related_name="experiencias",
        verbose_name="Perfil",
    )
    empresa = models.CharField("Empresa", max_length=160)
    cargo = models.CharField("Cargo", max_length=160)
    anos = models.PositiveSmallIntegerField(
        "Años",
        validators=[MinValueValidator(0), MaxValueValidator(60)],
    )
    descripcion = models.TextField("Descripción", blank=True)

    class Meta:
        db_table = "experiencias"
        verbose_name = "Experiencia laboral"
        verbose_name_plural = "Experiencias laborales"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.cargo} · {self.empresa}"


class PostulanteHabilidad(TimeStampedModel):
    profile = models.ForeignKey(
        PostulanteProfile,
        on_delete=models.CASCADE,
        related_name="habilidades",
        verbose_name="Perfil",
    )
    habilidad = models.ForeignKey(
        "catalogos.Habilidad",
        on_delete=models.PROTECT,
        related_name="postulantes",
        verbose_name="Habilidad",
    )
    nivel = models.CharField(
        "Nivel",
        max_length=20,
        choices=Nivel.choices,
        default=Nivel.INTERMEDIO,
    )

    class Meta:
        db_table = "postulante_habilidades"
        verbose_name = "Habilidad del postulante"
        verbose_name_plural = "Habilidades del postulante"
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "habilidad"],
                name="unique_habilidad_por_postulante",
            )
        ]

    def __str__(self):
        return f"{self.habilidad} · {self.get_nivel_display()}"


class PostulanteIdioma(TimeStampedModel):
    profile = models.ForeignKey(
        PostulanteProfile,
        on_delete=models.CASCADE,
        related_name="idiomas",
        verbose_name="Perfil",
    )
    idioma = models.ForeignKey(
        "catalogos.Idioma",
        on_delete=models.PROTECT,
        related_name="postulantes",
        verbose_name="Idioma",
    )
    nivel = models.CharField(
        "Nivel",
        max_length=20,
        choices=Nivel.choices,
        default=Nivel.INTERMEDIO,
    )

    class Meta:
        db_table = "postulante_idiomas"
        verbose_name = "Idioma del postulante"
        verbose_name_plural = "Idiomas del postulante"
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "idioma"],
                name="unique_idioma_por_postulante",
            )
        ]

    def __str__(self):
        return f"{self.idioma} · {self.get_nivel_display()}"
