from __future__ import annotations

from django.test import Client, TestCase
from django.urls import reverse

from apps.platform.accounts.models import Role, User
from apps.platform.audit.models import AuditLog
from apps.platform.audit.service import registrar


def _usuario(email: str, rol: str, is_admin: bool = False) -> User:
    return User.objects.create_user(
        email=email,
        password="ClaveSegura123!",
        role=Role.objects.get(codigo=rol),
        is_staff=is_admin,
        is_superuser=is_admin,
        celular_verificado=True,
    )


class ServiceTests(TestCase):
    def test_registrar_guarda_accion_con_json(self):
        gador = _usuario("gador@example.com", Role.Code.SUPERADMIN, True)
        request = self.client.get("/").wsgi_request

        row = registrar(
            request,
            AuditLog.Accion.CAMBIO_ESTADO,
            None,
            antes={"estado": "PENDIENTE_VALIDACION"},
            despues={"estado": "APROBADA"},
            usuario=gador,
        )

        self.assertEqual(row.usuario, gador)
        self.assertEqual(row.accion, AuditLog.Accion.CAMBIO_ESTADO)
        self.assertEqual(row.datos_antes, {"estado": "PENDIENTE_VALIDACION"})
        self.assertEqual(row.datos_despues, {"estado": "APROBADA"})
        self.assertEqual(row.ip, "127.0.0.1")


class VistaAuditTests(TestCase):
    def setUp(self):
        self.gador = _usuario("gador2@example.com", Role.Code.SUPERADMIN, True)
        AuditLog.objects.create(accion=AuditLog.Accion.LOGIN)

    def test_solamente_gador_entra_a_la_lista(self):
        c = Client()
        c.force_login(_usuario("empresa.audit@example.com", Role.Code.EMPRESA))
        self.assertEqual(c.get(reverse("audit:lista")).status_code, 403)

        c = Client()
        c.force_login(self.gador)
        response = c.get(reverse("audit:lista"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Auditoría")

    def test_detalle_muestra_json(self):
        row = AuditLog.objects.first()
        row.datos_antes = {"estado": "PENDIENTE_VALIDACION"}
        row.datos_despues = {"estado": "APROBADA"}
        row.save()

        c = Client()
        c.force_login(self.gador)
        response = c.get(reverse("audit:detalle", args=[row.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PENDIENTE_VALIDACION")
        self.assertContains(response, "APROBADA")

    def test_validacion_empresa_genera_registro(self):
        from apps.recruitment.catalogos.models import Rubro
        from apps.recruitment.empresas.models import Empresa

        rubro = Rubro.objects.create(nombre="Servicios")
        user = _usuario("nueva.empresa@example.com", Role.Code.EMPRESA)
        empresa = Empresa.objects.create(
            user=user,
            nit="555001",
            razon_social="Empresa Auditoría",
            rubro=rubro,
            representante_nombres="Ana",
            representante_apellidos="Pérez",
            representante_ci="2222222",
            direccion="Calle Auditoría 1",
        )

        c = Client()
        c.force_login(self.gador)
        response = c.post(
            reverse("empresas:gador_accion", args=[empresa.pk]),
            {"accion": "aprobar"},
        )

        self.assertEqual(response.status_code, 302)
        row = AuditLog.objects.filter(registro_id=empresa.pk).first()
        self.assertIsNotNone(row)
        self.assertEqual(row.accion, AuditLog.Accion.CAMBIO_ESTADO)
        self.assertEqual(
            row.datos_antes["estado"],
            Empresa.Estado.PENDIENTE,
        )
        self.assertEqual(row.datos_despues["estado"], Empresa.Estado.APROBADA)
