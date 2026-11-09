from __future__ import annotations

from django.test import TestCase
from django.urls import reverse

from apps.platform.accounts.models import Role, User
from apps.recruitment.catalogos.models import Rubro
from apps.recruitment.empresas.models import Empresa


def datos_empresa(**overrides):
    datos = {
        "email": "nuevaempresa@example.com",
        "password1": "ClaveSegura123!",
        "password2": "ClaveSegura123!",
        "nit": "1234567890123",
        "razon_social": "Nueva Empresa S.R.L.",
        "rubro": None,
        "representante_nombres": "Carlos",
        "representante_apellidos": "Pérez",
        "representante_ci": "1234567 LP",
        "celular": "70002001",
        "direccion": "Av. Principal 123",
        "descripcion": "Empresa de prueba",
        "terminos": "on",
    }
    datos.update(overrides)
    return datos


def crear_empresa(
    estado=Empresa.Estado.PENDIENTE,
    email="empresa@example.com",
    nit="1000001",
    celular=None,
):
    role = Role.objects.get(codigo=Role.Code.EMPRESA)
    rubro, _ = Rubro.objects.get_or_create(nombre="Tecnología")
    user = User.objects.create_user(
        email=email,
        password="ClaveSegura123!",
        role=role,
        celular=celular or f"+5917{nit[-7:]}",
        first_name="Empresa",
        last_name="Demo",
    )
    empresa = Empresa.objects.create(
        user=user,
        nit=nit,
        razon_social="Empresa Demo",
        rubro=rubro,
        representante_nombres="Ana",
        representante_apellidos="Demo",
        representante_ci="1111111 LP",
        direccion="Calle Demo 123",
        estado=estado,
    )
    return user, empresa


class RegistroEmpresaTests(TestCase):
    def setUp(self):
        self.rubro, _ = Rubro.objects.get_or_create(nombre="Tecnología")

    def test_registro_crea_empresa_pendiente_y_loguea(self):
        response = self.client.post(
            reverse("empresas:registro"),
            datos_empresa(rubro=self.rubro.pk),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("dashboard:empresa"))

        user = User.objects.get(email="nuevaempresa@example.com")
        self.assertEqual(user.role.codigo, Role.Code.EMPRESA)
        self.assertFalse(user.celular_verificado)
        self.assertEqual(user.celular, "+59170002001")

        empresa = Empresa.objects.get(user=user)
        self.assertEqual(empresa.estado, Empresa.Estado.PENDIENTE)
        self.assertEqual(empresa.nit, "1234567890123")
        self.assertEqual(empresa.rubro, self.rubro)
        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.get(reverse("dashboard:empresa"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pendiente de validación")

    def test_nit_duplicado(self):
        crear_empresa(nit="1234567890123")

        response = self.client.post(
            reverse("empresas:registro"),
            datos_empresa(rubro=self.rubro.pk, email="otra@example.com", celular="70002002"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una empresa con ese NIT")
        self.assertFalse(User.objects.filter(email="otra@example.com").exists())

    def test_email_duplicado(self):
        crear_empresa(email="nuevaempresa@example.com", nit="1000002")

        response = self.client.post(
            reverse("empresas:registro"),
            datos_empresa(rubro=self.rubro.pk, celular="70002002"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una cuenta con ese correo")

    def test_celular_duplicado(self):
        crear_empresa(nit="1000003", celular="+59170003000")

        response = self.client.post(
            reverse("empresas:registro"),
            datos_empresa(
                rubro=self.rubro.pk,
                email="otra@example.com",
                celular="70003000",
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una cuenta con ese celular")

    def test_empresa_pendiente_puede_login_y_ver_estado(self):
        user, empresa = crear_empresa()

        autenticado = self.client.login(
            username=user.email,
            password="ClaveSegura123!",
        )

        self.assertTrue(autenticado)
        response = self.client.get(reverse("dashboard:empresa"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pendiente de validación")
        self.assertContains(response, empresa.razon_social)

    def test_empresa_no_puede_entrar_al_panel_gador(self):
        user, _ = crear_empresa()
        self.client.force_login(user)

        response = self.client.get(reverse("empresas:gador_lista"))
        self.assertEqual(response.status_code, 403)


class GadorEmpresasTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.SUPERADMIN),
        )
        self.client.force_login(self.admin)
        self.pendiente_user, self.pendiente = crear_empresa(
            email="pendiente@example.com",
            nit="2000001",
        )
        self.aprobada_user, self.aprobada = crear_empresa(
            estado=Empresa.Estado.APROBADA,
            email="aprobada@example.com",
            nit="2000002",
        )

    def test_lista_todas_y_filtra_por_estado(self):
        response = self.client.get(reverse("empresas:gador_lista"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Empresa Demo")
        self.assertEqual(len(response.context["empresas"]), 2)

        response = self.client.get(
            reverse("empresas:gador_lista"),
            {"estado": Empresa.Estado.PENDIENTE},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [empresa.pk for empresa in response.context["empresas"]],
            [self.pendiente.pk],
        )

    def test_detalle_empresa(self):
        response = self.client.get(
            reverse("empresas:gador_detalle", args=[self.pendiente.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.pendiente.razon_social)
        self.assertContains(response, self.pendiente.nit)

    def test_aprobar_empresa(self):
        response = self.client.post(
            reverse("empresas:gador_accion", args=[self.pendiente.pk]),
            {"accion": "aprobar"},
        )

        self.assertEqual(response.status_code, 302)
        self.pendiente.refresh_from_db()
        self.assertEqual(self.pendiente.estado, Empresa.Estado.APROBADA)
        self.assertEqual(self.pendiente.revisada_por, self.admin)
        self.assertIsNotNone(self.pendiente.revisada_en)

    def test_rechazar_exige_motivo(self):
        response = self.client.post(
            reverse("empresas:gador_accion", args=[self.pendiente.pk]),
            {"accion": "rechazar", "motivo": ""},
            follow=True,
        )

        self.assertContains(response, "Debes indicar el motivo del rechazo")
        self.pendiente.refresh_from_db()
        self.assertEqual(self.pendiente.estado, Empresa.Estado.PENDIENTE)

    def test_rechazar_guarda_motivo(self):
        response = self.client.post(
            reverse("empresas:gador_accion", args=[self.pendiente.pk]),
            {"accion": "rechazar", "motivo": "Documentación incompleta."},
        )

        self.assertEqual(response.status_code, 302)
        self.pendiente.refresh_from_db()
        self.assertEqual(self.pendiente.estado, Empresa.Estado.RECHAZADA)
        self.assertEqual(self.pendiente.motivo_rechazo, "Documentación incompleta.")

    def test_suspender_empresa_aprobada(self):
        response = self.client.post(
            reverse("empresas:gador_accion", args=[self.aprobada.pk]),
            {"accion": "suspender"},
        )

        self.assertEqual(response.status_code, 302)
        self.aprobada.refresh_from_db()
        self.assertEqual(self.aprobada.estado, Empresa.Estado.SUSPENDIDA)

    def test_empresa_puede_ver_mis_ofertas_placeholder(self):
        user, _ = crear_empresa(email="ofertas@example.com", nit="3000001")
        self.client.force_login(user)

        response = self.client.get(reverse("ofertas:empresa_lista"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mis ofertas")
        self.assertContains(response, 'id="sidebar"')
        self.assertContains(response, 'aria-current="page"')

    def test_gador_dashboard_tiene_sidebar_empresas(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("dashboard:gador"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="sidebar"')
        self.assertContains(response, reverse("empresas:gador_lista"))
