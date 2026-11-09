from django.shortcuts import render

from apps.platform.accounts.models import Role
from apps.recruitment.empresas.models import Empresa
from apps.recruitment.ofertas.models import Oferta
from apps.recruitment.postulantes.services import calcular_completitud
from core.permissions import role_required

from . import selectors


@role_required(Role.Code.SUPERADMIN)
def dashboard_gador(request):
    """Panel global del SuperAdmin: usuarios, empresas y actividad de la plataforma."""
    contexto = {
        "resumen": selectors.resumen_gador(),
        "empresas_pendientes": Empresa.objects.filter(
            estado=Empresa.Estado.PENDIENTE
        ).count(),
        "ofertas_pendientes": Oferta.objects.filter(
            estado=Oferta.Estado.EN_REVISION_GADOR
        ).count(),
    }
    return render(request, "dashboard/gador.html", contexto)


@role_required(Role.Code.SUPERADMIN)
def reportes_gador(request):
    """Reportes exportables: placeholder de la demo."""
    return render(request, "dashboard/reportes.html")


@role_required(Role.Code.EMPRESA)
def dashboard_empresa(request):
    """Panel de la empresa autenticada: estado y resumen de actividad."""
    empresa = getattr(request.user, "empresa", None)
    contexto = {
        "resumen": selectors.resumen_empresa(getattr(empresa, "pk", None)),
        "empresa": empresa,
    }
    return render(request, "dashboard/empresa.html", contexto)


@role_required(Role.Code.POSTULANTE)
def dashboard_postulante(request):
    """Panel del postulante autenticado: sus postulaciones y ofertas disponibles."""
    perfil = getattr(request.user, "postulante_profile", None)
    contexto = {
        "resumen": selectors.resumen_postulante(request.user.pk),
        "perfil": perfil,
        "completitud": calcular_completitud(perfil),
    }
    return render(request, "dashboard/postulante.html", contexto)
