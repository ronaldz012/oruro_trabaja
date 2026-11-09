from django.core.management.base import BaseCommand

from apps.recruitment.catalogos.models import (
    Departamento,
    Habilidad,
    Idioma,
    Modalidad,
    Profesion,
    Rubro,
    TipoContrato,
)

PROFESIONES = [
    "Ingeniero de Sistemas",
    "Ingeniero Informático",
    "Ingeniero de Software",
    "Técnico Superior en Sistemas Informáticos",
    "Analista de Sistemas",
    "Ingeniero Civil",
    "Arquitecto",
    "Técnico en Construcción",
    "Electricista",
    "Plomero",
    "Soldador",
    "Mecánico",
    "Chofer",
    "Médico",
    "Enfermero",
    "Odontólogo",
    "Nutricionista",
    "Psicólogo",
    "Fisioterapeuta",
    "Veterinario",
    "Docente",
    "Educador",
    "Contador Público",
    "Auditor",
    "Administrador de Empresas",
    "Abogado",
    "Comunicador Social",
    "Diseñador Gráfico",
    "Especialista en Marketing",
    "Especialista en Recursos Humanos",
    "Secretaria",
    "Atención al cliente",
    "Chef",
    "Cocinero",
    "Panadero",
    "Comerciante",
    "Vendedor",
    "Cajero",
    "Agricultor",
    "Ganadero",
    "Minero",
    "Personal de seguridad",
    "Personal de limpieza",
    "Otro",
]

HABILIDADES = [
    # Tecnología
    "Python",
    "Django",
    "Laravel",
    "JavaScript",
    "React",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "Redes",
    "Soporte técnico",
    "Mantenimiento de computadoras",
    "Análisis de datos",
    "Excel",
    "Word",
    "PowerPoint",
    "Google Workspace",
    # Oficina y administración
    "Atención al cliente",
    "Ventas",
    "Cajero",
    "Contabilidad",
    "Facturación",
    "Archivo",
    "Gestión de proyectos",
    "Recursos Humanos",
    "Liderazgo",
    "Trabajo en equipo",
    "Comunicación",
    "Organización",
    "Redacción",
    # Oficios y servicios
    "Electricidad",
    "Plomería",
    "Soldadura",
    "Carpintería",
    "Albañilería",
    "Mecánica automotriz",
    "Conducción de vehículos",
    "Cocina",
    "Panadería",
    "Repostería",
    "Peluquería",
    "Costura",
    # Salud y educación
    "Primeros auxilios",
    "Enfermería",
    "Farmacología",
    "Cuidado de personas",
    "Docencia",
    "Planificación de clases",
    # Otros
    "Idiomas",
    "Investigación",
    "Fotografía",
    "Diseño gráfico",
    "Redes sociales",
    "Marketing digital",
]

IDIOMAS = [
    "Español",
    "Inglés",
    "Quechua",
    "Aymara",
    "Portugués",
    "Francés",
    "Alemán",
    "Italiano",
    "Chino Mandarín",
    "Japonés",
]

RUBROS = [
    "Minería",
    "Tecnología",
    "Comercio",
    "Salud",
    "Educación",
    "Construcción",
    "Gastronomía",
    "Transporte",
    "Servicios",
    "Industria",
    "Agricultura",
    "Turismo",
    "Banca y finanzas",
    "Comunicación",
    "Otro",
]

TIPOS_CONTRATO = [
    "Indefinido",
    "Plazo fijo",
    "Pasantía",
    "Consultoría",
]

MODALIDADES = [
    "Presencial",
    "Remoto",
    "Híbrido",
]

DEPARTAMENTOS = [
    "La Paz",
    "Cochabamba",
    "Santa Cruz",
    "Oruro",
    "Potosí",
    "Chuquisaca",
    "Tarija",
    "Beni",
    "Pando",
]


class Command(BaseCommand):
    help = "Carga profesiones, habilidades e idiomas base para desarrollo."

    def handle(self, *args, **options):
        for nombre in PROFESIONES:
            Profesion.objects.get_or_create(nombre=nombre)
        for nombre in HABILIDADES:
            Habilidad.objects.get_or_create(nombre=nombre)
        for nombre in IDIOMAS:
            Idioma.objects.get_or_create(nombre=nombre)
        for nombre in RUBROS:
            Rubro.objects.get_or_create(nombre=nombre)
        for nombre in TIPOS_CONTRATO:
            TipoContrato.objects.get_or_create(nombre=nombre)
        for nombre in MODALIDADES:
            Modalidad.objects.get_or_create(nombre=nombre)
        for nombre in DEPARTAMENTOS:
            Departamento.objects.get_or_create(nombre=nombre)

        self.stdout.write(
            self.style.SUCCESS(
                "Catálogos cargados: "
                f"{Profesion.objects.count()} profesiones, "
                f"{Habilidad.objects.count()} habilidades, "
                f"{Idioma.objects.count()} idiomas, "
                f"{Rubro.objects.count()} rubros, "
                f"{TipoContrato.objects.count()} tipos de contrato, "
                f"{Modalidad.objects.count()} modalidades, "
                f"{Departamento.objects.count()} departamentos."
            )
        )
