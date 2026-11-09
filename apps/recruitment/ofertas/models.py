from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import TimeStampedModel


class Oferta(TimeStampedModel):
    class Estado(models.TextChoices):
        BORRADOR = "BORRADOR", "Borrador"
        EN_REVISION_GADOR = "EN_REVISION_GADOR", "En revisión GADOR"
        PUBLICADA = "PUBLICADA", "Publicada"
        EN_PROCESO_SELECCION = "EN_PROCESO_SELECCION", "En proceso de selección"
        CERRADA = "CERRADA", "Cerrada"
        ANULADA = "ANULADA", "Anulada"

    empresa = models.ForeignKey(
        "empresas.Empresa",
        on_delete=models.CASCADE,
        related_name="ofertas",
        verbose_name="Empresa",
    )
    titulo = models.CharField("Título", max_length=200)
    descripcion = models.TextField("Descripción")
    requisitos_obligatorios = models.TextField("Requisitos obligatorios")
    requisitos_deseables = models.TextField("Requisitos deseables", blank=True)
    profesiones = models.ManyToManyField(
        "catalogos.Profesion",
        related_name="ofertas",
        blank=True,
        verbose_name="Profesiones requeridas",
    )
    habilidades = models.ManyToManyField(
        "catalogos.Habilidad",
        through="OfertaHabilidad",
        related_name="ofertas",
        blank=True,
        verbose_name="Habilidades",
    )
    anos_experiencia = models.PositiveSmallIntegerField(
        "Años de experiencia",
        default=0,
    )
    tipo_contrato = models.ForeignKey(
        "catalogos.TipoContrato",
        on_delete=models.PROTECT,
        related_name="ofertas",
        verbose_name="Tipo de contrato",
    )
    modalidad = models.ForeignKey(
        "catalogos.Modalidad",
        on_delete=models.PROTECT,
        related_name="ofertas",
        verbose_name="Modalidad",
    )
    departamento = models.ForeignKey(
        "catalogos.Departamento",
        on_delete=models.PROTECT,
        related_name="ofertas",
        verbose_name="Departamento",
    )
    municipio = models.CharField("Municipio", max_length=120, blank=True)
    salario_min = models.DecimalField(
        "Salario mínimo",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    salario_max = models.DecimalField(
        "Salario máximo",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    a_tratar = models.BooleanField("Salario a tratar", default=False)
    beneficios = models.TextField("Beneficios", blank=True)
    fecha_cierre = models.DateField("Fecha de cierre")
    plazas = models.PositiveSmallIntegerField("Número de plazas", default=1)
    vistas = models.PositiveIntegerField("Vistas", default=0)
    estado = models.CharField(
        "Estado",
        max_length=30,
        choices=Estado.choices,
        default=Estado.BORRADOR,
        db_index=True,
    )
    motivo_revision = models.TextField("Motivo de revisión", blank=True)
    publicada_en = models.DateTimeField("Publicada en", null=True, blank=True)
    revisada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ofertas_revisadas",
        verbose_name="Revisada por",
    )
    revisada_en = models.DateTimeField("Revisada en", null=True, blank=True)

    class Meta:
        db_table = "ofertas"
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ["-creado_en"]

    def __str__(self):
        return self.titulo

    @property
    def activa(self) -> bool:
        return self.estado in {
            self.Estado.PUBLICADA,
            self.Estado.EN_PROCESO_SELECCION,
        }

    @property
    def vigente(self) -> bool:
        return self.estado == self.Estado.PUBLICADA and self.fecha_cierre >= timezone.localdate()


class OfertaHabilidad(TimeStampedModel):
    oferta = models.ForeignKey(
        Oferta,
        on_delete=models.CASCADE,
        related_name="requerimientos_habilidad",
        verbose_name="Oferta",
    )
    habilidad = models.ForeignKey(
        "catalogos.Habilidad",
        on_delete=models.PROTECT,
        related_name="requerimientos_oferta",
        verbose_name="Habilidad",
    )
    obligatoria = models.BooleanField("Obligatoria", default=True)

    class Meta:
        db_table = "oferta_habilidades"
        verbose_name = "Habilidad de la oferta"
        verbose_name_plural = "Habilidades de la oferta"
        constraints = [
            models.UniqueConstraint(
                fields=["oferta", "habilidad"],
                name="unique_habilidad_por_oferta",
            )
        ]

    def __str__(self):
        return f"{self.oferta} · {self.habilidad}"


class Postulacion(TimeStampedModel):
    class Estado(models.TextChoices):
        POSTULADO = "POSTULADO", "Postulado"
        VISTO = "VISTO", "Visto"
        PRESELECCIONADO = "PRESELECCIONADO", "Preseleccionado"
        ENTREVISTA = "ENTREVISTA", "Entrevista"
        FINALISTA = "FINALISTA", "Finalista"
        CONTRATADO = "CONTRATADO", "Contratado"
        RECHAZADO = "RECHAZADO", "Rechazado"

    oferta = models.ForeignKey(
        Oferta,
        on_delete=models.CASCADE,
        related_name="postulaciones",
        verbose_name="Oferta",
    )
    postulante = models.ForeignKey(
        "postulantes.PostulanteProfile",
        on_delete=models.CASCADE,
        related_name="postulaciones",
        verbose_name="Postulante",
    )
    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=Estado.choices,
        default=Estado.POSTULADO,
        db_index=True,
    )
    visto_en = models.DateTimeField("Visto en", null=True, blank=True)

    class Meta:
        db_table = "postulaciones"
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"
        ordering = ["-creado_en"]
        constraints = [
            models.UniqueConstraint(
                fields=["oferta", "postulante"],
                name="unique_postulacion_por_oferta",
            )
        ]

    def __str__(self):
        return f"{self.postulante} → {self.oferta}"


class OfertaGuardada(TimeStampedModel):
    postulante = models.ForeignKey(
        "postulantes.PostulanteProfile",
        on_delete=models.CASCADE,
        related_name="ofertas_guardadas",
        verbose_name="Postulante",
    )
    oferta = models.ForeignKey(
        Oferta,
        on_delete=models.CASCADE,
        related_name="guardadas_por",
        verbose_name="Oferta",
    )

    class Meta:
        db_table = "ofertas_guardadas"
        verbose_name = "Oferta guardada"
        verbose_name_plural = "Ofertas guardadas"
        ordering = ["-creado_en"]
        constraints = [
            models.UniqueConstraint(
                fields=["postulante", "oferta"],
                name="unique_oferta_guardada_por_postulante",
            )
        ]

    def __str__(self):
        return f"{self.postulante} ★ {self.oferta}"
