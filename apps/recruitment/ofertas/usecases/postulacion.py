from __future__ import annotations

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.recruitment.ofertas.models import Postulacion
from core.exceptions import DomainError

ORDEN_ESTADOS = [
    Postulacion.Estado.POSTULADO,
    Postulacion.Estado.VISTO,
    Postulacion.Estado.PRESELECCIONADO,
    Postulacion.Estado.ENTREVISTA,
    Postulacion.Estado.FINALISTA,
    Postulacion.Estado.CONTRATADO,
]

TERMINALES = {
    Postulacion.Estado.CONTRATADO,
    Postulacion.Estado.RECHAZADO,
}


def postularse(oferta, postulante, completitud: dict) -> Postulacion:
    if not completitud.get("puede_postular"):
        raise DomainError(
            "Necesitás un perfil mayor al 80 % y tu CV cargado para postular.",
            code="PERFIL_INCOMPLETO",
        )
    if oferta.estado != oferta.Estado.PUBLICADA:
        raise DomainError(
            "Esta oferta no está recibiendo postulaciones.",
            code="OFERTA_NO_DISPONIBLE",
        )
    if oferta.fecha_cierre < timezone.localdate():
        raise DomainError(
            "Esta oferta ya cerró sus postulaciones.",
            code="OFERTA_VENCIDA",
        )

    try:
        with transaction.atomic():
            return Postulacion.objects.create(
                oferta=oferta,
                postulante=postulante,
            )
    except IntegrityError as exc:
        raise DomainError(
            "Ya postulaste a esta oferta.",
            code="YA_POSTULO",
        ) from exc


def marcar_visto(postulacion: Postulacion) -> Postulacion:
    if postulacion.estado == Postulacion.Estado.POSTULADO:
        postulacion.estado = Postulacion.Estado.VISTO
        postulacion.visto_en = timezone.now()
        postulacion.save(
            update_fields=["estado", "visto_en", "actualizado_en"]
        )
    return postulacion


def estados_siguientes(estado: str) -> list[str]:
    if estado in TERMINALES:
        return []

    permitidos = set(ORDEN_ESTADOS)
    permitidos.add(Postulacion.Estado.RECHAZADO)

    if estado == Postulacion.Estado.POSTULADO:
        permitidos.discard(Postulacion.Estado.POSTULADO)
        return [e for e in ORDEN_ESTADOS if e in permitidos] + [
            Postulacion.Estado.RECHAZADO
        ]

    if estado in ORDEN_ESTADOS:
        indice = ORDEN_ESTADOS.index(estado)
        permitidos = set(ORDEN_ESTADOS[indice + 1 :])
        permitidos.add(Postulacion.Estado.RECHAZADO)
        return [
            e
            for e in ORDEN_ESTADOS
            if e in permitidos
        ] + [Postulacion.Estado.RECHAZADO]

    return []


def cambiar_estado(postulacion: Postulacion, nuevo_estado: str) -> Postulacion:
    if nuevo_estado not in estados_siguientes(postulacion.estado):
        raise ValueError("Ese cambio de estado no está permitido.")

    postulacion.estado = nuevo_estado
    if nuevo_estado == Postulacion.Estado.VISTO and not postulacion.visto_en:
        postulacion.visto_en = timezone.now()
    postulacion.save(
        update_fields=["estado", "visto_en", "actualizado_en"]
    )
    return postulacion


def retirar_postulacion(postulacion: Postulacion) -> None:
    if postulacion.visto_en is not None:
        raise DomainError(
            "La empresa ya vio tu postulación; no podés retirarla.",
            code="POSTULACION_VISTA",
        )
    if postulacion.estado != Postulacion.Estado.POSTULADO:
        raise DomainError(
            "Solo podés retirar una postulación que todavía no fue vista.",
            code="POSTULACION_NO_RETIRABLE",
        )
    postulacion.delete()
