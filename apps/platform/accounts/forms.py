from django import forms
from django.contrib.auth.forms import AuthenticationForm


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "autocomplete": "email",
                "class": "input",
                "placeholder": "tu@correo.com",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "input",
                "placeholder": "••••••••",
            }
        ),
    )

    error_messages = {
        "invalid_login": "Correo o contraseña incorrectos. Verifica tus datos.",
        "inactive": "Esta cuenta está inactiva.",
    }
