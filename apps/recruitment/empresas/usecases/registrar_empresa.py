from __future__ import annotations

from dataclasses import dataclass

from django.db import transaction

from apps.platform.accounts.models import Role
from apps.platform.accounts.usecases.crear_usuario import (
    CrearUsuario,
    CrearUsuarioInput,
)
from apps.recruitment.catalogos.models import Rubro
from apps.recruitment.empresas.models import Empresa
from apps.recruitment.empresas.normalizers import normalizar_celular, normalizar_nit
from core.exceptions import DomainError


@dataclass(frozen=True)
class RegistrarEmpresaInput:
    email: str
    password: str
    nit: str
    razon_social: str
    rubro: Rubro
    representante_nombres: str
    representante_apellidos: str
    representante_ci: str
    celular: str
    direccion: str
    logo: object | None = None
    descripcion: str = ""


class RegistrarEmpresa:
    """Crea la cuenta y el perfil de empresa en estado pendiente."""

    @transaction.atomic
    def execute(self, data: RegistrarEmpresaInput):
        nit = normalizar_nit(data.nit)
        celular = normalizar_celular(data.celular)
        email = data.email.strip().lower()

        if Empresa.objects.filter(nit=nit).exists():
            raise DomainError(
                "Ya existe una empresa con ese NIT. "
                "Si crees que es un error, contacta a GADOR.",
                code="NIT_TAKEN",
            )

        user = CrearUsuario().execute(
            CrearUsuarioInput(
                email=email,
                password=data.password,
                role_code=Role.Code.EMPRESA,
                celular=celular,
                first_name=data.representante_nombres.strip(),
                last_name=data.representante_apellidos.strip(),
                is_active=True,
                celular_verificado=False,
            )
        )

        empresa = Empresa.objects.create(
            user=user,
            nit=nit,
            razon_social=data.razon_social.strip(),
            rubro=data.rubro,
            representante_nombres=data.representante_nombres.strip(),
            representante_apellidos=data.representante_apellidos.strip(),
            representante_ci=data.representante_ci,
            direccion=data.direccion.strip(),
            logo=data.logo,
            descripcion=data.descripcion.strip(),
        )
        return user, empresa
