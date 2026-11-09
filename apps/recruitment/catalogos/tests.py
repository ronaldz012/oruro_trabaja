from django.test import TestCase
from django.urls import reverse

from apps.platform.accounts.models import Role, User
from apps.recruitment.catalogos.models import Profesion, Rubro


class CatalogosGadorTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="catalogos-admin@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.SUPERADMIN),
        )
        self.rubro = Rubro.objects.create(nombre="Tecnología")
        self.profesion = Profesion.objects.create(nombre="Ingeniería de Sistemas")
        self.client.force_login(self.admin)

    def test_gador_puede_entrar(self):
        response = self.client.get(reverse("catalogos:gador_lista"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Catálogos")
        self.assertContains(response, "Solo lectura")
        self.assertContains(response, self.rubro.nombre)

    def test_cambia_de_tab(self):
        response = self.client.get(
            reverse("catalogos:gador_lista"),
            {"tipo": "profesiones"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.profesion.nombre)
        self.assertEqual(response.context["catalogo_actual"]["codigo"], "profesiones")

    def test_tab_invalido_vuelve_a_rubros(self):
        response = self.client.get(
            reverse("catalogos:gador_lista"),
            {"tipo": "no-existe"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["catalogo_actual"]["codigo"], "rubros")

    def test_paginacion(self):
        for indice in range(20):
            Rubro.objects.create(nombre=f"Rubro {indice}")

        response = self.client.get(
            reverse("catalogos:gador_lista"),
            {"tipo": "rubros", "page": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["page_obj"].object_list), 1)

    def test_otro_rol_no_puede_entrar(self):
        empresa = User.objects.create_user(
            email="catalogos-empresa@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.EMPRESA),
        )
        self.client.force_login(empresa)

        response = self.client.get(reverse("catalogos:gador_lista"))

        self.assertEqual(response.status_code, 403)
