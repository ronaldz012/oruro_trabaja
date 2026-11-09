from __future__ import annotations

from django.shortcuts import render

from apps.platform.accounts.models import Role
from apps.recruitment.catalogos.models import (
    Departamento,
    Habilidad,
    Idioma,
    Modalidad,
    Profesion,
    Rubro,
    TipoContrato,
)
from core.pagination import paginar
from core.permissions import role_required

CATALOGOS = [
    {
        "codigo": "rubros",
        "nombre": "Rubros",
        "singular": "Rubro",
        "modelo": Rubro,
    },
    {
        "codigo": "profesiones",
        "nombre": "Profesiones",
        "singular": "Profesión",
        "modelo": Profesion,
    },
    {
        "codigo": "habilidades",
        "nombre": "Habilidades",
        "singular": "Habilidad",
        "modelo": Habilidad,
    },
    {
        "codigo": "idiomas",
        "nombre": "Idiomas",
        "singular": "Idioma",
        "modelo": Idioma,
    },
    {
        "codigo": "tipos-contrato",
        "nombre": "Tipos de contrato",
        "singular": "Tipo de contrato",
        "modelo": TipoContrato,
    },
    {
        "codigo": "modalidades",
        "nombre": "Modalidades",
        "singular": "Modalidad",
        "modelo": Modalidad,
    },
    {
        "codigo": "departamentos",
        "nombre": "Departamentos",
        "singular": "Departamento",
        "modelo": Departamento,
    },
]


@role_required(Role.Code.SUPERADMIN)
def gador_lista(request):
    tipo = request.GET.get("tipo") or "rubros"
    catalogo_actual = next(
        (catalogo for catalogo in CATALOGOS if catalogo["codigo"] == tipo),
        None,
    )
    if catalogo_actual is None:
        tipo = "rubros"
        catalogo_actual = CATALOGOS[0]

    registros = catalogo_actual["modelo"].objects.all()
    page_obj = paginar(request, registros, 20)

    conteos = {
        catalogo["codigo"]: catalogo["modelo"].objects.count()
        for catalogo in CATALOGOS
    }

    contexto = {
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "catalogos": [
            {
                "codigo": catalogo["codigo"],
                "nombre": catalogo["nombre"],
                "total": conteos[catalogo["codigo"]],
            }
            for catalogo in CATALOGOS
        ],
        "catalogo_actual": catalogo_actual,
        "tipo_actual": tipo,
        "total_registros": page_obj.paginator.count,
    }
    return render(request, "catalogos/gador_lista.html", contexto)
