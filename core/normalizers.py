from __future__ import annotations

import re

from django import forms


def normalizar_celular(valor: str) -> str:
    """Normaliza un celular boliviano a E.164 (+591XXXXXXXX)."""
    digitos = re.sub(r"\D", "", valor)
    digitos = digitos.removeprefix("591")
    if not re.fullmatch(r"[67]\d{7}", digitos):
        raise forms.ValidationError(
            "Ingresa un celular boliviano válido (ej. 71234567)."
        )
    return f"+591{digitos}"
