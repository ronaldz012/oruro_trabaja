from django.db import models

from core.models import TimeStampedModel


class Profesion(TimeStampedModel):
    nombre = models.CharField("Nombre", max_length=120, unique=True)

    class Meta:
        db_table = "profesiones"
        verbose_name = "Profesión"
        verbose_name_plural = "Profesiones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Habilidad(TimeStampedModel):
    nombre = models.CharField("Nombre", max_length=120, unique=True)

    class Meta:
        db_table = "habilidades"
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Idioma(TimeStampedModel):
    nombre = models.CharField("Nombre", max_length=80, unique=True)

    class Meta:
        db_table = "idiomas"
        verbose_name = "Idioma"
        verbose_name_plural = "Idiomas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Rubro(TimeStampedModel):
    nombre = models.CharField("Nombre", max_length=120, unique=True)

    class Meta:
        db_table = "rubros"
        verbose_name = "Rubro"
        verbose_name_plural = "Rubros"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class TipoContrato(TimeStampedModel):
    nombre = models.CharField("Nombre", max_length=80, unique=True)

    class Meta:
        db_table = "tipos_contrato"
        verbose_name = "Tipo de contrato"
        verbose_name_plural = "Tipos de contrato"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Modalidad(TimeStampedModel):
    nombre = models.CharField("Nombre", max_length=80, unique=True)

    class Meta:
        db_table = "modalidades"
        verbose_name = "Modalidad"
        verbose_name_plural = "Modalidades"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Departamento(TimeStampedModel):
    nombre = models.CharField("Nombre", max_length=80, unique=True)

    class Meta:
        db_table = "departamentos"
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
