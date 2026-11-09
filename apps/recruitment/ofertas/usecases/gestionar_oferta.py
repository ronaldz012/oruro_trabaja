from __future__ import annotations

from django.utils import timezone

from apps.recruitment.ofertas.models import Oferta


def _validar_en_revision(oferta: Oferta) -> None:
    if oferta.estado != Oferta.Estado.EN_REVISION_GADOR:
        raise ValueError("La oferta no está en revisión por GADOR.")


def aprobar_oferta(oferta: Oferta, *, actor) -> Oferta:
    _validar_en_revision(oferta)
    oferta.estado = Oferta.Estado.PUBLICADA
    oferta.publicada_en = timezone.now()
    oferta.motivo_revision = ""
    oferta.revisada_por = actor
    oferta.revisada_en = timezone.now()
    oferta.save(
        update_fields=[
            "estado",
            "publicada_en",
            "motivo_revision",
            "revisada_por",
            "revisada_en",
            "actualizado_en",
        ]
    )
    return oferta


def devolver_oferta(oferta: Oferta, *, actor, motivo: str) -> Oferta:
    _validar_en_revision(oferta)
    if not motivo.strip():
        raise ValueError("Debes indicar el motivo de la devolución.")

    oferta.estado = Oferta.Estado.BORRADOR
    oferta.motivo_revision = motivo.strip()
    oferta.revisada_por = actor
    oferta.revisada_en = timezone.now()
    oferta.save(
        update_fields=[
            "estado",
            "motivo_revision",
            "revisada_por",
            "revisada_en",
            "actualizado_en",
        ]
    )
    return oferta


def iniciar_seleccion(oferta: Oferta) -> Oferta:
    if oferta.estado != Oferta.Estado.PUBLICADA:
        raise ValueError("Solo se inicia selección desde una oferta publicada.")
    oferta.estado = Oferta.Estado.EN_PROCESO_SELECCION
    oferta.save(update_fields=["estado", "actualizado_en"])
    return oferta


def cerrar_oferta(oferta: Oferta) -> Oferta:
    if oferta.estado not in {
        Oferta.Estado.PUBLICADA,
        Oferta.Estado.EN_PROCESO_SELECCION,
    }:
        raise ValueError("Solo se cierran ofertas publicadas o en selección.")
    oferta.estado = Oferta.Estado.CERRADA
    oferta.save(update_fields=["estado", "actualizado_en"])
    return oferta


def anular_oferta(oferta: Oferta) -> Oferta:
    if oferta.estado in {Oferta.Estado.CERRADA, Oferta.Estado.ANULADA}:
        raise ValueError("La oferta ya está cerrada o anulada.")
    oferta.estado = Oferta.Estado.ANULADA
    oferta.save(update_fields=["estado", "actualizado_en"])
    return oferta
