
from django.urls import reverse

from .models import Role

ROLE_DASHBOARD = {
    Role.Code.SUPERADMIN: "dashboard:gador",
    Role.Code.EMPRESA: "dashboard:empresa",
    Role.Code.POSTULANTE: "dashboard:postulante",
}


def dashboard_url_for(user) -> str:
    #Devuelve la URL del panel que corresponde al usuario autenticado
    role = getattr(getattr(user, "role", None), "codigo", None)

    if role in ROLE_DASHBOARD:
        return reverse(ROLE_DASHBOARD[role])  # type: ignore
    if getattr(user, "is_superuser", False):
        return reverse("admin:index")
    return reverse("accounts:login")
