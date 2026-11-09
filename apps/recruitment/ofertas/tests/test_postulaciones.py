from __future__ import annotations

from datetime import date, timedelta

from django.core.files.base import ContentFile
from django.urls import reverse
from django.utils import timezone

from apps.platform.accounts.models import Role, User
from apps.recruitment.catalogos.models import Habilidad, Idioma, Modalidad
from apps.recruitment.ofertas.models import Oferta, Postulacion
from apps.recruitment.postulantes.models import (
    Experiencia,
    Formacion,
    PostulanteHabilidad,
    PostulanteIdioma,
    PostulanteProfile,
)

from .test_ofertas import OfertasTestsBase, crear_empresa


def crear_postulante(
    *,
    email="postulante@example.com",
    ci="1234567 LP",
    celular="+59170005001",
    completo=True,
    con_cv=True,
):
    role = Role.objects.get(codigo=Role.Code.POSTULANTE)
    user = User.objects.create_user(
        email=email,
        password="ClaveSegura123!",
        role=role,
        celular=celular,
        first_name="Ana",
        last_name="Postulante",
    )
    perfil = PostulanteProfile.objects.create(user=user, ci=ci)
    if not completo:
        return user, perfil

    perfil.foto = "postulantes/fotos/test.jpg"
    perfil.direccion = "Calle 1"
    perfil.fecha_nacimiento = date(1995, 1, 1)
    if con_cv:
        perfil.cv = "postulantes/cv/test.pdf"
    perfil.save()

    Formacion.objects.create(
        profile=perfil,
        titulo="Ingeniería de Sistemas",
        institucion="Universidad Técnica de Oruro",
        anio_titulacion=2018,
    )
    Experiencia.objects.create(
        profile=perfil,
        empresa="Empresa Demo",
        cargo="Desarrolladora",
        anos=2,
    )
    for nombre in ("Python", "SQL", "Django"):
        habilidad, _ = Habilidad.objects.get_or_create(nombre=nombre)
        PostulanteHabilidad.objects.create(profile=perfil, habilidad=habilidad)
    idioma, _ = Idioma.objects.get_or_create(nombre="Español")
    PostulanteIdioma.objects.create(profile=perfil, idioma=idioma)
    return user, perfil


class PostulacionFlowTests(OfertasTestsBase):
    def setUp(self):
        super().setUp()
        self.postulante_user, self.perfil = crear_postulante()
        self.oferta = self.crear_oferta(
            estado=Oferta.Estado.PUBLICADA,
            publicada_en=timezone.now(),
        )

    def test_listado_publico_solo_muestra_publicadas_vigentes(self):
        self.crear_oferta(titulo="Borrador oculto", estado=Oferta.Estado.BORRADOR)
        self.crear_oferta(
            titulo="Publicada vencida",
            estado=Oferta.Estado.PUBLICADA,
            fecha_cierre=timezone.localdate() - timedelta(days=1),
        )
        self.client.force_login(self.postulante_user)

        response = self.client.get(reverse("ofertas:publicas"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta.titulo)
        self.assertNotContains(response, "Borrador oculto")
        self.assertNotContains(response, "Publicada vencida")

    def test_listado_publico_filtra_por_modalidad(self):
        remoto = Modalidad.objects.create(nombre="Remoto")
        oferta_remota = self.crear_oferta(
            titulo="Oferta remota",
            estado=Oferta.Estado.PUBLICADA,
            modalidad=remoto,
            publicada_en=timezone.now(),
        )
        self.client.force_login(self.postulante_user)

        response = self.client.get(
            reverse("ofertas:publicas"),
            {"modalidad": remoto.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, oferta_remota.titulo)
        self.assertNotContains(response, self.oferta.titulo)

    def test_listado_publico_paginado(self):
        for indice in range(10):
            self.crear_oferta(
                titulo=f"Publicada {indice}",
                estado=Oferta.Estado.PUBLICADA,
                publicada_en=timezone.now(),
            )
        self.client.force_login(self.postulante_user)

        response = self.client.get(reverse("ofertas:publicas"), {"page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["page_obj"].object_list), 1)

    def test_detalle_incrementa_vistas(self):
        self.client.force_login(self.postulante_user)

        response = self.client.get(reverse("ofertas:detalle", args=[self.oferta.pk]))

        self.assertEqual(response.status_code, 200)
        self.oferta.refresh_from_db()
        self.assertEqual(self.oferta.vistas, 1)

    def test_detalle_de_borrador_no_es_visible(self):
        borrador = self.crear_oferta(
            titulo="Borrador oculto",
            estado=Oferta.Estado.BORRADOR,
        )
        self.client.force_login(self.postulante_user)

        response = self.client.get(reverse("ofertas:detalle", args=[borrador.pk]))

        self.assertEqual(response.status_code, 404)

    def test_postulacion_exitosa(self):
        self.client.force_login(self.postulante_user)

        response = self.client.post(
            reverse("ofertas:postular", args=[self.oferta.pk])
        )

        self.assertEqual(response.status_code, 302)
        postulacion = Postulacion.objects.get(
            oferta=self.oferta,
            postulante=self.perfil,
        )
        self.assertEqual(postulacion.estado, Postulacion.Estado.POSTULADO)

    def test_perfil_incompleto_no_permite_postular(self):
        user, _ = crear_postulante(
            email="incompleto@example.com",
            ci="7654321 LP",
            celular="+59170005002",
            completo=False,
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("ofertas:postular", args=[self.oferta.pk]),
            follow=True,
        )

        self.assertContains(response, "80 %")
        self.assertFalse(Postulacion.objects.exists())

    def test_perfil_sin_cv_no_permite_postular(self):
        user, _ = crear_postulante(
            email="sincv@example.com",
            ci="7654322 LP",
            celular="+59170005003",
            con_cv=False,
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("ofertas:postular", args=[self.oferta.pk]),
            follow=True,
        )

        self.assertContains(response, "CV cargado")
        self.assertFalse(Postulacion.objects.exists())

    def test_no_permite_postular_dos_veces(self):
        self.client.force_login(self.postulante_user)
        self.client.post(reverse("ofertas:postular", args=[self.oferta.pk]))

        response = self.client.post(
            reverse("ofertas:postular", args=[self.oferta.pk]),
            follow=True,
        )

        self.assertContains(response, "Ya postulaste")
        self.assertEqual(Postulacion.objects.count(), 1)

    def test_no_permite_postular_a_oferta_no_publicada(self):
        oferta = self.crear_oferta(
            titulo="Oferta en selección",
            estado=Oferta.Estado.EN_PROCESO_SELECCION,
        )
        self.client.force_login(self.postulante_user)

        response = self.client.post(
            reverse("ofertas:postular", args=[oferta.pk]),
            follow=True,
        )

        self.assertContains(response, "no está recibiendo postulaciones")
        self.assertFalse(Postulacion.objects.filter(oferta=oferta).exists())

    def test_no_permite_postular_a_oferta_vencida(self):
        oferta = self.crear_oferta(
            titulo="Oferta vencida",
            estado=Oferta.Estado.PUBLICADA,
            fecha_cierre=timezone.localdate() - timedelta(days=1),
        )
        self.client.force_login(self.postulante_user)

        response = self.client.post(
            reverse("ofertas:postular", args=[oferta.pk]),
            follow=True,
        )

        self.assertContains(response, "ya cerró sus postulaciones")
        self.assertFalse(Postulacion.objects.filter(oferta=oferta).exists())

    def test_mis_postulaciones_lista_solo_las_propias(self):
        Postulacion.objects.create(oferta=self.oferta, postulante=self.perfil)
        self.client.force_login(self.postulante_user)

        response = self.client.get(reverse("ofertas:mis_postulaciones"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta.titulo)
        self.assertEqual(len(response.context["page_obj"].object_list), 1)

    def test_sidebar_postulante_usa_rutas_reales(self):
        self.client.force_login(self.postulante_user)

        response = self.client.get(reverse("ofertas:publicas"))

        self.assertContains(response, reverse("ofertas:publicas"))
        self.assertContains(response, reverse("ofertas:mis_postulaciones"))

    def test_empresa_ve_detalle_solo_de_sus_ofertas(self):
        self.client.force_login(self.empresa_user)

        response = self.client.get(
            reverse("ofertas:empresa_detalle", args=[self.oferta.pk])
        )
        self.assertEqual(response.status_code, 200)

        otro_user, _ = crear_empresa(
            email="otra@example.com",
            nit="4000099",
            celular="+59170004999",
        )
        self.client.force_login(otro_user)

        response = self.client.get(
            reverse("ofertas:empresa_detalle", args=[self.oferta.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_empresa_ve_postulantes_en_su_oferta(self):
        Postulacion.objects.create(oferta=self.oferta, postulante=self.perfil)
        self.client.force_login(self.empresa_user)

        response = self.client.get(
            reverse("ofertas:empresa_detalle", args=[self.oferta.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.perfil.user.get_full_name())
        self.assertContains(response, "Postulado")

    def test_empresa_ve_presentacion_del_postulante(self):
        self.perfil.presentacion = "Me interesa aportar en proyectos de desarrollo."
        self.perfil.save(update_fields=["presentacion"])
        postulacion = Postulacion.objects.create(
            oferta=self.oferta,
            postulante=self.perfil,
        )
        self.client.force_login(self.empresa_user)

        response = self.client.get(
            reverse(
                "ofertas:empresa_postulante",
                args=[self.oferta.pk, postulacion.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Me interesa aportar en proyectos de desarrollo.")
        self.assertContains(response, "Presentación")

    def test_empresa_descarga_cv_de_su_postulante(self):
        postulacion = Postulacion.objects.create(
            oferta=self.oferta,
            postulante=self.perfil,
        )
        self.perfil.cv.save(
            "cv-prueba.pdf",
            ContentFile(b"%PDF-1.4 contenido de prueba"),
            save=True,
        )
        self.addCleanup(lambda: self.perfil.cv.delete(save=False))
        self.client.force_login(self.empresa_user)

        response = self.client.get(
            reverse(
                "ofertas:empresa_postulante_cv",
                args=[self.oferta.pk, postulacion.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_otra_empresa_no_descarga_cv(self):
        postulacion = Postulacion.objects.create(
            oferta=self.oferta,
            postulante=self.perfil,
        )
        self.perfil.cv.save(
            "cv-prueba.pdf",
            ContentFile(b"%PDF-1.4 contenido de prueba"),
            save=True,
        )
        self.addCleanup(lambda: self.perfil.cv.delete(save=False))
        otro_user, _ = crear_empresa(
            email="otra-cv@example.com",
            nit="4000098",
            celular="+59170004998",
        )
        self.client.force_login(otro_user)

        response = self.client.get(
            reverse(
                "ofertas:empresa_postulante_cv",
                args=[self.oferta.pk, postulacion.pk],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_postulante_retira_postulacion_no_vista(self):
        postulacion = Postulacion.objects.create(
            oferta=self.oferta,
            postulante=self.perfil,
        )
        self.client.force_login(self.postulante_user)

        response = self.client.post(
            reverse("ofertas:postulacion_retirar", args=[postulacion.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Postulacion.objects.filter(pk=postulacion.pk).exists())

    def test_no_retira_postulacion_ya_vista(self):
        postulacion = Postulacion.objects.create(
            oferta=self.oferta,
            postulante=self.perfil,
            estado=Postulacion.Estado.VISTO,
            visto_en=timezone.now(),
        )
        self.client.force_login(self.postulante_user)

        response = self.client.post(
            reverse("ofertas:postulacion_retirar", args=[postulacion.pk]),
            follow=True,
        )

        self.assertContains(response, "ya vio tu postulación")
        self.assertTrue(Postulacion.objects.filter(pk=postulacion.pk).exists())

    def test_abrir_perfil_marca_visto(self):
        postulacion = Postulacion.objects.create(
            oferta=self.oferta,
            postulante=self.perfil,
        )
        self.client.force_login(self.empresa_user)

        response = self.client.get(
            reverse(
                "ofertas:empresa_postulante",
                args=[self.oferta.pk, postulacion.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        postulacion.refresh_from_db()
        self.assertEqual(postulacion.estado, Postulacion.Estado.VISTO)
        self.assertIsNotNone(postulacion.visto_en)

    def test_empresa_avanza_estado_de_postulacion(self):
        postulacion = Postulacion.objects.create(
            oferta=self.oferta,
            postulante=self.perfil,
            estado=Postulacion.Estado.VISTO,
        )
        self.client.force_login(self.empresa_user)

        response = self.client.post(
            reverse(
                "ofertas:empresa_postulante_estado",
                args=[self.oferta.pk, postulacion.pk],
            ),
            {"estado": Postulacion.Estado.PRESELECCIONADO},
        )

        self.assertEqual(response.status_code, 302)
        postulacion.refresh_from_db()
        self.assertEqual(
            postulacion.estado,
            Postulacion.Estado.PRESELECCIONADO,
        )

    def test_empresa_no_puede_retroceder_estado(self):
        postulacion = Postulacion.objects.create(
            oferta=self.oferta,
            postulante=self.perfil,
            estado=Postulacion.Estado.ENTREVISTA,
        )
        self.client.force_login(self.empresa_user)

        response = self.client.post(
            reverse(
                "ofertas:empresa_postulante_estado",
                args=[self.oferta.pk, postulacion.pk],
            ),
            {"estado": Postulacion.Estado.POSTULADO},
            follow=True,
        )

        self.assertContains(response, "no está permitido")
        postulacion.refresh_from_db()
        self.assertEqual(postulacion.estado, Postulacion.Estado.ENTREVISTA)

    def test_empresa_inicia_seleccion_y_cierra(self):
        self.client.force_login(self.empresa_user)

        self.client.post(
            reverse("ofertas:empresa_accion", args=[self.oferta.pk]),
            {"accion": "iniciar_seleccion"},
        )
        self.oferta.refresh_from_db()
        self.assertEqual(
            self.oferta.estado,
            Oferta.Estado.EN_PROCESO_SELECCION,
        )

        self.client.post(
            reverse("ofertas:empresa_accion", args=[self.oferta.pk]),
            {"accion": "cerrar"},
        )
        self.oferta.refresh_from_db()
        self.assertEqual(self.oferta.estado, Oferta.Estado.CERRADA)

    def test_empresa_anula_oferta(self):
        self.client.force_login(self.empresa_user)

        self.client.post(
            reverse("ofertas:empresa_accion", args=[self.oferta.pk]),
            {"accion": "anular"},
        )

        self.oferta.refresh_from_db()
        self.assertEqual(self.oferta.estado, Oferta.Estado.ANULADA)
