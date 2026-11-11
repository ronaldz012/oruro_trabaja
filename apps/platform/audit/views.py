from __future__ import annotations

from django.shortcuts import get_object_or_404, render

from apps.platform.accounts.models import Role
from apps.platform.audit.models import AuditLog
from core.pagination import paginar
from core.permissions import role_required


@role_required(Role.Code.SUPERADMIN)
def lista(request):
    return render(
        request,
        "audit/lista.html",
        {"registros": paginar(request, AuditLog.objects.select_related("usuario"), 20)},
    )


@role_required(Role.Code.SUPERADMIN)
def detalle(request, pk):
    registro = get_object_or_404(
        AuditLog.objects.select_related("usuario"),
        pk=pk,
    )
    return render(request, "audit/detalle.html", {"registro": registro})
