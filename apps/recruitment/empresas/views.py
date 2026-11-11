from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.db import IntegrityError
from django.db.models import Case, Count, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.platform.accounts.models import Role
from apps.platform.audit import service as audit
from apps.platform.audit.models import AuditLog
from apps.recruitment.empresas.forms import RegistroEmpresaForm
from apps.recruitment.empresas.models import Empresa
from apps.recruitment.empresas.usecases.gestionar_empresa import CambiarEstadoEmpresa
from apps.recruitment.empresas.usecases.registrar_empresa import (
    RegistrarEmpresa,
    RegistrarEmpresaInput,
)
from core.exceptions import DomainError
from core.pagination import paginar
from core.permissions import role_required


def registro(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistroEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user, _empresa = RegistrarEmpresa().execute(
                    RegistrarEmpresaInput(
                        email=form.cleaned_data["email"],
                        password=form.cleaned_data["password1"],
                        nit=form.cleaned_data["nit"],
                        razon_social=form.cleaned_data["razon_social"],
                        rubro=form.cleaned_data["rubro"],
                        representante_nombres=form.cleaned_data["representante_nombres"],
                        representante_apellidos=form.cleaned_data[
                            "representante_apellidos"
                        ],
                        representante_ci=form.cleaned_data["representante_ci"],
                        celular=form.cleaned_data["celular"],
                        direccion=form.cleaned_data["direccion"],
                        logo=form.cleaned_data["logo"],
                        descripcion=form.cleaned_data["descripcion"],
                    )
                )
            except DomainError as exc:
                form.add_error(None, exc.message)
            except IntegrityError:
                form.add_error(
                    None,
                    "No se pudo completar el registro. "
                    "Verifica los datos e intenta nuevamente.",
                )
            else:
                audit.registrar(
                    request,
                    AuditLog.Accion.CREAR,
                    _empresa,
                    despues={"estado": _empresa.estado},
                )
                auth_login(
                    request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                messages.success(
                    request,
                    "Registramos tu empresa. Queda pendiente de validación por GADOR.",
                )
                return redirect("dashboard:empresa")
    else:
        form = RegistroEmpresaForm()

    return render(request, "empresas/registro.html", {"form": form})


@role_required(Role.Code.SUPERADMIN)
def gador_lista(request):
    estado_actual = request.GET.get("estado") or ""
    estados_validos = dict(Empresa.Estado.choices)

    empresas = Empresa.objects.select_related("user", "rubro")
    if estado_actual in estados_validos:
        empresas = empresas.filter(estado=estado_actual)

    orden_estado = Case(
        When(estado=Empresa.Estado.PENDIENTE, then=Value(0)),
        When(estado=Empresa.Estado.RECHAZADA, then=Value(1)),
        When(estado=Empresa.Estado.APROBADA, then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )
    empresas = empresas.annotate(orden_estado=orden_estado).order_by(
        "orden_estado", "-creado_en"
    )

    conteos = {codigo: 0 for codigo in estados_validos}
    for fila in Empresa.objects.values("estado").annotate(total=Count("id")):
        conteos[fila["estado"]] = fila["total"]

    resumen_estados = [
        {"codigo": codigo, "nombre": nombre, "total": conteos[codigo]}
        for codigo, nombre in Empresa.Estado.choices
    ]

    page_obj = paginar(request, empresas, 20)

    contexto = {
        "empresas": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "estados": resumen_estados,
        "estado_actual": estado_actual,
        "conteos": conteos,
        "total": sum(conteos.values()),
    }
    return render(request, "empresas/gador_lista.html", contexto)


@role_required(Role.Code.SUPERADMIN)
def gador_detalle(request, pk):
    empresa = get_object_or_404(
        Empresa.objects.select_related("user", "rubro", "revisada_por"),
        pk=pk,
    )
    return render(
        request,
        "empresas/gador_detalle.html",
        {"empresa": empresa},
    )


@role_required(Role.Code.SUPERADMIN)
@require_POST
def gador_accion(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    accion = request.POST.get("accion", "")
    motivo = request.POST.get("motivo", "")
    estado_antes = [empresa.estado, empresa.motivo_rechazo]

    try:
        CambiarEstadoEmpresa().execute(
            empresa,
            accion=accion,
            actor=request.user,
            motivo=motivo,
        )
    except DomainError as exc:
        messages.error(request, exc.message)
    else:
        audit.registrar(
            request,
            AuditLog.Accion.CAMBIO_ESTADO,
            empresa,
            antes={"estado": estado_antes[0], "motivo": estado_antes[1]},
            despues={"estado": empresa.estado, "motivo": empresa.motivo_rechazo},
        )
        messages.success(
            request,
            f"Empresa actualizada a: {empresa.get_estado_display()}.",
        )

    return redirect("empresas:gador_detalle", pk=empresa.pk)

