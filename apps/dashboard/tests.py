from django.test import TestCase
from django.urls import reverse

from apps.platform.accounts.models import Role, User


class DashboardGadorTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="dashboard-admin@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.SUPERADMIN),
        )
        self.client.force_login(self.admin)

    def test_sidebar_incluye_catalogos_y_reportes(self):
        response = self.client.get(reverse("dashboard:gador"))

        self.assertContains(response, reverse("catalogos:gador_lista"))
        self.assertContains(response, reverse("dashboard:reportes"))

    def test_reporte_placeholder(self):
        response = self.client.get(reverse("dashboard:reportes"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reportes en preparación")
        self.assertContains(response, "En preparación")

    def test_otro_rol_no_puede_ver_reportes(self):
        empresa = User.objects.create_user(
            email="dashboard-empresa@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.EMPRESA),
        )
        self.client.force_login(empresa)

        response = self.client.get(reverse("dashboard:reportes"))

        self.assertEqual(response.status_code, 403)
