from __future__ import annotations

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from apps.platform.accounts.models import User
from apps.recruitment.catalogos.models import Rubro
from apps.recruitment.empresas.models import Empresa
from apps.recruitment.empresas.normalizers import normalizar_celular, normalizar_nit
from apps.recruitment.empresas.validators import validar_logo, validar_tamano_logo


class RegistroEmpresaForm(forms.Form):
    email = forms.EmailField(
        label="Email corporativo",
        widget=forms.EmailInput(
            attrs={
                "class": "input",
                "placeholder": "empresa@correo.com",
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
    nit = forms.CharField(
        label="NIT",
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "1234567890123"}
        ),
    )
    razon_social = forms.CharField(
        label="Razón social",
        max_length=200,
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Nombre legal de la empresa"}
        ),
    )
    rubro = forms.ModelChoiceField(
        label="Rubro",
        queryset=Rubro.objects.all(),
        empty_label="Selecciona un rubro",
        widget=forms.Select(attrs={"class": "input"}),
    )
    representante_nombres = forms.CharField(
        label="Nombres del representante",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "input"}),
    )
    representante_apellidos = forms.CharField(
        label="Apellidos del representante",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "input"}),
    )
    representante_ci = forms.CharField(
        label="CI del representante",
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "1234567 LP"}
        ),
    )
    celular = forms.CharField(
        label="Celular del representante",
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
    direccion = forms.CharField(
        label="Dirección",
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "input", "placeholder": "Calle, número, zona"}
        ),
    )
    logo = forms.FileField(
        label="Logo",
        required=False,
        validators=[validar_logo, validar_tamano_logo],
        widget=forms.FileInput(
            attrs={"class": "input", "accept": "image/*"}
        ),
    )
    descripcion = forms.CharField(
        label="Descripción de la empresa",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "input min-h-24",
                "rows": 3,
                "placeholder": "A qué se dedica la empresa",
            }
        ),
    )
    terminos = forms.BooleanField(
        label="Acepto los términos de uso y la política de privacidad.",
        error_messages={"required": "Debes aceptar los términos para continuar."},
        widget=forms.CheckboxInput(
            attrs={
                "class": "h-4 w-4 rounded border-secondary-300 text-primary-600 focus:ring-primary-300",
            }
        ),
    )

    def clean_email(self) -> str:
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta con ese correo. "
                "Si crees que es un error, contacta a GADOR."
            )
        return email

    def clean_celular(self) -> str:
        celular = normalizar_celular(self.cleaned_data["celular"])
        if User.objects.filter(celular=celular).exists():
            raise forms.ValidationError(
                "Ya existe una cuenta con ese celular. Inicia sesión o usa otro número."
            )
        return celular

    def clean_nit(self) -> str:
        nit = normalizar_nit(self.cleaned_data["nit"])
        if Empresa.objects.filter(nit=nit).exists():
            raise forms.ValidationError(
                "Ya existe una empresa con ese NIT. "
                "Si crees que es un error, contacta a GADOR."
            )
        return nit

    def clean_representante_ci(self) -> str:
        return " ".join(
            self.cleaned_data["representante_ci"].strip().upper().replace("-", " ").split()
        )

    def clean_password1(self) -> str:
        password = self.cleaned_data["password1"]
        user = User(
            email=self.cleaned_data.get("email", ""),
            first_name=self.cleaned_data.get("representante_nombres", ""),
            last_name=self.cleaned_data.get("representante_apellidos", ""),
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
