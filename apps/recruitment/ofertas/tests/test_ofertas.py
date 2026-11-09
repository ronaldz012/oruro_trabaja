from __future__ import annotations

from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.platform.accounts.models import Role, User
from apps.recruitment.catalogos.models import (
    Departamento,
    Habilidad,
    Modalidad,
    Profesion,
    Rubro,
    TipoContrato,
)
from apps.recruitment.empresas.models import Empresa
from apps.recruitment.ofertas.models import Oferta


def crear_empresa(
    *,
    estado=Empresa.Estado.APROBADA,
    email="empresa@example.com",
    nit="4000001",
    celular="+59170004001",
):
    role = Role.objects.get(codigo=Role.Code.EMPRESA)
    rubro = Rubro.objects.get_or_create(nombre="Tecnología")[0]
    user = User.objects.create_user(
        email=email,
        password="ClaveSegura123!",
        role=role,
        celular=celular,
        first_name="Empresa",
        last_name="Test",
    )
    empresa = Empresa.objects.create(
        user=user,
        nit=nit,
        razon_social=f"Empresa {nit}",
        rubro=rubro,
        representante_nombres="Ana",
        representante_apellidos="Test",
        representante_ci="1111111 LP",
        direccion="Calle 123",
        estado=estado,
    )
    return user, empresa


class OfertasTestsBase(TestCase):
    def setUp(self):
        self.tipo = TipoContrato.objects.get_or_create(nombre="Tiempo completo")[0]
        self.modalidad = Modalidad.objects.get_or_create(nombre="Híbrido")[0]
        self.departamento = Departamento.objects.get_or_create(nombre="Oruro")[0]
        self.profesion = Profesion.objects.get_or_create(nombre="Ingeniero de Sistemas")[0]
        self.habilidad_1 = Habilidad.objects.get_or_create(nombre="Python")[0]
        self.habilidad_2 = Habilidad.objects.get_or_create(nombre="SQL")[0]
        self.habilidad_3 = Habilidad.objects.get_or_create(nombre="Django")[0]

        self.empresa_user, self.empresa = crear_empresa()
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.SUPERADMIN),
        )

    def datos_oferta(self, **overrides):
        datos = {
            "titulo": "Desarrollador Full Stack",
            "descripcion": "Desarrollo de aplicaciones web.",
            "requisitos_obligatorios": "Python y SQL.",
            "requisitos_deseables": "Django.",
            "profesiones": [self.profesion.pk],
            "anos_experiencia": 2,
            "tipo_contrato": self.tipo.pk,
            "modalidad": self.modalidad.pk,
            "departamento": self.departamento.pk,
            "municipio": "Oruro",
            "salario_min": "5000",
            "salario_max": "8000",
            "beneficios": "Capacitación",
            "fecha_cierre": (timezone.localdate() + timedelta(days=20)).isoformat(),
            "plazas": 2,
            "habilidades_obligatorias": [self.habilidad_1.pk, self.habilidad_2.pk],
            "habilidades_deseables": [self.habilidad_3.pk],
        }
        datos.update(overrides)
        return datos

    def crear_oferta(self, estado=Oferta.Estado.BORRADOR, **overrides):
        oferta = Oferta.objects.create(
            empresa=self.empresa,
            titulo=overrides.pop("titulo", "Oferta de prueba"),
            descripcion="Descripción",
            requisitos_obligatorios="Requisitos",
            anos_experiencia=1,
            tipo_contrato=overrides.pop("tipo_contrato", self.tipo),
            modalidad=overrides.pop("modalidad", self.modalidad),
            departamento=overrides.pop("departamento", self.departamento),
            municipio="Oruro",
            fecha_cierre=overrides.pop(
                "fecha_cierre",
                timezone.localdate() + timedelta(days=20),
            ),
            plazas=1,
            estado=estado,
            **overrides,
        )
        oferta.profesiones.set([self.profesion])
        return oferta


class EmpresaOfertasTests(OfertasTestsBase):
    def test_empresa_aprobada_crea_borrador(self):
        self.client.force_login(self.empresa_user)

        response = self.client.post(
            reverse("ofertas:empresa_crear"),
            self.datos_oferta(),
        )

        self.assertEqual(response.status_code, 302)
        oferta = Oferta.objects.get(titulo="Desarrollador Full Stack")
        self.assertEqual(oferta.empresa, self.empresa)
        self.assertEqual(oferta.estado, Oferta.Estado.BORRADOR)
        self.assertEqual(oferta.profesiones.count(), 1)
        self.assertEqual(oferta.requerimientos_habilidad.count(), 3)
        self.assertEqual(
            oferta.requerimientos_habilidad.filter(obligatoria=True).count(),
            2,
        )

    def test_empresa_pendiente_no_crea_ofertas(self):
        user, empresa = crear_empresa(
            estado=Empresa.Estado.PENDIENTE,
            email="pendiente@example.com",
            nit="4000002",
            celular="+59170004002",
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("ofertas:empresa_crear"),
            self.datos_oferta(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("dashboard:empresa"))
        self.assertFalse(Oferta.objects.filter(empresa=empresa).exists())

    def test_enviar_a_revision(self):
        oferta = self.crear_oferta()
        self.client.force_login(self.empresa_user)

        response = self.client.post(
            reverse("ofertas:empresa_enviar", args=[oferta.pk])
        )

        self.assertEqual(response.status_code, 302)
        oferta.refresh_from_db()
        self.assertEqual(oferta.estado, Oferta.Estado.EN_REVISION_GADOR)

    def test_solo_edita_borradores(self):
        oferta = self.crear_oferta(estado=Oferta.Estado.EN_REVISION_GADOR)
        self.client.force_login(self.empresa_user)

        response = self.client.get(
            reverse("ofertas:empresa_editar", args=[oferta.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("ofertas:empresa_lista"))

    @override_settings(EMPRESA_MAX_OFERTAS_ACTIVAS=1)
    def test_limite_de_ofertas_activas(self):
        self.crear_oferta(estado=Oferta.Estado.PUBLICADA)
        self.client.force_login(self.empresa_user)

        response = self.client.get(reverse("ofertas:empresa_crear"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("ofertas:empresa_lista"))

    def test_listado_empresa_paginado(self):
        for indice in range(11):
            self.crear_oferta(titulo=f"Oferta {indice}")
        self.client.force_login(self.empresa_user)

        response = self.client.get(reverse("ofertas:empresa_lista"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["page_obj"].object_list), 1)
        self.assertContains(response, "Página 2 de 2")

    def test_empresa_no_puede_entrar_al_panel_ofertas_gador(self):
        self.client.force_login(self.empresa_user)

        response = self.client.get(reverse("ofertas:gador_lista"))
        self.assertEqual(response.status_code, 403)


class GadorOfertasTests(OfertasTestsBase):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.admin)
        self.oferta = self.crear_oferta(estado=Oferta.Estado.EN_REVISION_GADOR)

    def test_lista_y_filtra_ofertas(self):
        response = self.client.get(reverse("ofertas:gador_lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta.titulo)

        response = self.client.get(
            reverse("ofertas:gador_lista"),
            {"estado": Oferta.Estado.EN_REVISION_GADOR},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"].object_list), 1)

    def test_detalle_oferta(self):
        response = self.client.get(
            reverse("ofertas:gador_detalle", args=[self.oferta.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta.titulo)
        self.assertContains(response, self.empresa.razon_social)

    def test_aprobar_publica(self):
        response = self.client.post(
            reverse("ofertas:gador_accion", args=[self.oferta.pk]),
            {"accion": "aprobar"},
        )

        self.assertEqual(response.status_code, 302)
        self.oferta.refresh_from_db()
        self.assertEqual(self.oferta.estado, Oferta.Estado.PUBLICADA)
        self.assertIsNotNone(self.oferta.publicada_en)
        self.assertEqual(self.oferta.revisada_por, self.admin)

    def test_devolver_exige_motivo(self):
        response = self.client.post(
            reverse("ofertas:gador_accion", args=[self.oferta.pk]),
            {"accion": "devolver", "motivo": ""},
            follow=True,
        )

        self.assertContains(response, "Debes indicar el motivo")
        self.oferta.refresh_from_db()
        self.assertEqual(self.oferta.estado, Oferta.Estado.EN_REVISION_GADOR)

    def test_devolver_a_borrador(self):
        response = self.client.post(
            reverse("ofertas:gador_accion", args=[self.oferta.pk]),
            {"accion": "devolver", "motivo": "Faltan requisitos."},
        )

        self.assertEqual(response.status_code, 302)
        self.oferta.refresh_from_db()
        self.assertEqual(self.oferta.estado, Oferta.Estado.BORRADOR)
        self.assertEqual(self.oferta.motivo_revision, "Faltan requisitos.")

    def test_sidebar_gador_incluye_ofertas(self):
        response = self.client.get(reverse("dashboard:gador"))
        self.assertContains(response, reverse("ofertas:gador_lista"))

    def test_solo_superadmin_puede_revisar(self):
        self.client.force_login(self.empresa_user)
        response = self.client.get(reverse("ofertas:gador_lista"))
        self.assertEqual(response.status_code, 403)

    def test_oferta_sin_profesion_ni_habilidades_es_valida(self):
        self.client.force_login(self.empresa_user)

        datos = self.datos_oferta()
        datos.pop("profesiones")
        datos.pop("habilidades_obligatorias")
        datos.pop("habilidades_deseables")

        response = self.client.post(reverse("ofertas:empresa_crear"), datos)

        self.assertEqual(response.status_code, 302)
        oferta = Oferta.objects.get(titulo="Desarrollador Full Stack")
        self.assertEqual(oferta.profesiones.count(), 0)
        self.assertEqual(oferta.requerimientos_habilidad.count(), 0)

    def test_formulario_tiene_wizard_y_tags(self):
        self.client.force_login(self.empresa_user)

        response = self.client.get(reverse("ofertas:empresa_crear"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="wizard-step-1"')
        self.assertContains(response, 'id="id_profesiones_tag_search"')
        self.assertContains(response, 'id="id_habilidades_obligatorias_tag_search"')
        self.assertContains(response, "Profesiones afines (opcional)")

    def test_editar_conserva_profesion_y_habilidades(self):
        oferta = self.crear_oferta()
        oferta.profesiones.set([self.profesion])
        from apps.recruitment.ofertas.models import OfertaHabilidad

        OfertaHabilidad.objects.create(
            oferta=oferta,
            habilidad=self.habilidad_1,
            obligatoria=True,
        )
        OfertaHabilidad.objects.create(
            oferta=oferta,
            habilidad=self.habilidad_2,
            obligatoria=False,
        )
        self.client.force_login(self.empresa_user)

        response = self.client.get(
            reverse("ofertas:empresa_editar", args=[oferta.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profesion.nombre)
        self.assertContains(response, self.habilidad_1.nombre)
        self.assertContains(response, self.habilidad_2.nombre)
