from __future__ import annotations

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from apps.recruitment.catalogos.models import Profesion
from apps.recruitment.ofertas.models import Oferta, OfertaGuardada

from .test_ofertas import OfertasTestsBase
from .test_postulaciones import crear_postulante


class EmpleosPublicosTests(OfertasTestsBase):
    def setUp(self):
        super().setUp()
        self.postulante_user, self.perfil = crear_postulante()
        hoy = timezone.localdate()
        self.oferta = self.crear_oferta(
            titulo="Oferta publicada",
            estado=Oferta.Estado.PUBLICADA,
            publicada_en=timezone.now(),
            fecha_cierre=hoy + timedelta(days=30),
        )
        self.otra = self.crear_oferta(
            titulo="Otra oferta",
            estado=Oferta.Estado.PUBLICADA,
            publicada_en=timezone.now() - timedelta(days=1),
            fecha_cierre=hoy + timedelta(days=10),
        )

    def test_filtra_por_profesion(self):
        otra_profesion = Profesion.objects.create(nombre="Contabilidad")
        self.otra.profesiones.set([otra_profesion])
        self.client.force_login(self.postulante_user)

        response = self.client.get(
            reverse("ofertas:publicas"),
            {"profesion": otra_profesion.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.otra.titulo)
        self.assertNotContains(response, self.oferta.titulo)

    def test_ordena_por_cierre_proximo(self):
        self.client.force_login(self.postulante_user)

        response = self.client.get(
            reverse("ofertas:publicas"),
            {"orden": "cierre"},
        )

        self.assertEqual(response.status_code, 200)
        resultados = list(response.context["page_obj"].object_list)
        self.assertEqual(resultados[0].pk, self.otra.pk)

    def test_busqueda_y_filtro_se_combinan(self):
        otra_profesion = Profesion.objects.create(nombre="Diseño")
        self.otra.profesiones.set([otra_profesion])
        self.client.force_login(self.postulante_user)

        response = self.client.get(
            reverse("ofertas:publicas"),
            {"q": "Otra", "profesion": otra_profesion.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.otra.titulo)
        self.assertNotContains(response, self.oferta.titulo)

    def test_filtros_activos_cuenta_los_avanzados(self):
        self.client.force_login(self.postulante_user)

        response = self.client.get(
            reverse("ofertas:publicas"),
            {
                "profesion": self.profesion.pk,
                "orden": "cierre",
            },
        )

        self.assertEqual(response.context["filtros_activos"], 2)

    def test_guardar_y_quitar_oferta(self):
        self.client.force_login(self.postulante_user)
        url = reverse("ofertas:guardar", args=[self.oferta.pk])
        siguiente = reverse("ofertas:publicas")

        response = self.client.post(url, {"next": siguiente})

        self.assertRedirects(response, siguiente, fetch_redirect_response=False)
        self.assertTrue(
            OfertaGuardada.objects.filter(
                postulante=self.perfil,
                oferta=self.oferta,
            ).exists()
        )

        response = self.client.post(url, {"next": siguiente})

        self.assertRedirects(response, siguiente, fetch_redirect_response=False)
        self.assertFalse(
            OfertaGuardada.objects.filter(
                postulante=self.perfil,
                oferta=self.oferta,
            ).exists()
        )

    def test_tab_guardadas_muestra_solo_las_propias(self):
        OfertaGuardada.objects.create(
            postulante=self.perfil,
            oferta=self.oferta,
        )
        self.client.force_login(self.postulante_user)

        response = self.client.get(
            reverse("ofertas:publicas"),
            {"guardadas": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta.titulo)
        self.assertNotContains(response, self.otra.titulo)
        self.assertEqual(response.context["total_guardadas"], 1)

    def test_guardadas_de_otro_postulante_no_aparecen(self):
        _, otro_perfil = crear_postulante(
            email="otro-postulante@example.com",
            ci="8888888 LP",
            celular="+59170006001",
        )
        OfertaGuardada.objects.create(
            postulante=otro_perfil,
            oferta=self.oferta,
        )
        self.client.force_login(self.postulante_user)

        response = self.client.get(
            reverse("ofertas:publicas"),
            {"guardadas": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.oferta.titulo)
        self.assertEqual(response.context["total_guardadas"], 0)

    def test_solo_postulante_puede_guardar(self):
        self.client.force_login(self.empresa_user)

        response = self.client.post(
            reverse("ofertas:guardar", args=[self.oferta.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_detalle_muestra_quitar_de_guardadas(self):
        OfertaGuardada.objects.create(
            postulante=self.perfil,
            oferta=self.oferta,
        )
        self.client.force_login(self.postulante_user)

        response = self.client.get(
            reverse("ofertas:detalle", args=[self.oferta.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quitar de guardadas")

    def test_listado_muestra_boton_guardar(self):
        self.client.force_login(self.postulante_user)

        response = self.client.get(reverse("ofertas:publicas"))

        self.assertContains(
            response,
            reverse("ofertas:guardar", args=[self.oferta.pk]),
        )

    def test_paginacion_visible_con_una_sola_pagina(self):
        self.client.force_login(self.postulante_user)

        response = self.client.get(reverse("ofertas:publicas"))

        self.assertContains(response, "Página 1 de 1")
        self.assertContains(response, "Anterior")
        self.assertContains(response, "Siguiente")

    def test_next_inseguro_redirige_a_empleos(self):
        self.client.force_login(self.postulante_user)

        response = self.client.post(
            reverse("ofertas:guardar", args=[self.oferta.pk]),
            {"next": "https://sitio-malicioso.example.com/"},
        )

        self.assertRedirects(
            response,
            reverse("ofertas:publicas"),
            fetch_redirect_response=False,
        )
