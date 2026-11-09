from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import NON_FIELD_ERRORS
from django.shortcuts import redirect

from .forms import EmailAuthenticationForm
from .redirects import dashboard_url_for
from .throttle import (
    esta_bloqueado,
    limpiar_intentos,
    mensaje_bloqueo,
    registrar_fallo,
)


class RoleLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        if esta_bloqueado(request):
            form = self.get_form()
            form.add_error(None, mensaje_bloqueo())
            return self.render_to_response(self.get_context_data(form=form))
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        if form.has_error(NON_FIELD_ERRORS, "invalid_login"):
            registrar_fallo(self.request)
        return super().form_invalid(form)

    def form_valid(self, form):
        limpiar_intentos(self.request)
        return super().form_valid(form)

    def get_success_url(self):
        return dashboard_url_for(self.request.user)


class RoleLogoutView(LogoutView):
    next_page = "accounts:login"


def home(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    return redirect(dashboard_url_for(request.user))
