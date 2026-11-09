from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.platform.accounts import otp
from apps.platform.accounts.models import CodigoOTP, RegistroPendiente, Role
from apps.recruitment.catalogos.models import Habilidad, Idioma
from core.exceptions import DomainError
from core.permissions import role_required

from .forms import (
    CambiarCelularForm,
    CVForm,
    DatosPersonalesForm,
    ExperienciaForm,
    FormacionForm,
    HabilidadForm,
    IdiomaForm,
    RegistroPostulanteForm,
    VerificarCodigoForm,
)
from .models import Experiencia, Formacion, PostulanteHabilidad, PostulanteIdioma
from .services import MIN_HABILIDADES, calcular_completitud
from .usecases.registrar_postulante import (
    CambiarCelularPendiente,
    CambiarCelularPendienteInput,
    IniciarRegistroPostulante,
    IniciarRegistroPostulanteInput,
    VerificarRegistroPostulante,
    VerificarRegistroPostulanteInput,
)

PENDING_SESSION_KEY = "registro_pendiente_id"
DEMO_OTP_KEY = "demo_otp"
PROPOSITO = CodigoOTP.Proposito.REGISTRO_PENDIENTE


def _ip(request) -> str | None:
    return request.META.get("REMOTE_ADDR") or None


def _limpiar_sesion(request) -> None:
    request.session.pop(PENDING_SESSION_KEY, None)
    request.session.pop(DEMO_OTP_KEY, None)


def _get_pendiente(request) -> RegistroPendiente | None:
    pendiente_id = request.session.get(PENDING_SESSION_KEY)
    if not pendiente_id:
        return None

    pendiente = RegistroPendiente.objects.filter(pk=pendiente_id).first()
    if pendiente is None:
        _limpiar_sesion(request)
        return None

    if pendiente.expira_en <= timezone.now():
        _limpiar_sesion(request)
        return None

    return pendiente


def _demo_codigo_vigente(pendiente, codigo: str | None) -> bool:
    if not codigo:
        return False

    actual = otp.ultimo_codigo(pendiente=pendiente, proposito=PROPOSITO)
    if actual is None or actual.consumido_en is not None:
        return False
    if actual.expira_en <= timezone.now():
        return False
    if actual.intentos >= settings.OTP_MAX_ATTEMPTS:
        return False
    return check_password(codigo, actual.codigo_hash)


def _demo_codigo_sesion(request, pendiente) -> str | None:
    """Código demo visible solo si pertenece al último token vigente."""
    if not settings.DEMO_MODE:
        return None

    codigo = request.session.get(DEMO_OTP_KEY)
    if not codigo:
        return None

    if not _demo_codigo_vigente(pendiente, codigo):
        request.session.pop(DEMO_OTP_KEY, None)
        return None

    return codigo


def _contexto_verificacion(request, pendiente, form, estado) -> dict:
    return {
        "form": form,
        "celular": pendiente.celular,
        "segundos_para_reenviar": estado.segundos,
        "puede_reenviar": estado.puede_reenviar,
        "limite_alcanzado": estado.limite_alcanzado,
        "codigo_vencido": bool(estado.ultimo) and not estado.activo,
        "demo_codigo": _demo_codigo_sesion(request, pendiente),
    }


def registro(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistroPostulanteForm(request.POST)
        if form.is_valid():
            try:
                pendiente, codigo = IniciarRegistroPostulante().execute(
                    IniciarRegistroPostulanteInput(
                        ci=form.cleaned_data["ci"],
                        nombres=form.cleaned_data["nombres"],
                        apellidos=form.cleaned_data["apellidos"],
                        celular=form.cleaned_data["celular"],
                        email=form.cleaned_data["email"],
                        password=form.cleaned_data["password1"],
                        ip=_ip(request),
                    )
                )
            except DomainError as exc:
                form.add_error(None, exc.message)
            except IntegrityError:
                form.add_error(
                    None,
                    "No se pudo iniciar el registro. Verifica tus datos e intenta nuevamente.",
                )
            else:
                request.session[PENDING_SESSION_KEY] = str(pendiente.pk)
                if settings.DEMO_MODE:
                    request.session[DEMO_OTP_KEY] = codigo
                return redirect("postulantes:verificar_celular")
    else:
        form = RegistroPostulanteForm()

    return render(request, "postulantes/registro.html", {"form": form})


def verificar_celular(request):
    pendiente = _get_pendiente(request)
    if pendiente is None:
        messages.error(
            request,
            "El registro venció o no existe. Vuelve a empezar.",
        )
        return redirect("postulantes:registro")

    if request.method == "POST":
        form = VerificarCodigoForm(request.POST)
        if form.is_valid():
            try:
                user = VerificarRegistroPostulante().execute(
                    VerificarRegistroPostulanteInput(
                        pendiente_id=str(pendiente.pk),
                        codigo=form.cleaned_data["codigo"],
                        ip=_ip(request),
                    )
                )
            except DomainError as exc:
                form.add_error(None, exc.message)
            except IntegrityError:
                form.add_error(
                    None,
                    "No se pudo completar el registro. Intenta nuevamente.",
                )
            else:
                _limpiar_sesion(request)
                auth_login(
                    request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                messages.success(
                    request,
                    "Tu celular fue verificado correctamente.",
                )
                return redirect("home")
    else:
        form = VerificarCodigoForm()

    estado = otp.estado_reenvio(pendiente=pendiente, proposito=PROPOSITO)
    contexto = _contexto_verificacion(request, pendiente, form, estado)
    return render(request, "postulantes/verificar_celular.html", contexto)


@require_POST
def reenviar_codigo(request):
    pendiente = _get_pendiente(request)
    if pendiente is None:
        messages.error(
            request,
            "El registro venció o no existe. Vuelve a empezar.",
        )
        return redirect("postulantes:registro")

    try:
        codigo = otp.crear_y_enviar(
            pendiente=pendiente,
            proposito=PROPOSITO,
            ip=_ip(request),
        )
    except DomainError as exc:
        messages.error(request, exc.message)
    else:
        if settings.DEMO_MODE:
            request.session[DEMO_OTP_KEY] = codigo
        messages.success(request, "Enviamos un nuevo código a tu celular.")

    return redirect("postulantes:verificar_celular")


def cambiar_celular(request):
    pendiente = _get_pendiente(request)
    if pendiente is None:
        messages.error(
            request,
            "El registro venció o no existe. Vuelve a empezar.",
        )
        return redirect("postulantes:registro")

    if request.method == "POST":
        form = CambiarCelularForm(request.POST, pendiente=pendiente)
        if form.is_valid():
            try:
                pendiente, codigo = CambiarCelularPendiente().execute(
                    CambiarCelularPendienteInput(
                        pendiente_id=str(pendiente.pk),
                        celular=form.cleaned_data["celular"],
                        ip=_ip(request),
                    )
                )
            except DomainError as exc:
                form.add_error("celular", exc.message)
            except IntegrityError:
                form.add_error(
                    None,
                    "No se pudo actualizar el celular. Intenta nuevamente.",
                )
            else:
                if settings.DEMO_MODE:
                    request.session[DEMO_OTP_KEY] = codigo
                messages.success(
                    request,
                    "Actualizamos tu celular. Enviamos un nuevo código.",
                )
                return redirect("postulantes:verificar_celular")
    else:
        form = CambiarCelularForm(pendiente=pendiente)

    return render(
        request,
        "postulantes/cambiar_celular.html",
        {"form": form, "celular": pendiente.celular},
    )


# ── Perfil del postulante ────────────────────────────────────────────────

def _perfil_actual(request):
    perfil = getattr(request.user, "postulante_profile", None)
    if perfil is None:
        messages.error(request, "Tu cuenta no tiene un perfil de postulante.")
    return perfil


def _contexto_perfil(perfil, **form_overrides) -> dict:
    forms = {
        "datos_form": DatosPersonalesForm(instance=perfil),
        "formacion_form": FormacionForm(),
        "experiencia_form": ExperienciaForm(),
        "habilidad_form": HabilidadForm(),
        "idioma_form": IdiomaForm(),
        "cv_form": CVForm(),
    }
    forms.update(form_overrides)

    return {
        "perfil": perfil,
        "completitud": calcular_completitud(perfil),
        "formaciones": perfil.formaciones.all(),
        "experiencias": perfil.experiencias.all(),
        "habilidades": perfil.habilidades.select_related("habilidad"),
        "idiomas": perfil.idiomas.select_related("idioma"),
        "habilidades_sugeridas": Habilidad.objects.values_list("nombre", flat=True),
        "idiomas_sugeridos": Idioma.objects.values_list("nombre", flat=True),
        "puede_eliminar_formacion": perfil.formaciones.count() > 1,
        "puede_eliminar_experiencia": perfil.experiencias.count() > 1,
        "puede_eliminar_habilidad": perfil.habilidades.count() > MIN_HABILIDADES,
        "puede_eliminar_idioma": perfil.idiomas.count() > 1,
        **forms,
    }


def _respuesta_perfil(request, perfil, mensaje: str, nivel: str = "success"):
    """Responde a HTMX sin recargar; si no, redirect clásico."""
    if request.headers.get("HX-Request"):
        response = render(
            request,
            "postulantes/perfil.html",
            _contexto_perfil(perfil),
        )
        completitud = calcular_completitud(perfil)
        response["HX-Trigger"] = json.dumps(
            {
                "perfilActualizado": {
                    "porcentaje": completitud["porcentaje"],
                    "puede_postular": completitud["puede_postular"],
                    "faltantes": completitud["faltantes"],
                    "titulo_principal": (
                        perfil.formaciones.first().titulo
                        if perfil.formaciones.exists()
                        else "Postulante"
                    ),
                    "secciones": [
                        {
                            "clave": seccion["clave"],
                            "completa": seccion["completa"],
                            "peso": seccion["peso"],
                            "faltantes": seccion["faltantes"],
                        }
                        for seccion in completitud["secciones"]
                    ],
                    "mensaje": mensaje,
                    "nivel": nivel,
                }
            }
        )
        return response

    getattr(messages, nivel)(request, mensaje)
    return redirect("postulantes:perfil")


@role_required(Role.Code.POSTULANTE)
def perfil(request):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")
    return render(request, "postulantes/perfil.html", _contexto_perfil(perfil))


@role_required(Role.Code.POSTULANTE)
@require_POST
def perfil_datos(request):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    form = DatosPersonalesForm(request.POST, request.FILES, instance=perfil)
    if form.is_valid():
        nueva_foto = form.cleaned_data.get("foto")
        if (
            nueva_foto
            and perfil.foto
            and perfil.foto.name != getattr(nueva_foto, "name", None)
        ):
            perfil.foto.delete(save=False)
        form.save()
        return _respuesta_perfil(request, perfil, "Datos personales actualizados.")

    return render(
        request,
        "postulantes/perfil.html",
        _contexto_perfil(perfil, datos_form=form),
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def perfil_cv(request):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    form = CVForm(request.POST, request.FILES)
    if form.is_valid():
        if perfil.cv:
            perfil.cv.delete(save=False)
        perfil.cv = form.cleaned_data["cv"]
        perfil.save(update_fields=["cv"])
        return _respuesta_perfil(request, perfil, "CV actualizado.")

    return render(
        request,
        "postulantes/perfil.html",
        _contexto_perfil(perfil, cv_form=form),
    )


@role_required(Role.Code.POSTULANTE)
def perfil_cv_descargar(request):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")
    if not perfil.cv:
        raise Http404("El postulante no tiene CV.")

    return FileResponse(
        perfil.cv.open("rb"),
        as_attachment=True,
        filename=Path(perfil.cv.name).name,
        content_type="application/pdf",
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def formacion_agregar(request):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    form = FormacionForm(request.POST)
    if form.is_valid():
        formacion = form.save(commit=False)
        formacion.profile = perfil
        formacion.save()
        return _respuesta_perfil(
            request, perfil, "Formación académica agregada."
        )

    return render(
        request,
        "postulantes/perfil.html",
        _contexto_perfil(perfil, formacion_form=form),
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def formacion_eliminar(request, pk):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    formacion = get_object_or_404(Formacion, pk=pk, profile=perfil)
    if perfil.formaciones.count() <= 1:
        return _respuesta_perfil(
            request,
            perfil,
            "Debe quedar al menos una formación académica.",
            nivel="error",
        )

    formacion.delete()
    return _respuesta_perfil(
        request, perfil, "Formación académica eliminada.", nivel="info"
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def experiencia_agregar(request):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    form = ExperienciaForm(request.POST)
    if form.is_valid():
        experiencia = form.save(commit=False)
        experiencia.profile = perfil
        experiencia.save()
        return _respuesta_perfil(
            request, perfil, "Experiencia laboral agregada."
        )

    return render(
        request,
        "postulantes/perfil.html",
        _contexto_perfil(perfil, experiencia_form=form),
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def experiencia_eliminar(request, pk):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    experiencia = get_object_or_404(Experiencia, pk=pk, profile=perfil)
    if perfil.experiencias.count() <= 1:
        return _respuesta_perfil(
            request,
            perfil,
            "Debe quedar al menos una experiencia laboral.",
            nivel="error",
        )

    experiencia.delete()
    return _respuesta_perfil(
        request, perfil, "Experiencia laboral eliminada.", nivel="info"
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def habilidad_agregar(request):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    form = HabilidadForm(request.POST)
    if form.is_valid():
        nombre = " ".join(form.cleaned_data["nombre"].split())
        habilidad = Habilidad.objects.filter(nombre__iexact=nombre).first()
        if habilidad is None:
            habilidad = Habilidad.objects.create(nombre=nombre)

        PostulanteHabilidad.objects.update_or_create(
            profile=perfil,
            habilidad=habilidad,
            defaults={"nivel": form.cleaned_data["nivel"]},
        )
        return _respuesta_perfil(request, perfil, "Habilidad guardada.")

    return render(
        request,
        "postulantes/perfil.html",
        _contexto_perfil(perfil, habilidad_form=form),
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def habilidad_eliminar(request, pk):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    habilidad = get_object_or_404(PostulanteHabilidad, pk=pk, profile=perfil)
    if perfil.habilidades.count() <= MIN_HABILIDADES:
        return _respuesta_perfil(
            request,
            perfil,
            f"Debés mantener al menos {MIN_HABILIDADES} habilidades.",
            nivel="error",
        )

    habilidad.delete()
    return _respuesta_perfil(request, perfil, "Habilidad eliminada.", nivel="info")


@role_required(Role.Code.POSTULANTE)
@require_POST
def idioma_agregar(request):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    form = IdiomaForm(request.POST)
    if form.is_valid():
        nombre = " ".join(form.cleaned_data["nombre"].split())
        idioma = Idioma.objects.filter(nombre__iexact=nombre).first()
        if idioma is None:
            idioma = Idioma.objects.create(nombre=nombre)

        PostulanteIdioma.objects.update_or_create(
            profile=perfil,
            idioma=idioma,
            defaults={"nivel": form.cleaned_data["nivel"]},
        )
        return _respuesta_perfil(request, perfil, "Idioma guardado.")

    return render(
        request,
        "postulantes/perfil.html",
        _contexto_perfil(perfil, idioma_form=form),
    )


@role_required(Role.Code.POSTULANTE)
@require_POST
def idioma_eliminar(request, pk):
    perfil = _perfil_actual(request)
    if perfil is None:
        return redirect("dashboard:postulante")

    idioma = get_object_or_404(PostulanteIdioma, pk=pk, profile=perfil)
    if perfil.idiomas.count() <= 1:
        return _respuesta_perfil(
            request,
            perfil,
            "Debe quedar al menos un idioma para no bajar tu porcentaje.",
            nivel="error",
        )

    idioma.delete()
    return _respuesta_perfil(request, perfil, "Idioma eliminado.", nivel="info")
