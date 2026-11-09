from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.recruitment.catalogos.models import (
    Departamento,
    Habilidad,
    Modalidad,
    Profesion,
    TipoContrato,
)
from apps.recruitment.empresas.models import Empresa
from apps.recruitment.ofertas.models import Oferta, OfertaHabilidad


class Command(BaseCommand):
    help = "Crea ofertas de ejemplo: publicada, en revisión y borrador."

    def handle(self, *args, **options):
        empresa = Empresa.objects.filter(estado=Empresa.Estado.APROBADA).first()
        if empresa is None:
            self.stdout.write(self.style.ERROR("No hay empresa aprobada. Corre seed_empresas."))
            return

        tipo = TipoContrato.objects.get_or_create(nombre="Indefinido")[0]
        modalidad = Modalidad.objects.get_or_create(nombre="Híbrido")[0]
        departamento = Departamento.objects.get_or_create(nombre="Oruro")[0]
        profesion = Profesion.objects.get_or_create(nombre="Ingeniero de Sistemas")[0]
        habilidades = [
            Habilidad.objects.get_or_create(nombre=nombre)[0]
            for nombre in ("Python", "SQL", "Django", "Análisis de datos")
        ]

        publicada, _ = Oferta.objects.update_or_create(
            empresa=empresa,
            titulo="Desarrollador Full Stack",
            defaults={
                "descripcion": "Desarrollo de aplicaciones web para la plataforma de la Gobernación.",
                "requisitos_obligatorios": "Experiencia en Python, SQL y desarrollo web.",
                "requisitos_deseables": "Conocimientos de Django y Docker.",
                "anos_experiencia": 2,
                "tipo_contrato": tipo,
                "modalidad": modalidad,
                "departamento": departamento,
                "municipio": "Oruro",
                "salario_min": 6000,
                "salario_max": 9000,
                "a_tratar": False,
                "beneficios": "Seguro de salud y capacitación.",
                "fecha_cierre": timezone.localdate() + timedelta(days=30),
                "plazas": 2,
                "estado": Oferta.Estado.PUBLICADA,
                "publicada_en": timezone.now(),
            },
        )
        publicada.profesiones.set([profesion])
        self._habilidades(publicada, habilidades[:3], habilidades[3:])

        revision, _ = Oferta.objects.update_or_create(
            empresa=empresa,
            titulo="Analista de Datos",
            defaults={
                "descripcion": "Análisis de información para la toma de decisiones.",
                "requisitos_obligatorios": "Manejo de SQL y Excel avanzado.",
                "requisitos_deseables": "Python para análisis de datos.",
                "anos_experiencia": 1,
                "tipo_contrato": tipo,
                "modalidad": modalidad,
                "departamento": departamento,
                "municipio": "Oruro",
                "salario_min": 4500,
                "salario_max": 6500,
                "a_tratar": False,
                "fecha_cierre": timezone.localdate() + timedelta(days=20),
                "plazas": 1,
                "estado": Oferta.Estado.EN_REVISION_GADOR,
            },
        )
        revision.profesiones.set([profesion])
        self._habilidades(revision, habilidades[1:3], habilidades[3:])

        borrador, _ = Oferta.objects.update_or_create(
            empresa=empresa,
            titulo="Pasante de Soporte Técnico",
            defaults={
                "descripcion": "Apoyo en soporte técnico y mantenimiento de equipos.",
                "requisitos_obligatorios": "Conocimientos básicos de redes y hardware.",
                "requisitos_deseables": "Excel y atención al cliente.",
                "anos_experiencia": 0,
                "tipo_contrato": tipo,
                "modalidad": modalidad,
                "departamento": departamento,
                "municipio": "Oruro",
                "salario_min": None,
                "salario_max": None,
                "a_tratar": True,
                "fecha_cierre": timezone.localdate() + timedelta(days=15),
                "plazas": 1,
                "estado": Oferta.Estado.BORRADOR,
            },
        )
        borrador.profesiones.set([profesion])
        self._habilidades(borrador, [], habilidades[3:])

        self.stdout.write(self.style.SUCCESS("Ofertas seed creadas: 1 publicada, 1 en revisión, 1 borrador."))

    def _habilidades(self, oferta, obligatorias, deseables):
        oferta.requerimientos_habilidad.all().delete()
        OfertaHabilidad.objects.bulk_create(
            [
                OfertaHabilidad(oferta=oferta, habilidad=h, obligatoria=True)
                for h in obligatorias
            ]
            + [
                OfertaHabilidad(oferta=oferta, habilidad=h, obligatoria=False)
                for h in deseables
            ]
        )
