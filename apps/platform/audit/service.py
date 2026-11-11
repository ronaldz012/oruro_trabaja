from __future__ import annotations

from typing import Any

from apps.platform.audit.models import AuditLog


def _ip_de_request(request) -> str | None:
    """IP del cliente; si hay proxy, usa el primer valor de X-Forwarded-For."""
    if request is None:
        return None
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        return request.META["HTTP_X_FORWARDED_FOR"].split(",")[0].strip()
    return request.META.get("REMOTE_ADDR") or None


def registrar(
    request,
    accion: str,
    objeto=None,
    *,
    antes: dict[str, Any] | None = None,
    despues: dict[str, Any] | None = None,
    usuario=None,
) -> AuditLog:
    """Guarda una entrada de auditoría para la acción ejecutada.

    `objeto` puede ser None (por ejemplo LOGIN), en cuyo caso no se
    referencia tabla ni registro. Devuelve el AuditLog creado.
    """
    if objeto is not None:
        tabla = objeto._meta.db_table
        pk = objeto.pk
    else:
        tabla = ""
        pk = None

    if usuario is None:
        user = getattr(request, "user", None)
        if user is not None and user.is_authenticated:
            usuario = user

    return AuditLog.objects.create(
        usuario=usuario,
        accion=accion,
        tabla=tabla,
        registro_id=pk,
        datos_antes=antes,
        datos_despues=despues,
        ip=_ip_de_request(request),
    )
