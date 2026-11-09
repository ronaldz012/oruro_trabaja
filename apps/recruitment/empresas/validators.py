from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validar_tamano_logo(value):
    if value.size > 2 * 1024 * 1024:
        raise ValidationError("El logo no puede superar los 2 MB.")


validar_logo = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png"],
    message="El logo debe ser JPG o PNG.",
)
