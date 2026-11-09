from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.platform.accounts.models import CodigoOTP, RegistroPendiente, Role, User
from apps.recruitment.postulantes.models import PostulanteProfile


def datos_registro(**overrides):
    datos = {
        "ci": "1234567 LP",
        "nombres": "Ana",
        "apellidos": "Pérez",
        "celular": "71234567",
        "email": "ana@example.com",
        "password1": "ClaveSegura123!",
        "password2": "ClaveSegura123!",
        "terminos": "on",
    }
    datos.update(overrides)
    return datos


def crear_usuario(role, **overrides):
    datos = {
        "email": "otro@example.com",
        "password": "ClaveSegura123!",
        "role": role,
        "celular": "+59170000001",
    }
    datos.update(overrides)
    return User.objects.create_user(**datos)


@override_settings(DEMO_MODE=True)
class RegistroPendienteTests(TestCase):
    def registrar(self, **overrides):
        return self.client.post(
            reverse("postulantes:registro"),
            datos_registro(**overrides),
        )

    def pendiente(self) -> RegistroPendiente:
        return RegistroPendiente.objects.get()

    def codigo_demo(self) -> str:
        return self.client.session["demo_otp"]

    def test_registro_crea_pendiente_y_no_usuario(self):
        response = self.registrar()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("postulantes:verificar_celular"),
        )
        self.assertEqual(User.objects.count(), 0)

        pendiente = self.pendiente()
        self.assertEqual(pendiente.ci, "1234567 LP")
        self.assertEqual(pendiente.celular, "+59171234567")
        self.assertEqual(pendiente.email, "ana@example.com")
        self.assertTrue(check_password("ClaveSegura123!", pendiente.password_hash))
        self.assertGreater(pendiente.expira_en, timezone.now())
        self.assertEqual(
            self.client.session["registro_pendiente_id"],
            str(pendiente.pk),
        )

        otp = CodigoOTP.objects.get(registro_pendiente=pendiente)
        self.assertIsNone(otp.user)
        self.assertEqual(otp.celular, "+59171234567")
        self.assertEqual(otp.proposito, CodigoOTP.Proposito.REGISTRO_PENDIENTE)
        self.assertEqual(len(self.codigo_demo()), 6)

    def test_verificacion_crea_usuario_y_limpia_pendiente(self):
        self.registrar()
        codigo = self.codigo_demo()

        response = self.client.post(
            reverse("postulantes:verificar_celular"),
            {"codigo": codigo},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("home"))

        user = User.objects.get(email="ana@example.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.celular_verificado)
        self.assertEqual(user.celular, "+59171234567")
        self.assertEqual(user.first_name, "Ana")
        self.assertEqual(user.last_name, "Pérez")
        self.assertEqual(user.role.codigo, Role.Code.POSTULANTE)
        self.assertTrue(check_password("ClaveSegura123!", user.password))

        perfil = PostulanteProfile.objects.get(user=user)
        self.assertEqual(perfil.ci, "1234567 LP")

        self.assertEqual(RegistroPendiente.objects.count(), 0)
        self.assertEqual(CodigoOTP.objects.count(), 1)
        self.assertIsNone(CodigoOTP.objects.get().registro_pendiente_id)
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            user.pk,
        )

    def test_codigo_incorrecto_no_crea_usuario(self):
        self.registrar()

        response = self.client.post(
            reverse("postulantes:verificar_celular"),
            {"codigo": "000000"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Código incorrecto")
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(RegistroPendiente.objects.count(), 1)

        otp = CodigoOTP.objects.get()
        self.assertEqual(otp.intentos, 1)
        self.assertIsNone(otp.consumido_en)

    def test_codigo_vencido_no_crea_usuario(self):
        self.registrar()
        codigo = self.codigo_demo()
        CodigoOTP.objects.update(
            expira_en=timezone.now() - timedelta(minutes=1)
        )

        response = self.client.post(
            reverse("postulantes:verificar_celular"),
            {"codigo": codigo},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "venció")
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(RegistroPendiente.objects.count(), 1)

    def test_pendiente_vencido_no_permite_verificar(self):
        self.registrar()
        RegistroPendiente.objects.update(
            expira_en=timezone.now() - timedelta(minutes=1)
        )

        response = self.client.get(reverse("postulantes:verificar_celular"))

        self.assertRedirects(
            response,
            reverse("postulantes:registro"),
            fetch_redirect_response=False,
        )
        self.assertEqual(User.objects.count(), 0)

    def test_ci_duplicada(self):
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        user = crear_usuario(role)
        PostulanteProfile.objects.create(user=user, ci="1234567 LP")

        response = self.registrar(email="nueva@example.com", celular="70000002")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe un postulante con esa CI.")
        self.assertEqual(RegistroPendiente.objects.count(), 0)

    def test_email_duplicado(self):
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        crear_usuario(role, email="ana@example.com")

        response = self.registrar(ci="7654321 OR", celular="70000002")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una cuenta con ese correo.")
        self.assertEqual(RegistroPendiente.objects.count(), 0)

    def test_celular_duplicado(self):
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        crear_usuario(role, celular="+59171234567")

        response = self.registrar(ci="7654321 OR", email="nueva@example.com")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una cuenta con ese celular.")
        self.assertEqual(RegistroPendiente.objects.count(), 0)

    @override_settings(OTP_RESEND_SECONDS=0)
    def test_mismo_celular_reemplaza_pendiente_anterior(self):
        self.registrar()
        primero = self.pendiente()
        primer_codigo = self.codigo_demo()

        self.registrar(email="nueva@example.com", ci="7654321 OR")

        self.assertEqual(RegistroPendiente.objects.count(), 1)
        segundo = self.pendiente()
        self.assertNotEqual(primero.pk, segundo.pk)
        self.assertEqual(segundo.email, "nueva@example.com")
        self.assertEqual(segundo.ci, "7654321 OR")
        self.assertNotEqual(primer_codigo, self.codigo_demo())
        self.assertFalse(
            CodigoOTP.objects.filter(registro_pendiente_id=primero.pk).exists()
        )
        self.assertTrue(
            CodigoOTP.objects.filter(
                celular="+59171234567",
                registro_pendiente__isnull=True,
            ).exists()
        )

    @override_settings(OTP_RESEND_SECONDS=0)
    def test_limite_celular_al_reintentar_registro(self):
        self.registrar()
        self.registrar(email="nueva@example.com", ci="7654321 OR")
        self.registrar(email="tercera@example.com", ci="1111111 LP")
        self.assertEqual(
            CodigoOTP.objects.filter(celular="+59171234567").count(),
            3,
        )

        response = self.registrar(
            email="cuarta@example.com",
            ci="2222222 LP",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "límite de 3")
        self.assertEqual(RegistroPendiente.objects.count(), 1)
        self.assertEqual(
            CodigoOTP.objects.filter(celular="+59171234567").count(),
            3,
        )

    def test_pendientes_no_reservan_ci_ni_email(self):
        self.registrar()
        self.registrar(celular="70000002")

        self.assertEqual(RegistroPendiente.objects.count(), 2)
        self.assertEqual(
            RegistroPendiente.objects.filter(email="ana@example.com").count(),
            2,
        )

    def test_carrera_email_tomado(self):
        self.registrar()
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        crear_usuario(
            role,
            email="ana@example.com",
            celular="+59170000001",
        )

        response = self.client.post(
            reverse("postulantes:verificar_celular"),
            {"codigo": self.codigo_demo()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una cuenta con ese correo.")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(RegistroPendiente.objects.count(), 1)

    def test_carrera_ci_tomada(self):
        self.registrar()
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        user = crear_usuario(
            role,
            email="otro@example.com",
            celular="+59170000001",
        )
        PostulanteProfile.objects.create(user=user, ci="1234567 LP")

        response = self.client.post(
            reverse("postulantes:verificar_celular"),
            {"codigo": self.codigo_demo()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe un postulante con esa CI.")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(RegistroPendiente.objects.count(), 1)

    def test_carrera_celular_tomado(self):
        self.registrar()
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        crear_usuario(
            role,
            email="otro@example.com",
            celular="+59171234567",
        )

        response = self.client.post(
            reverse("postulantes:verificar_celular"),
            {"codigo": self.codigo_demo()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una cuenta con ese celular.")
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(RegistroPendiente.objects.count(), 1)

    def test_cambiar_celular_conserva_datos(self):
        self.registrar()
        pendiente = self.pendiente()
        codigo_anterior = self.codigo_demo()

        response = self.client.post(
            reverse("postulantes:cambiar_celular"),
            {"celular": "70002222"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response["Location"],
            reverse("postulantes:verificar_celular"),
        )

        pendiente.refresh_from_db()
        self.assertEqual(pendiente.celular, "+59170002222")
        self.assertEqual(pendiente.ci, "1234567 LP")
        self.assertEqual(pendiente.email, "ana@example.com")
        self.assertTrue(check_password("ClaveSegura123!", pendiente.password_hash))

        self.assertNotEqual(codigo_anterior, self.codigo_demo())
        self.assertEqual(
            CodigoOTP.objects.filter(
                registro_pendiente=pendiente,
                consumido_en__isnull=True,
            ).count(),
            1,
        )

    def test_cambiar_celular_duplicado(self):
        self.registrar()
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        crear_usuario(role, celular="+59170003333")

        response = self.client.post(
            reverse("postulantes:cambiar_celular"),
            {"celular": "70003333"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ya existe una cuenta con ese celular.")
        self.assertEqual(self.pendiente().celular, "+59171234567")

    @override_settings(OTP_RESEND_SECONDS=0)
    def test_cambiar_celular_respeta_limite_por_celular(self):
        self.registrar()
        pendiente = self.pendiente()
        for _ in range(3):
            CodigoOTP.objects.create(
                celular="+59170004444",
                codigo_hash=make_password("000000"),
                proposito=CodigoOTP.Proposito.REGISTRO_PENDIENTE,
                expira_en=timezone.now() + timedelta(minutes=10),
                ip="127.0.0.1",
            )

        response = self.client.post(
            reverse("postulantes:cambiar_celular"),
            {"celular": "70004444"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "límite de 3")
        pendiente.refresh_from_db()
        self.assertEqual(pendiente.celular, "+59171234567")

    def test_reenvio_respeta_cooldown(self):
        self.registrar()

        response = self.client.post(
            reverse("postulantes:reenviar_codigo"),
            follow=True,
        )

        self.assertContains(response, "Espera")
        self.assertEqual(CodigoOTP.objects.count(), 1)

    @override_settings(OTP_RESEND_SECONDS=0)
    def test_reenvio_exitoso(self):
        self.registrar()

        response = self.client.post(
            reverse("postulantes:reenviar_codigo"),
            follow=True,
        )

        self.assertContains(response, "Enviamos un nuevo código")
        self.assertEqual(CodigoOTP.objects.count(), 2)

    @override_settings(OTP_RESEND_SECONDS=0)
    def test_limite_tres_sms_por_celular_en_cinco_horas(self):
        self.registrar()

        self.client.post(reverse("postulantes:reenviar_codigo"))
        self.client.post(reverse("postulantes:reenviar_codigo"))
        self.assertEqual(
            CodigoOTP.objects.filter(celular="+59171234567").count(),
            3,
        )

        response = self.client.post(
            reverse("postulantes:reenviar_codigo"),
            follow=True,
        )

        self.assertContains(response, "límite de 3")
        self.assertEqual(
            CodigoOTP.objects.filter(celular="+59171234567").count(),
            3,
        )

    @override_settings(OTP_RESEND_SECONDS=0)
    def test_limite_cinco_sms_por_ip_en_una_hora(self):
        for indice in range(5):
            response = self.registrar(
                ci=f"100000{indice} LP",
                celular=f"7000000{indice}",
                email=f"ip{indice}@example.com",
            )
            self.assertEqual(response.status_code, 302)

        self.assertEqual(RegistroPendiente.objects.count(), 5)
        self.assertEqual(CodigoOTP.objects.count(), 5)

        response = self.registrar(
            ci="2000000 LP",
            celular="70009999",
            email="ip5@example.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "límite de 5 envíos por hora")
        self.assertEqual(RegistroPendiente.objects.count(), 5)


@override_settings(DEMO_MODE=True)
class LoginSinVerificacionTests(TestCase):
    def test_login_no_redirige_a_verificar(self):
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        crear_usuario(
            role,
            email="ana@example.com",
            celular="+59171234567",
            celular_verificado=False,
        )

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "ana@example.com",
                "password": "ClaveSegura123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("dashboard:postulante"))

        response = self.client.get(reverse("dashboard:postulante"))
        self.assertEqual(response.status_code, 200)

    def test_usuario_desactivado_no_accede_al_panel(self):
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        user = crear_usuario(
            role,
            email="inactivo@example.com",
            celular="+59170000009",
        )
        User.objects.filter(pk=user.pk).update(is_active=False)
        self.client.force_login(user)

        response = self.client.get(reverse("dashboard:postulante"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])


@override_settings(
    DEMO_MODE=False,
    TEXTBEE_API_KEY="",
    TEXTBEE_DEVICE_ID="",
)
class SmsBackendTests(TestCase):
    def test_backend_real_requiere_configuracion(self):
        from apps.platform.accounts.sms import TextbeeSmsBackend, get_sms_backend
        from core.exceptions import DomainError

        self.assertIsInstance(get_sms_backend(), TextbeeSmsBackend)
        with self.assertRaises(DomainError):
            get_sms_backend().enviar("+59171234567", "código 123456")
