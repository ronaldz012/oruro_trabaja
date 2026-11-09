from __future__ import annotations

from django.utils import timezone

from apps.recruitment.empresas.models import Empresa
from core.exceptions import DomainError


class CambiarEstadoEmpresa:
    """Aprobación, rechazo y suspensión por parte de GADOR."""

    def execute(
        self,
        empresa: Empresa,
        *,
        accion: str,
        actor,
        motivo: str = "",
    ) -> Empresa:
        accion = accion.strip().lower()

        if accion == "aprobar":
            empresa.estado = Empresa.Estado.APROBADA
            empresa.motivo_rechazo = ""
        elif accion == "rechazar":
            if not motivo.strip():
                raise DomainError(
                    "Debes indicar el motivo del rechazo.",
                    code="MOTIVO_REQUERIDO",
                )
            empresa.estado = Empresa.Estado.RECHAZADA
            empresa.motivo_rechazo = motivo.strip()
        elif accion == "suspender":
            empresa.estado = Empresa.Estado.SUSPENDIDA
        else:
            raise DomainError("Acción inválida.", code="ACCION_INVALIDA")

        empresa.revisada_por = actor
        empresa.revisada_en = timezone.now()
        empresa.save(
            update_fields=[
                "estado",
                "motivo_rechazo",
                "revisada_por",
                "revisada_en",
                "actualizado_en",
            ]
        )
        return empresa
