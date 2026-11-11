from __future__ import annotations

import re

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from apps.platform.accounts.models import User
from apps.recruitment.postulantes.models import (
    Experiencia,
    Formacion,
    Nivel,
    PostulanteProfile,
)
from apps.recruitment.postulantes.normalizers import normalizar_celular, normalizar_ci
from apps.recruitment.postulantes.validators import validar_cv, validar_tamano_cv


class RegistroPostulanteForm(forms.Form):
    ci = forms.CharField(
        label="Cédula de identidad",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "1234567",
                "autocomplete": "off",
            }
        ),
    )
    nombres = forms.CharField(
        label="Nombres",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Tus nombres",
                "autocomplete": "given-name",
            }
        ),
    )
    apellidos = forms.CharField(
        label="Apellidos",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Tus apellidos",
                "autocomplete": "family-name",
            }
        ),
    )
    celular = forms.CharField(
        label="Celular",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "71234567",
                "autocomplete": "tel",
                "inputmode": "tel",
            }
        ),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "placeholder": "tu@correo.com",
                "autocomplete": "email",
            }
        ),
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "••••••••",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirma tu contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": "••••••••",
                "autocomplete": "new-password",
            }
        ),
    )
    terminos = forms.BooleanField(
        label="Acepto los términos de uso y la política de privacidad.",
        error_messages={
            "required": "Debes aceptar los términos para continuar.",
        },
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 rounded border-secondary-300 text-primary-600 focus:ring-primary-300",
            }
        ),
    )

    def clean_ci(self) -> str:
        ci = normalizar_ci(self.cleaned_data["ci"])
        if PostulanteProfile.objects.filter(ci=ci).exists():
            raise forms.ValidationError(
                "Ya existe un postulante con esa CI. "
                "Si crees que es un error, contacta a GADOR."
            )
        return ci

    def clean_celular(self) -> str:
        celular = normalizar_celular(self.cleaned_data["celular"])
        if User.objects.filter(celular=celular).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta con ese celular. "
                "Inicia sesión o usa otro número."
            )
        return celular

    def clean_email(self) -> str:
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta con ese correo. "
                "Si crees que es un error, contacta a GADOR."
            )
        return email

    def clean_password1(self) -> str:
        password = self.cleaned_data["password1"]
        user = User(
            email=self.cleaned_data.get("email", ""),
            first_name=self.cleaned_data.get("nombres", ""),
            last_name=self.cleaned_data.get("apellidos", ""),
        )
        try:
            validate_password(password, user=user)
        except DjangoValidationError as exc:
            raise forms.ValidationError(exc.messages) from exc
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned_data


class CambiarCelularForm(forms.Form):
    celular = forms.CharField(
        label="Nuevo celular",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "+591 71234567",
                "autocomplete": "tel",
                "inputmode": "tel",
            }
        ),
    )

    def __init__(self, *args, pendiente=None, **kwargs):
        self.pendiente = pendiente
        super().__init__(*args, **kwargs)

    def clean_celular(self) -> str:
        celular = normalizar_celular(self.cleaned_data["celular"])
        if User.objects.filter(celular=celular).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta con ese celular. "
                "Inicia sesión o usa otro número."
            )
        return celular


class VerificarCodigoForm(forms.Form):
    codigo = forms.CharField(
        label="Código de verificación",
        min_length=6,
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "class": "input text-center text-lg tracking-[0.5em]",
                "placeholder": "000000",
                "inputmode": "numeric",
                "autocomplete": "one-time-code",
                "maxlength": 6,
            }
        ),
    )

    def clean_codigo(self) -> str:
        codigo = re.sub(r"\D", "", self.cleaned_data["codigo"])
        if len(codigo) != 6:
            raise forms.ValidationError("El código debe tener 6 dígitos.")
        return codigo


class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = PostulanteProfile
        fields = ("foto", "direccion", "fecha_nacimiento", "presentacion")
        widgets = {  # noqa: RUF012
            "foto": forms.FileInput(attrs={"class": "input", "accept": "image/*"}),
            "direccion": forms.TextInput(
                attrs={"class": "input", "placeholder": "Calle, número, zona"}
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={"class": "input", "type": "date"}
            ),
            "presentacion": forms.Textarea(
                attrs={
                    "class": "input min-h-28",
                    "rows": 4,
                    "placeholder": "Contá brevemente quién sos, qué buscás y qué podés aportar.",
                    "maxlength": 600,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["direccion"].required = True
        self.fields["direccion"].error_messages["required"] = (
            "La dirección es obligatoria."
        )
        self.fields["fecha_nacimiento"].required = True
        self.fields["fecha_nacimiento"].error_messages["required"] = (
            "La fecha de nacimiento es obligatoria."
        )
        self.fields["foto"].required = not bool(self.instance.foto)
        self.fields["foto"].error_messages["required"] = (
            "La foto de perfil es obligatoria."
        )
        self.fields["foto"].help_text = (
            "Obligatoria. Si ya tenés una, subí otra solo para reemplazarla."
        )


class FormacionForm(forms.ModelForm):
    class Meta:
        model = Formacion
        fields = ("titulo", "institucion", "anio_titulacion", "nro_titulo")
        widgets = {  # noqa: RUF012
            "titulo": forms.TextInput(
                attrs={"class": "input", "placeholder": "Ej. Ingeniero de Sistemas"}
            ),
            "institucion": forms.TextInput(
                attrs={"class": "input", "placeholder": "Universidad o instituto"}
            ),
            "anio_titulacion": forms.NumberInput(
                attrs={"class": "input", "min": 1950, "max": 2100}
            ),
            "nro_titulo": forms.TextInput(
                attrs={"class": "input", "placeholder": "Opcional"}
            ),
        }


class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ("empresa", "cargo", "anos", "descripcion")
        widgets = {  # noqa: RUF012
            "empresa": forms.TextInput(
                attrs={"class": "input", "placeholder": "Nombre de la empresa"}
            ),
            "cargo": forms.TextInput(
                attrs={"class": "input", "placeholder": "Cargo desempeñado"}
            ),
            "anos": forms.NumberInput(
                attrs={"class": "input", "min": 0, "max": 60}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "input min-h-24",
                    "rows": 3,
                    "placeholder": "Funciones principales (opcional)",
                }
            ),
        }


class HabilidadForm(forms.Form):
    nombre = forms.CharField(
        label="Habilidad",
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "list": "habilidades-sugeridas",
                "placeholder": "Ej. SQL, Excel, atención al cliente",
                "autocomplete": "off",
            }
        ),
    )
    nivel = forms.ChoiceField(
        label="Nivel",
        choices=Nivel.choices,
        widget=forms.Select(attrs={"class": "input"}),
    )


class IdiomaForm(forms.Form):
    nombre = forms.CharField(
        label="Idioma",
        max_length=80,
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "list": "idiomas-sugeridos",
                "placeholder": "Ej. Inglés, Quechua, Portugués",
                "autocomplete": "off",
            }
        ),
    )
    nivel = forms.ChoiceField(
        label="Nivel",
        choices=Nivel.choices,
        widget=forms.Select(attrs={"class": "input"}),
    )


class CVForm(forms.Form):
    cv = forms.FileField(
        label="CV en PDF",
        validators=[validar_cv, validar_tamano_cv],
        widget=forms.FileInput(
            attrs={"class": "input", "accept": "application/pdf"}
        ),
    )
