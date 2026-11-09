from __future__ import annotations

from apps.recruitment.postulantes.models import ci_validator
from core.normalizers import normalizar_celular

__all__ = ["normalizar_celular", "normalizar_ci"]


def normalizar_ci(valor: str) -> str:
    """Normaliza una CI boliviana: mayúsculas, sin guiones y espacios simples."""
    ci = " ".join(valor.strip().upper().replace("-", " ").split())
    ci_validator(ci)
    return ci
