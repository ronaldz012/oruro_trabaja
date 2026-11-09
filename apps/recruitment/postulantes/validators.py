from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validar_tamano_cv(value):
    if value.size > 5 * 1024 * 1024:
        raise ValidationError("El CV no puede superar los 5 MB.")


def validar_tamano_foto(value):
    if value.size > 2 * 1024 * 1024:
        raise ValidationError("La foto no puede superar los 2 MB.")


validar_cv = FileExtensionValidator(
    allowed_extensions=["pdf"],
    message="El CV debe ser un archivo PDF.",
)
validar_foto = FileExtensionValidator(
    allowed_extensions=["jpg", "jpeg", "png"],
    message="La foto debe ser JPG o PNG.",
)
