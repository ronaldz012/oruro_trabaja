from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.db.models import (Case,Count,Exists,F,IntegerField,OuterRef,Q,Value,When,)
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from apps.platform.accounts.models import Role
from apps.platform.audit import service as audit
from apps.platform.audit.models import AuditLog
from apps.recruitment.catalogos.models import (Departamento, Habilidad,Modalidad,Profesion,TipoContrato)
from apps.recruitment.ofertas.forms import OfertaForm
from apps.recruitment.ofertas.models import Oferta, OfertaGuardada, Postulacion
from apps.recruitment.ofertas.usecases.gestionar_oferta import (anular_oferta,aprobar_oferta,cerrar_oferta, devolver_oferta,iniciar_seleccion)
from apps.recruitment.ofertas.usecases.postulacion import (cambiar_estado,estados_siguientes,marcar_visto,postularse,retirar_postulacion)
from apps.recruitment.postulantes.services import calcular_completitud
from core.exceptions import DomainError
from core.pagination import paginar
from core.permissions import role_required

PASOS_POR_CAMPO = {
    "titulo": 1,
    "descripcion": 1,
    "plazas": 1,
    "profesiones": 1,
    "anos_experiencia": 1,
    "requisitos_obligatorios": 2,
    "requisitos_deseables": 2,
    "habilidades_obligatorias": 2,
    "habilidades_deseables": 2,
    "tipo_contrato": 3,
    "modalidad": 3,
    "departamento": 3,
    "municipio": 3,
    "salario_min": 3,
    "salario_max": 3,
    "a_tratar": 3,
    "beneficios": 3,
    "fecha_cierre": 3,
}


def _paso_inicial(form) -> int:
    for campo in form.errors:
        if campo in PASOS_POR_CAMPO:
            return PASOS_POR_CAMPO[campo]
    return 1


def _contexto_form_oferta(form) -> dict:
    return {
        "form": form,
        "paso_inicial": _paso_inicial(form),
        "profesiones_sugeridas": Profesion.objects.all(),
        "habilidades_sugeridas": Habilidad.objects.all(),
    }


def _empresa_actual(request):
    return getattr(request.user, "empresa", None)


def _puede_gestionar(empresa) -> bool:
    return bool(empresa and empresa.estado == empresa.Estado.APROBADA)


def _limite_alcanzado(empresa, oferta=None) -> bool:
    activas = empresa.ofertas.filter(
        estado__in=[Oferta.Estado.PUBLICADA, Oferta.Estado.EN_PROCESO_SELECCION]
    )
    if oferta is not None and oferta.activa:
        activas = activas.exclude(pk=oferta.pk)
    return activas.count() >= settings.EMPRESA_MAX_OFERTAS_ACTIVAS


@role_required(Role.Code.EMPRESA)
def empresa_lista(request):
    empresa = _empresa_actual(request)
    if empresa is None:
        messages.error(request, "Tu usuario no tiene una empresa asociada.")
        return redirect("dashboard:empresa")

    estado_actual = request.GET.get("estado") or ""
    estados_validos = dict(Oferta.Estado.choices)

    ofertas = Oferta.objects.filter(empresa=empresa).select_related(
        "tipo_contrato", "modalidad", "departamento"
    )
    if estado_actual in estados_validos:
        ofertas = ofertas.filter(estado=estado_actual)
    ofertas = ofertas.annotate(
        total_postulaciones=Count("postulaciones")
    ).order_by("-creado_en")

    conteos = {codigo: 0 for codigo in estados_validos}
    for fila in empresa.ofertas.values("estado").annotate(total=Count("id")):
        conteos[fila["estado"]] = fila["total"]

    page_obj = paginar(request, ofertas, 10)
    contexto = {
        "empresa": empresa,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "estados": [
            {"codigo": codigo, "nombre": nombre, "total": conteos[codigo]}
            for codigo, nombre in Oferta.Estado.choices
        ],
        "estado_actual": estado_actual,
        "total": sum(conteos.values()),
        "puede_gestionar": _puede_gestionar(empresa),
        "limite_alcanzado": _limite_alcanzado(empresa),
        "limite": settings.EMPRESA_MAX_OFERTAS_ACTIVAS,
    }
    return render(request, "ofertas/empresa_lista.html", contexto)


@role_required(Role.Code.EMPRESA)
def empresa_crear(request):
    empresa = _empresa_actual(request)
    if empresa is None:
        messages.error(request, "Tu usuario no tiene una empresa asociada.")
        return redirect("dashboard:empresa")
    if not _puede_gestionar(empresa):
        messages.error(request, "Tu empresa debe estar aprobada por GADOR para crear ofertas.")
        return redirect("dashboard:empresa")
    if _limite_alcanzado(empresa):
        messages.error(
            request,
            f"Alcanzaste el límite de {settings.EMPRESA_MAX_OFERTAS_ACTIVAS} ofertas activas.",
        )
        return redirect("ofertas:empresa_lista")

    if request.method == "POST":
        form = OfertaForm(request.POST, instance=Oferta(empresa=empresa))
        if form.is_valid():
            oferta = form.save()
            oferta.estado = Oferta.Estado.BORRADOR
            oferta.save(update_fields=["estado", "actualizado_en"])
            messages.success(request, "Oferta creada como borrador.")
            return redirect("ofertas:empresa_lista")
    else:
        form = OfertaForm(instance=Oferta(empresa=empresa))

    return render(
        request,
        "ofertas/empresa_form.html",
        {
            **_contexto_form_oferta(form),
            "empresa": empresa,
            "modo": "crear",
        },
    )


@role_required(Role.Code.EMPRESA)
def empresa_editar(request, pk):
    empresa = _empresa_actual(request)
    if empresa is None:
        messages.error(request, "Tu usuario no tiene una empresa asociada.")
        return redirect("dashboard:empresa")
    if not _puede_gestionar(empresa):
        messages.error(request, "Tu empresa debe estar aprobada por GADOR.")
        return redirect("dashboard:empresa")

    oferta = get_object_or_404(Oferta, pk=pk, empresa=empresa)
    if oferta.estado != Oferta.Estado.BORRADOR:
        messages.error(request, "Solo podés editar ofertas en borrador.")
        return redirect("ofertas:empresa_lista")

    if request.method == "POST":
        form = OfertaForm(request.POST, instance=oferta)
        if form.is_valid():
            form.save()
            messages.success(request, "Oferta actualizada.")
            return redirect("ofertas:empresa_lista")
    else:
        form = OfertaForm(instance=oferta)

    return render(
        request,
        "ofertas/empresa_form.html",
        {
            **_contexto_form_oferta(form),
            "empresa": empresa,
            "modo": "editar",
            "oferta": oferta,
        },
    )


@role_required(Role.Code.EMPRESA)
@require_POST
def empresa_enviar(request, pk):
    empresa = _empresa_actual(request)
    if empresa is None:
        return redirect("dashboard:empresa")
    if not _puede_gestionar(empresa):
        messages.error(request, "Tu empresa debe estar aprobada por GADOR.")
        return redirect("dashboard:empresa")

    oferta = get_object_or_404(Oferta, pk=pk, empresa=empresa)
    if oferta.estado != Oferta.Estado.BORRADOR:
        messages.error(request, "Solo se envían a revisión las ofertas en borrador.")
    elif _limite_alcanzado(empresa, oferta=oferta):
        messages.error(
            request,
            f"Alcanzaste el límite de {settings.EMPRESA_MAX_OFERTAS_ACTIVAS} ofertas activas.",
        )
    else:
        oferta.estado = Oferta.Estado.EN_REVISION_GADOR
        oferta.motivo_revision = ""
        oferta.save(update_fields=["estado", "motivo_revision", "actualizado_en"])
        messages.success(request, "Oferta enviada a revisión por GADOR.")

    return redirect("ofertas:empresa_lista")


@role_required(Role.Code.SUPERADMIN)
def gador_lista(request):
    estado_actual = request.GET.get("estado") or ""
    estados_validos = dict(Oferta.Estado.choices)

    ofertas = Oferta.objects.select_related(
        "empresa", "tipo_contrato", "modalidad", "departamento"
    )
    if estado_actual in estados_validos:
        ofertas = ofertas.filter(estado=estado_actual)

    orden_estado = Case(
        When(estado=Oferta.Estado.EN_REVISION_GADOR, then=Value(0)),
        When(estado=Oferta.Estado.BORRADOR, then=Value(1)),
        When(estado=Oferta.Estado.PUBLICADA, then=Value(2)),
        default=Value(3),
        output_field=IntegerField(),
    )
    ofertas = ofertas.annotate(orden_estado=orden_estado).order_by(
        "orden_estado", "-creado_en"
    )

    conteos = {codigo: 0 for codigo in estados_validos}
    for fila in Oferta.objects.values("estado").annotate(total=Count("id")):
        conteos[fila["estado"]] = fila["total"]

    page_obj = paginar(request, ofertas, 20)
    contexto = {
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "estados": [
            {"codigo": codigo, "nombre": nombre, "total": conteos[codigo]}
            for codigo, nombre in Oferta.Estado.choices
        ],
        "estado_actual": estado_actual,
        "total": sum(conteos.values()),
    }
    return render(request, "ofertas/gador_lista.html", contexto)


@role_required(Role.Code.SUPERADMIN)
def gador_detalle(request, pk):
    oferta = get_object_or_404(
        Oferta.objects.select_related(
            "empresa__user",
            "tipo_contrato",
            "modalidad",
            "departamento",
            "revisada_por",
        ).prefetch_related(
            "profesiones",
            "requerimientos_habilidad__habilidad",
        ),
        pk=pk,
    )
    return render(request, "ofertas/gador_detalle.html", {"oferta": oferta})


@role_required(Role.Code.SUPERADMIN)
@require_POST
def gador_accion(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    accion = request.POST.get("accion", "")
    motivo = request.POST.get("motivo", "")
    estado_antes = oferta.estado

    if accion == "aprobar":
        try:
            aprobar_oferta(oferta, actor=request.user)
        except ValueError as exc:
            messages.error(request, str(exc))
        else:
            audit.registrar(
                request,
                AuditLog.Accion.CAMBIO_ESTADO,
                oferta,
                antes={"estado": estado_antes},
                despues={"estado": oferta.estado},
            )
            messages.success(request, "Oferta publicada.")
    elif accion == "devolver":
        try:
            devolver_oferta(oferta, actor=request.user, motivo=motivo)
        except ValueError as exc:
            messages.error(request, str(exc))
        else:
            audit.registrar(
                request,
                AuditLog.Accion.CAMBIO_ESTADO,
                oferta,
                antes={"estado": estado_antes, "motivo": ""},
                despues={"estado": oferta.estado, "motivo": oferta.motivo_revision},
            )
            messages.success(request, "Oferta devuelta a borrador.")
    else:
        messages.error(request, "Acción inválida.")

    return redirect("ofertas:gador_detalle", pk=oferta.pk)


# ── Ofertas públicas para postulantes ────────────────────────────────────

def _perfil_postulante(request):
    perfil = getattr(request.user, "postulante_profile", None)
    if perfil is None:
        messages.error(request, "Tu cuenta no tiene un perfil de postulante.")
    return perfil


@role_required(Role.Code.POSTULANTE)
def publicas(request):
    perfil = _perfil_postulante(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    hoy = timezone.localdate()
    base = Oferta.objects.filter(
        estado=Oferta.Estado.PUBLICADA,
        fecha_cierre__gte=hoy,
    ).select_related(
        "empresa", "tipo_contrato", "modalidad", "departamento"
    )

    q = (request.GET.get("q") or "").strip()
    profesion = request.GET.get("profesion") or ""
    modalidad = request.GET.get("modalidad") or ""
    tipo = request.GET.get("tipo_contrato") or ""
    departamento = request.GET.get("departamento") or ""
    solo_guardadas = request.GET.get("guardadas") == "1"
    orden = request.GET.get("orden") or "recientes"
    if orden not in {"recientes", "cierre"}:
        orden = "recientes"

    ofertas = base
    if q:
        ofertas = ofertas.filter(
            Q(titulo__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(empresa__razon_social__icontains=q)
        )
    if profesion.isdigit():
        ofertas = ofertas.filter(profesiones__id=profesion)
    if modalidad.isdigit():
        ofertas = ofertas.filter(modalidad_id=modalidad)
    if tipo.isdigit():
        ofertas = ofertas.filter(tipo_contrato_id=tipo)
    if departamento.isdigit():
        ofertas = ofertas.filter(departamento_id=departamento)
    if solo_guardadas:
        ofertas = ofertas.filter(guardadas_por__postulante=perfil)

    if orden == "cierre":
        ofertas = ofertas.order_by("fecha_cierre", "-publicada_en")
    else:
        ofertas = ofertas.order_by("-publicada_en", "-creado_en")

    ofertas = ofertas.annotate(
        postulado=Exists(
            Postulacion.objects.filter(
                oferta=OuterRef("pk"),
                postulante=perfil,
            )
        ),
        guardada=Exists(
            OfertaGuardada.objects.filter(
                oferta=OuterRef("pk"),
                postulante=perfil,
            )
        ),
    )

    page_obj = paginar(request, ofertas, 10)
    filtros_activos = sum(
        [
            bool(profesion),
            bool(modalidad),
            bool(tipo),
            bool(departamento),
            orden != "recientes",
        ]
    )
    contexto = {
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "perfil": perfil,
        "completitud": calcular_completitud(perfil),
        "q": q,
        "profesion_actual": profesion,
        "modalidad_actual": modalidad,
        "tipo_actual": tipo,
        "departamento_actual": departamento,
        "orden_actual": orden,
        "guardadas_actual": solo_guardadas,
        "filtros_activos": filtros_activos,
        "total_resultados": page_obj.paginator.count,
        "total_guardadas": base.filter(
            guardadas_por__postulante=perfil
        ).count(),
        "profesiones": Profesion.objects.all(),
        "modalidades": Modalidad.objects.all(),
        "tipos_contrato": TipoContrato.objects.all(),
        "departamentos": Departamento.objects.all(),
    }
    return render(request, "ofertas/publicas.html", contexto)


@role_required(Role.Code.POSTULANTE)
def detalle(request, pk):
    perfil = _perfil_postulante(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    oferta = get_object_or_404(
        Oferta.objects.select_related(
            "empresa", "tipo_contrato", "modalidad", "departamento"
        ).prefetch_related(
            "profesiones",
            "requerimientos_habilidad__habilidad",
        ),
        pk=pk,
    )
    if oferta.estado not in {
        Oferta.Estado.PUBLICADA,
        Oferta.Estado.EN_PROCESO_SELECCION,
        Oferta.Estado.CERRADA,
    }:
        raise Http404("Oferta no disponible.")

    Oferta.objects.filter(pk=oferta.pk).update(vistas=F("vistas") + 1)
    oferta.vistas += 1

    postulacion = Postulacion.objects.filter(
        oferta=oferta,
        postulante=perfil,
    ).first()
    guardada = OfertaGuardada.objects.filter(
        oferta=oferta,
        postulante=perfil,
    ).exists()
    completitud = calcular_completitud(perfil)
    puede_postular = (
        completitud["puede_postular"]
        and oferta.estado == Oferta.Estado.PUBLICADA
        and oferta.fecha_cierre >= timezone.localdate()
        and postulacion is None
    )

    return render(
        request,
        "ofertas/detalle.html",
        {
            "oferta": oferta,
            "perfil": perfil,
            "completitud": completitud,
            "postulacion": postulacion,
            "guardada": guardada,
            "puede_postular": puede_postular,
        },
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def postular(request, pk):
    perfil = _perfil_postulante(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    oferta = get_object_or_404(Oferta, pk=pk)
    try:
        postularse(oferta, perfil, calcular_completitud(perfil))
    except DomainError as exc:
        messages.error(request, exc.message)
    else:
        messages.success(request, "Postulación enviada correctamente.")

    return redirect("ofertas:detalle", pk=oferta.pk)


@role_required(Role.Code.POSTULANTE)
@require_POST
def guardar(request, pk):
    perfil = _perfil_postulante(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    oferta = get_object_or_404(
        Oferta,
        pk=pk,
        estado__in=[
            Oferta.Estado.PUBLICADA,
            Oferta.Estado.EN_PROCESO_SELECCION,
            Oferta.Estado.CERRADA,
        ],
    )
    guardada, creada = OfertaGuardada.objects.get_or_create(
        postulante=perfil,
        oferta=oferta,
    )
    if creada:
        messages.success(request, "Oferta guardada.")
    else:
        guardada.delete()
        messages.info(request, "Oferta eliminada de guardadas.")

    siguiente = request.POST.get("next") or ""
    if not url_has_allowed_host_and_scheme(
        siguiente,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        siguiente = reverse("ofertas:publicas")

    return redirect(siguiente)


@role_required(Role.Code.POSTULANTE)
def mis_postulaciones(request):
    perfil = _perfil_postulante(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    postulaciones = perfil.postulaciones.select_related(
        "oferta__empresa",
        "oferta__modalidad",
        "oferta__departamento",
    ).order_by("-creado_en")
    page_obj = paginar(request, postulaciones, 10)

    return render(
        request,
        "ofertas/mis_postulaciones.html",
        {
            "page_obj": page_obj,
            "is_paginated": page_obj.has_other_pages(),
        },
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def postulacion_retirar(request, pk):
    perfil = _perfil_postulante(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    postulacion = get_object_or_404(Postulacion, pk=pk, postulante=perfil)
    try:
        retirar_postulacion(postulacion)
    except DomainError as exc:
        messages.error(request, exc.message)
    else:
        messages.success(request, "Postulación retirada.")

    return redirect("ofertas:mis_postulaciones")


# ── Detalle de oferta y postulantes para la empresa ──────────────────────

@role_required(Role.Code.EMPRESA)
def empresa_detalle(request, pk):
    empresa = _empresa_actual(request)
    if empresa is None:
        messages.error(request, "Tu usuario no tiene una empresa asociada.")
        return redirect("dashboard:empresa")

    oferta = get_object_or_404(
        Oferta.objects.select_related(
            "empresa", "tipo_contrato", "modalidad", "departamento"
        ).prefetch_related(
            "profesiones",
            "requerimientos_habilidad__habilidad",
        ),
        pk=pk,
        empresa=empresa,
    )
    postulaciones = oferta.postulaciones.select_related(
        "postulante__user",
        "postulante__profesion",
    ).order_by("-creado_en")

    return render(
        request,
        "ofertas/empresa_detalle.html",
        {
            "oferta": oferta,
            "empresa": empresa,
            "postulaciones": postulaciones,
            "puede_iniciar": oferta.estado == Oferta.Estado.PUBLICADA,
            "puede_cerrar": oferta.estado
            in {Oferta.Estado.PUBLICADA, Oferta.Estado.EN_PROCESO_SELECCION},
            "puede_anular": oferta.estado
            not in {Oferta.Estado.CERRADA, Oferta.Estado.ANULADA},
        },
    )


@role_required(Role.Code.EMPRESA)
@require_POST
def empresa_accion(request, pk):
    empresa = _empresa_actual(request)
    if empresa is None:
        return redirect("dashboard:empresa")

    oferta = get_object_or_404(Oferta, pk=pk, empresa=empresa)
    accion = request.POST.get("accion", "")

    try:
        if accion == "iniciar_seleccion":
            iniciar_seleccion(oferta)
        elif accion == "cerrar":
            cerrar_oferta(oferta)
        elif accion == "anular":
            anular_oferta(oferta)
        else:
            raise ValueError("Acción inválida.")
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Estado de la oferta actualizado.")

    return redirect("ofertas:empresa_detalle", pk=oferta.pk)


@role_required(Role.Code.EMPRESA)
def empresa_postulante(request, pk, postulacion_pk):
    empresa = _empresa_actual(request)
    if empresa is None:
        return redirect("dashboard:empresa")

    oferta = get_object_or_404(Oferta, pk=pk, empresa=empresa)
    postulacion = get_object_or_404(
        Postulacion.objects.select_related(
            "postulante__user",
            "postulante__profesion",
        ).prefetch_related(
            "postulante__formaciones",
            "postulante__experiencias",
            "postulante__habilidades__habilidad",
            "postulante__idiomas__idioma",
        ),
        pk=postulacion_pk,
        oferta=oferta,
    )
    marcar_visto(postulacion)
    siguientes = estados_siguientes(postulacion.estado)
    opciones_estado = [
        {"codigo": codigo, "nombre": nombre}
        for codigo, nombre in Postulacion.Estado.choices
        if codigo in siguientes
    ]

    return render(
        request,
        "ofertas/empresa_postulante.html",
        {
            "oferta": oferta,
            "postulacion": postulacion,
            "opciones_estado": opciones_estado,
        },
    )


@role_required(Role.Code.EMPRESA)
def empresa_postulante_cv(request, pk, postulacion_pk):
    empresa = _empresa_actual(request)
    if empresa is None:
        return redirect("dashboard:empresa")

    postulacion = get_object_or_404(
        Postulacion.objects.select_related("postulante"),
        pk=postulacion_pk,
        oferta_id=pk,
        oferta__empresa=empresa,
    )
    perfil = postulacion.postulante
    if not perfil.cv:
        raise Http404("El postulante no tiene CV.")

    return FileResponse(
        perfil.cv.open("rb"),
        as_attachment=True,
        filename=Path(perfil.cv.name).name,
        content_type="application/pdf",
    )


@role_required(Role.Code.EMPRESA)
@require_POST
def empresa_postulante_estado(request, pk, postulacion_pk):
    empresa = _empresa_actual(request)
    if empresa is None:
        return redirect("dashboard:empresa")

    oferta = get_object_or_404(Oferta, pk=pk, empresa=empresa)
    postulacion = get_object_or_404(Postulacion, pk=postulacion_pk, oferta=oferta)
    nuevo = request.POST.get("estado", "")

    try:
        cambiar_estado(postulacion, nuevo)
    except ValueError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, "Estado del postulante actualizado.")

    return redirect(
        "ofertas:empresa_postulante",
        pk=oferta.pk,
        postulacion_pk=postulacion.pk,
    )
