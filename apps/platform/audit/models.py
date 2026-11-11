from __future__ import annotations

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """Registro de auditoría de acciones relevantes del dominio.

    Cubre RF16: acciones CREAR, ACTUALIZAR, ELIMINAR, LOGIN y
    CAMBIO_ESTADO con el estado anterior y posterior en JSON.
    """

    class Accion(models.TextChoices):
        CREAR = "CREAR", "Crear"
        ACTUALIZAR = "ACTUALIZAR", "Actualizar"
        ELIMINAR = "ELIMINAR", "Eliminar"
        LOGIN = "LOGIN", "Login"
        CAMBIO_ESTADO = "CAMBIO_ESTADO", "Cambio de estado"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    accion = models.CharField(max_length=20, choices=Accion.choices)
    tabla = models.CharField(max_length=64)
    registro_id = models.PositiveIntegerField(null=True, blank=True)
    datos_antes = models.JSONField(null=True, blank=True)
    datos_despues = models.JSONField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        default_related_name = "audit_logs"
        ordering: tuple = ("-fecha",)
        verbose_name = "registro de auditoría"
        verbose_name_plural = "registros de auditoría"

    def __str__(self) -> str:
        actor = self.usuario or "anónimo"
        return f"{self.accion} · {self.tabla}#{self.registro_id or '-'} · {actor}"
