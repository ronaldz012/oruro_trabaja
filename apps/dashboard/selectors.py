"""Consultas agregadas para los widgets del panel.

El dashboard no define modelos: solo lee datos de ``accounts``, ``postulantes``,
``empresas``, ``ofertas``, ``postulaciones`` y ``reportes``.

Los modelos se resuelven de forma perezosa con ``apps.get_model`` para no
importarlos a nivel de módulo. Mientras una app de dominio todavía no exista,
sus widgets se resuelven con valores vacíos en lugar de romper el panel.
"""

from __future__ import annotations

import logging
from typing import Any

from django.apps import apps
from django.core.exceptions import FieldError
from django.db.models import Count

logger = logging.getLogger(__name__)

# Nombres de los modelos de dominio de los que depende el panel.
MODELOS: dict[str, tuple[str, str]] = {
    "usuarios": ("accounts", "User"),
    "empresas": ("empresas", "Empresa"),
    "postulantes": ("postulantes", "PostulanteProfile"),
    "ofertas": ("ofertas", "Oferta"),
    "postulaciones": ("ofertas", "Postulacion"),
    "reportes": ("reportes", "Reporte"),
}

# Relaciones esperadas entre los modelos. Si el modelo final usa otro ``related_name``
# basta con ajustar estas constantes.
OFERTA_EMPRESA = "empresa"  # Oferta.empresa
POSTULACION_OFERTA = "oferta"  # Postulacion.oferta
POSTULACION_POSTULANTE = "postulante"  # Postulacion.postulante
POSTULANTE_USUARIO = "user"  # PostulanteProfile.user


def _modelo(clave: str):
    """Devuelve el modelo asociado a ``clave`` o ``None`` si aún no existe."""
    app_label, nombre = MODELOS[clave]
    try:
        return apps.get_model(app_label, nombre)
    except LookupError:
        # Es esperable mientras las apps de dominio aún no existan.
        logger.debug(
            "dashboard: el modelo %s.%s no existe todavía; widget vacío.",
            app_label,
            nombre,
        )
        return None


def _contar(clave: str, **filtros: Any) -> int:
    """Cuenta registros del modelo, tolerando modelos o campos inexistentes."""
    modelo = _modelo(clave)
    if modelo is None:
        return 0
    try:
        return modelo.objects.filter(**filtros).count()
    except FieldError:
        logger.warning(
            "dashboard: filtro inválido para %s: %s", clave, sorted(filtros)
        )
        return 0


def _contar_distintos(clave: str, campo: str, **filtros: Any) -> int:
    """Cuenta valores distintos de ``campo`` (por ejemplo, postulantes únicos)."""
    modelo = _modelo(clave)
    if modelo is None:
        return 0
    try:
        resultado = (
            modelo.objects.filter(**filtros)
            .aggregate(total=Count(campo, distinct=True))
            .get("total")
        )
    except FieldError:
        logger.warning(
            "dashboard: campo inválido %s.%s para conteo distinto.", clave, campo
        )
        return 0
    return resultado or 0


def _conteo_por(
    clave: str,
    campo: str,
    *,
    limite: int | None = None,
    **filtros: Any,
) -> list[dict[str, Any]]:
    """Agrupa el modelo por ``campo`` y devuelve ``[{"valor", "total"}, ...]``."""
    modelo = _modelo(clave)
    if modelo is None:
        return []
    try:
        filas = (
            modelo.objects.filter(**filtros)
            .values(campo)
            .annotate(total=Count("pk"))
            .order_by("-total")
        )
        if limite is not None:
            filas = filas[:limite]
        return [{"valor": fila[campo], "total": fila["total"]} for fila in filas]
    except FieldError:
        logger.warning("dashboard: campo inválido %s.%s para agrupar.", clave, campo)
        return []


def resumen_gador() -> dict[str, Any]:
    """Widgets globales para el Dashboard del SuperAdmin (GADOR)."""
    return {
        "totales": {
            "usuarios": _contar("usuarios"),
            "empresas": _contar("empresas"),
            "postulantes": _contar("postulantes"),
            "ofertas": _contar("ofertas"),
            "postulaciones": _contar("postulaciones"),
            "reportes": _contar("reportes"),
        },
        "ofertas_por_estado": _conteo_por("ofertas", "estado"),
        "postulaciones_por_estado": _conteo_por("postulaciones", "estado"),
        "reportes_por_estado": _conteo_por("reportes", "estado"),
        "reportes_por_tipo": _conteo_por("reportes", "tipo"),
        "top_empresas": _conteo_por(
            "ofertas", f"{OFERTA_EMPRESA}__razon_social", limite=5
        ),
    }


def resumen_empresa(empresa_id: int | None) -> dict[str, Any]:
    """Widgets del Dashboard de una Empresa.

    ``empresa_id`` se obtiene del perfil de la empresa asociado al usuario.
    """
    if not empresa_id:
        return {
            "totales": {"ofertas": 0, "postulaciones": 0, "postulantes": 0},
            "postulaciones_por_estado": [],
        }

    filtro_ofertas = {f"{OFERTA_EMPRESA}_id": empresa_id}
    filtro_postulaciones = {
        f"{POSTULACION_OFERTA}__{OFERTA_EMPRESA}_id": empresa_id,
    }
    return {
        "totales": {
            "ofertas": _contar("ofertas", **filtro_ofertas),
            "postulaciones": _contar("postulaciones", **filtro_postulaciones),
            "postulantes": _contar_distintos(
                "postulaciones", POSTULACION_POSTULANTE, **filtro_postulaciones
            ),
        },
        "postulaciones_por_estado": _conteo_por(
            "postulaciones", "estado", **filtro_postulaciones
        ),
        "ofertas_por_estado": _conteo_por("ofertas", "estado", **filtro_ofertas),
    }


def resumen_postulante(usuario_id: int | None) -> dict[str, Any]:
    """Widgets del Dashboard de un Postulante.

    ``usuario_id`` es el ``pk`` del usuario autenticado; el postulante se
    localiza a través de su relación con ``accounts.User``.
    """
    if not usuario_id:
        return {
            "totales": {"postulaciones": 0, "ofertas_disponibles": 0},
            "postulaciones_por_estado": [],
        }

    filtro = {f"{POSTULACION_POSTULANTE}__{POSTULANTE_USUARIO}_id": usuario_id}
    return {
        "totales": {
            "postulaciones": _contar("postulaciones", **filtro),
            "ofertas_disponibles": _contar("ofertas", estado="PUBLICADA"),
        },
        "postulaciones_por_estado": _conteo_por(
            "postulaciones", "estado", **filtro
        ),
    }
