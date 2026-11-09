from __future__ import annotations

PESOS = {
    "datos": 10,
    "formacion": 20,
    "experiencia": 20,
    "habilidades": 20,
    "cv": 25,
    "idiomas": 5,
}

MIN_HABILIDADES = 3
UMBRAL_POSTULACION = 80


def calcular_completitud(profile) -> dict:
    """Calcula el porcentaje del perfil y qué le falta al postulante.

    El CV es obligatorio: sin él el perfil no puede superar el 80 %.
    Los idiomas siguen siendo un extra.
    """
    if profile is None:
        secciones = [
            {"clave": clave, "nombre": nombre, "peso": peso, "completa": False, "faltantes": ["Completa tu perfil."]}
            for clave, (nombre, peso) in _SECCIONES.items()
        ]
        return {
            "porcentaje": 0,
            "puede_postular": False,
            "secciones": secciones,
            "faltantes": ["Completa tu perfil."],
        }

    faltantes_datos = []
    if not profile.foto:
        faltantes_datos.append("Foto de perfil")
    if not profile.direccion:
        faltantes_datos.append("Dirección")
    if not profile.fecha_nacimiento:
        faltantes_datos.append("Fecha de nacimiento")

    formaciones = profile.formaciones.exists()
    experiencias = profile.experiencias.exists()
    cantidad_habilidades = profile.habilidades.count()
    tiene_cv = bool(profile.cv)
    idiomas = profile.idiomas.exists()

    faltantes_habilidades = []
    if cantidad_habilidades < MIN_HABILIDADES:
        restantes = MIN_HABILIDADES - cantidad_habilidades
        faltantes_habilidades.append(
            f"Agrega {restantes} habilidad{'es' if restantes != 1 else ''} más."
        )

    secciones = [
        {
            "clave": "datos",
            "nombre": _SECCIONES["datos"][0],
            "peso": PESOS["datos"],
            "completa": not faltantes_datos,
            "faltantes": faltantes_datos,
        },
        {
            "clave": "formacion",
            "nombre": _SECCIONES["formacion"][0],
            "peso": PESOS["formacion"],
            "completa": formaciones,
            "faltantes": [] if formaciones else ["Agrega al menos una formación académica."],
        },
        {
            "clave": "experiencia",
            "nombre": _SECCIONES["experiencia"][0],
            "peso": PESOS["experiencia"],
            "completa": experiencias,
            "faltantes": [] if experiencias else ["Agrega al menos una experiencia laboral."],
        },
        {
            "clave": "habilidades",
            "nombre": _SECCIONES["habilidades"][0],
            "peso": PESOS["habilidades"],
            "completa": cantidad_habilidades >= MIN_HABILIDADES,
            "faltantes": faltantes_habilidades,
        },
        {
            "clave": "cv",
            "nombre": _SECCIONES["cv"][0],
            "peso": PESOS["cv"],
            "completa": tiene_cv,
            "faltantes": [] if tiene_cv else ["Sube tu CV en PDF (obligatorio para postular)."],
        },
        {
            "clave": "idiomas",
            "nombre": _SECCIONES["idiomas"][0],
            "peso": PESOS["idiomas"],
            "completa": idiomas,
            "faltantes": [] if idiomas else ["Agrega al menos un idioma."],
        },
    ]

    porcentaje = sum(s["peso"] for s in secciones if s["completa"])
    pendientes = [s["nombre"] for s in secciones if not s["completa"]]

    return {
        "porcentaje": porcentaje,
        "puede_postular": porcentaje > UMBRAL_POSTULACION,
        "secciones": secciones,
        "por_clave": {s["clave"]: s for s in secciones},
        "faltantes": pendientes,
    }


_SECCIONES = {
    "datos": ("Datos personales", PESOS["datos"]),
    "formacion": ("Formación académica", PESOS["formacion"]),
    "experiencia": ("Experiencia laboral", PESOS["experiencia"]),
    "habilidades": ("Habilidades", PESOS["habilidades"]),
    "cv": ("CV en PDF", PESOS["cv"]),
    "idiomas": ("Idiomas", PESOS["idiomas"]),
}
