from __future__ import annotations

from django.conf import settings
from django.core.cache import cache


def _ip(request) -> str:
    return request.META.get("REMOTE_ADDR") or "desconocida"


def _clave(request) -> str:
    return f"login_attempts:{_ip(request)}"


def esta_bloqueado(request) -> bool:
    intentos = cache.get(_clave(request), 0)
    return intentos >= settings.LOGIN_MAX_ATTEMPTS


def mensaje_bloqueo() -> str:
    minutos = max(1, settings.LOGIN_TIMEOUT_SECONDS // 60)
    return (
        "Demasiados intentos desde esta conexión. "
        f"Esperá {minutos} minutos e intentá de nuevo."
    )


def registrar_fallo(request) -> None:
    clave = _clave(request)
    if cache.add(clave, 1, timeout=settings.LOGIN_TIMEOUT_SECONDS):
        return

    try:
        cache.incr(clave)
    except ValueError:
        cache.set(clave, 1, timeout=settings.LOGIN_TIMEOUT_SECONDS)


def limpiar_intentos(request) -> None:
    cache.delete(_clave(request))
