"""Control de acceso para cuentas desactivadas.

La verificación del celular ya no bloquea el login: el usuario solo se crea
después de verificar el OTP en el flujo de registro pendiente.
"""

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


class UserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user is not None and user.is_authenticated and not user.is_active:
            logout(request)
            messages.error(request, "Tu cuenta está desactivada.")
            return redirect("accounts:login")

        return self.get_response(request)
