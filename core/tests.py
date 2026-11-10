from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.test import TestCase
from django.urls import reverse

from apps.recruitment.postulantes.models import PostulanteProfile
from core.storage import private_storage


class PWATests(TestCase):
    def test_manifest(self):
        response = self.client.get(reverse("pwa_manifest"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/manifest+json")
        data = response.json()
        self.assertEqual(data["name"], "Oruro Trabaja")
        self.assertEqual(data["short_name"], "OruroTrabaja")
        self.assertEqual(data["start_url"], "/")
        self.assertEqual(data["scope"], "/")
        self.assertEqual(data["theme_color"], "#7A1014")
        self.assertTrue(any(icon["sizes"] == "512x512" for icon in data["icons"]))

    def test_service_worker(self):
        response = self.client.get(reverse("pwa_service_worker"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/javascript")
        self.assertEqual(response["Service-Worker-Allowed"], "/")
        self.assertIn("oruro-trabaja-v10", b"".join(response.streaming_content).decode())

    def test_offline_page_is_public(self):
        response = self.client.get(reverse("pwa_offline"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sin conexión")
        self.assertContains(response, "Oruro Trabaja")

    def test_login_includes_pwa_metadata_and_brand(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("pwa_manifest"))
        self.assertContains(response, 'name="theme-color" content="#7A1014"')
        self.assertContains(response, "Oruro Trabaja")
        self.assertContains(response, "img/logo-bolsa-trabajo.svg")
        self.assertContains(response, "img/login-oruro-trabaja.webp")

    def test_pwa_icons_exist(self):
        for name in (
            "icon-192.png",
            "icon-512.png",
            "maskable-512.png",
            "apple-touch-icon.png",
            "favicon-32.png",
        ):
            self.assertTrue(
                (Path(settings.BASE_DIR) / "static" / "icons" / name).exists(),
                f"Falta el icono {name}",
            )


class StorageTests(TestCase):
    def test_cv_uses_configured_private_storage(self):
        field = PostulanteProfile._meta.get_field("cv")

        self.assertIs(field.storage, private_storage())
        self.assertIsInstance(field.storage, FileSystemStorage)

