from __future__ import annotations

import re

from django import forms

from core.normalizers import normalizar_celular

__all__ = ["normalizar_celular", "normalizar_nit"]


def normalizar_nit(valor: str) -> str:
    """Deja solo dígitos del NIT boliviano."""
    nit = re.sub(r"\D", "", valor or "")
    if not (7 <= len(nit) <= 13):
        raise forms.ValidationError(
            "Ingresa un NIT válido (entre 7 y 13 dígitos)."
        )
    return nit
