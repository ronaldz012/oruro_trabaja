from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.platform.accounts.models import Role, User
from apps.platform.accounts.sms import (
    DemoSmsBackend,
    TextbeeSmsBackend,
    get_sms_backend,
)
from core.exceptions import DomainError


class LoginThrottleTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            email="login@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.POSTULANTE),
            celular="+59170007001",
        )
        self.url = reverse("accounts:login")

    def tearDown(self):
        cache.clear()

    def _fallar(self, ip="127.0.0.1"):
        return self.client.post(
            self.url,
            {
                "username": self.user.email,
                "password": "incorrecta",
            },
            REMOTE_ADDR=ip,
        )

    def test_bloquea_ip_despues_de_cinco_intentos(self):
        for _ in range(5):
            response = self._fallar()
            self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            {
                "username": self.user.email,
                "password": "ClaveSegura123!",
            },
            REMOTE_ADDR="127.0.0.1",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Demasiados intentos")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_otra_ip_no_queda_bloqueada(self):
        for _ in range(5):
            self._fallar(ip="10.0.0.1")

        response = self.client.post(
            self.url,
            {
                "username": self.user.email,
                "password": "ClaveSegura123!",
            },
            REMOTE_ADDR="10.0.0.2",
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_exitoso_limpia_intentos(self):
        for _ in range(4):
            self._fallar()

        response = self.client.post(
            self.url,
            {
                "username": self.user.email,
                "password": "ClaveSegura123!",
            },
            REMOTE_ADDR="127.0.0.1",
        )

        self.assertEqual(response.status_code, 302)
        self.assertIsNone(cache.get("login_attempts:127.0.0.1"))

    def test_formulario_vacio_no_cuenta_como_intento(self):
        for _ in range(5):
            response = self.client.post(
                self.url,
                {"username": "", "password": ""},
                REMOTE_ADDR="127.0.0.1",
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            {
                "username": self.user.email,
                "password": "ClaveSegura123!",
            },
            REMOTE_ADDR="127.0.0.1",
        )

        self.assertEqual(response.status_code, 302)


class SmsBackendTests(TestCase):
    @override_settings(DEMO_MODE=True)
    def test_demo_mode_usa_backend_demo(self):
        self.assertIsInstance(get_sms_backend(), DemoSmsBackend)

    @override_settings(
        DEMO_MODE=False,
        TEXTBEE_API_KEY="api-key",
        TEXTBEE_DEVICE_ID="device-id",
        TEXTBEE_BASE_URL="https://example.test/api/v1",
        TEXTBEE_TIMEOUT_SECONDS=5,
    )
    @patch("apps.platform.accounts.sms.request.urlopen")
    def test_textbee_envia_payload(self, urlopen):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"{}"
        urlopen.return_value = response

        TextbeeSmsBackend().enviar("+59170000000", "Hola")

        solicitud = urlopen.call_args.args[0]
        self.assertEqual(
            solicitud.full_url,
            "https://example.test/api/v1/gateway/send-sms",
        )
        self.assertEqual(
            dict(solicitud.header_items()).get("X-api-key"),
            "api-key",
        )
        self.assertIn(b'"recipients": ["+59170000000"]', solicitud.data)
        self.assertIn(b'"message": "Hola"', solicitud.data)

    @override_settings(
        DEMO_MODE=False,
        TEXTBEE_API_KEY="",
        TEXTBEE_DEVICE_ID="",
    )
    def test_textbee_sin_configuracion(self):
        with self.assertRaises(DomainError):
            TextbeeSmsBackend().enviar("+59170000000", "Hola")

    @override_settings(
        DEMO_MODE=False,
        TEXTBEE_API_KEY="api-key",
        TEXTBEE_DEVICE_ID="device-id",
        TEXTBEE_BASE_URL="https://example.test/api/v1",
        TEXTBEE_TIMEOUT_SECONDS=5,
    )
    @patch("apps.platform.accounts.sms.request.urlopen")
    def test_textbee_error_http(self, urlopen):
        urlopen.side_effect = HTTPError(
            "https://example.test",
            500,
            "Error",
            {},
            None,
        )

        with self.assertRaises(DomainError):
            TextbeeSmsBackend().enviar("+59170000000", "Hola")
