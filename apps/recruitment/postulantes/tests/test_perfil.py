from __future__ import annotations

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.platform.accounts.models import Role, User
from apps.recruitment.catalogos.models import Habilidad, Idioma, Profesion
from apps.recruitment.postulantes.models import (
    Experiencia,
    Formacion,
    PostulanteHabilidad,
    PostulanteIdioma,
    PostulanteProfile,
)
from apps.recruitment.postulantes.services import calcular_completitud


class PerfilTests(TestCase):
    def setUp(self):
        role = Role.objects.get(codigo=Role.Code.POSTULANTE)
        self.user = User.objects.create_user(
            email="perfil@example.com",
            password="ClaveSegura123!",
            role=role,
            celular="+59170001001",
        )
        self.perfil = PostulanteProfile.objects.create(
            user=self.user,
            ci="1111111 LP",
        )
        self.profesion = Profesion.objects.create(nombre="Ingeniero de Sistemas")
        self.habilidades = [
            Habilidad.objects.create(nombre=f"Habilidad {i}") for i in range(3)
        ]
        self.idioma = Idioma.objects.create(nombre="Inglés")
        self.client.force_login(self.user)

        self.addCleanup(self._limpiar_archivos)

    def _limpiar_archivos(self):
        self.perfil.refresh_from_db()
        if self.perfil.foto:
            self.perfil.foto.delete(save=False)
        if self.perfil.cv:
            self.perfil.cv.delete(save=False)

    def _completar_datos_personales(self):
        foto = SimpleUploadedFile(
            "foto.jpg",
            b"imagen-de-prueba",
            content_type="image/jpeg",
        )
        response = self.client.post(
            reverse("postulantes:perfil_datos"),
            {
                "direccion": "Calle 1 #123",
                "fecha_nacimiento": "1995-01-01",
                "profesion": self.profesion.pk,
                "foto": foto,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.perfil.refresh_from_db()

    def _agregar_formacion(self):
        response = self.client.post(
            reverse("postulantes:formacion_agregar"),
            {
                "titulo": "Ingeniero de Sistemas",
                "institucion": "Universidad Técnica de Oruro",
                "anio_titulacion": 2020,
                "nro_titulo": "UT-123",
            },
        )
        self.assertEqual(response.status_code, 302)

    def _agregar_experiencia(self):
        response = self.client.post(
            reverse("postulantes:experiencia_agregar"),
            {
                "empresa": "Empresa Demo",
                "cargo": "Desarrollador",
                "anos": 2,
                "descripcion": "Desarrollo web",
            },
        )
        self.assertEqual(response.status_code, 302)

    def _agregar_habilidades(self):
        for habilidad in self.habilidades:
            response = self.client.post(
                reverse("postulantes:habilidad_agregar"),
                {"nombre": habilidad.nombre, "nivel": "INTERMEDIO"},
            )
            self.assertEqual(response.status_code, 302)

    def _subir_cv(self):
        response = self.client.post(
            reverse("postulantes:perfil_cv"),
            {
                "cv": SimpleUploadedFile(
                    "cv.pdf",
                    b"%PDF-1.4 contenido de prueba",
                    content_type="application/pdf",
                )
            },
        )
        self.assertEqual(response.status_code, 302)
        self.perfil.refresh_from_db()

    def test_perfil_incompleto_no_puede_postular(self):
        completitud = calcular_completitud(self.perfil)

        self.assertEqual(completitud["porcentaje"], 0)
        self.assertFalse(completitud["puede_postular"])
        self.assertEqual(len(completitud["secciones"]), 6)
        self.assertIn("cv", completitud["por_clave"])
        self.assertFalse(completitud["por_clave"]["cv"]["completa"])

    def test_datos_personales_exige_foto_inicial(self):
        response = self.client.post(
            reverse("postulantes:perfil_datos"),
            {
                "direccion": "Calle 1 #123",
                "fecha_nacimiento": "1995-01-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "La foto de perfil es obligatoria.")
        self.perfil.refresh_from_db()
        self.assertFalse(self.perfil.foto)
        self.assertEqual(self.perfil.direccion, "")

    def test_no_guarda_direccion_vacia(self):
        self._completar_datos_personales()
        direccion_original = self.perfil.direccion

        response = self.client.post(
            reverse("postulantes:perfil_datos"),
            {
                "direccion": "",
                "fecha_nacimiento": "1995-01-01",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "La dirección es obligatoria.")
        self.perfil.refresh_from_db()
        self.assertEqual(self.perfil.direccion, direccion_original)

    def test_no_guarda_fecha_nacimiento_vacia(self):
        self._completar_datos_personales()

        response = self.client.post(
            reverse("postulantes:perfil_datos"),
            {
                "direccion": "Calle 1 #123",
                "fecha_nacimiento": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "La fecha de nacimiento es obligatoria.")
        self.perfil.refresh_from_db()
        self.assertIsNotNone(self.perfil.fecha_nacimiento)

    def test_permite_guardar_sin_reemplazar_foto_existente(self):
        self._completar_datos_personales()

        response = self.client.post(
            reverse("postulantes:perfil_datos"),
            {
                "direccion": "Nueva dirección 456",
                "fecha_nacimiento": "1996-02-02",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.perfil.refresh_from_db()
        self.assertEqual(self.perfil.direccion, "Nueva dirección 456")

    def test_guarda_presentacion(self):
        self._completar_datos_personales()
        texto = "Busco aportar en proyectos de desarrollo web."

        response = self.client.post(
            reverse("postulantes:perfil_datos"),
            {
                "direccion": "Calle 1 #123",
                "fecha_nacimiento": "1995-01-01",
                "presentacion": texto,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.perfil.refresh_from_db()
        self.assertEqual(self.perfil.presentacion, texto)

    def test_presentacion_maxima_600(self):
        self._completar_datos_personales()

        response = self.client.post(
            reverse("postulantes:perfil_datos"),
            {
                "direccion": "Calle 1 #123",
                "fecha_nacimiento": "1995-01-01",
                "presentacion": "a" * 601,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.perfil.refresh_from_db()
        self.assertEqual(self.perfil.presentacion, "")

    def test_porcentaje_no_retrocede_con_intento_invalido(self):
        self._completar_datos_personales()
        antes = calcular_completitud(self.perfil)["porcentaje"]

        self.client.post(
            reverse("postulantes:perfil_datos"),
            {
                "direccion": "",
                "fecha_nacimiento": "1995-01-01",
            },
        )

        self.perfil.refresh_from_db()
        despues = calcular_completitud(self.perfil)["porcentaje"]
        self.assertEqual(despues, antes)

    def test_perfil_core_sin_cv_no_permite_postular(self):
        self._completar_datos_personales()
        self._agregar_formacion()
        self._agregar_experiencia()
        self._agregar_habilidades()

        self.perfil.refresh_from_db()
        completitud = calcular_completitud(self.perfil)

        self.assertEqual(completitud["porcentaje"], 70)
        self.assertFalse(completitud["puede_postular"])

    def test_sin_cv_el_maximo_es_75(self):
        self._completar_datos_personales()
        self._agregar_formacion()
        self._agregar_experiencia()
        self._agregar_habilidades()
        self.client.post(
            reverse("postulantes:idioma_agregar"),
            {"nombre": self.idioma.nombre, "nivel": "AVANZADO"},
        )

        self.perfil.refresh_from_db()
        completitud = calcular_completitud(self.perfil)

        self.assertEqual(completitud["porcentaje"], 75)
        self.assertFalse(completitud["puede_postular"])

    def test_perfil_con_cv_sin_idiomas_permite_postular(self):
        self._completar_datos_personales()
        self._agregar_formacion()
        self._agregar_experiencia()
        self._agregar_habilidades()
        self._subir_cv()

        self.perfil.refresh_from_db()
        completitud = calcular_completitud(self.perfil)

        self.assertEqual(completitud["porcentaje"], 95)
        self.assertTrue(completitud["puede_postular"])

    def test_cv_e_idiomas_suman_extras(self):
        self._completar_datos_personales()
        self._agregar_formacion()
        self._agregar_experiencia()
        self._agregar_habilidades()
        self._subir_cv()
        self.client.post(
            reverse("postulantes:idioma_agregar"),
            {"nombre": self.idioma.nombre, "nivel": "AVANZADO"},
        )

        self.perfil.refresh_from_db()
        completitud = calcular_completitud(self.perfil)

        self.assertEqual(completitud["porcentaje"], 100)
        self.assertTrue(completitud["puede_postular"])

    def test_falta_de_habilidades_bloquea_postulacion(self):
        self._completar_datos_personales()
        self._agregar_formacion()
        self._agregar_experiencia()
        self._subir_cv()
        self.client.post(
            reverse("postulantes:idioma_agregar"),
            {"nombre": self.idioma.nombre, "nivel": "AVANZADO"},
        )

        self.perfil.refresh_from_db()
        completitud = calcular_completitud(self.perfil)

        self.assertEqual(completitud["porcentaje"], 80)
        self.assertFalse(completitud["puede_postular"])

    def test_pagina_perfil_muestra_progreso(self):
        response = self.client.get(reverse("postulantes:perfil"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mi perfil")
        self.assertContains(response, "0%")
        self.assertContains(response, "Falta para postular")
        self.assertContains(response, "Pendiente · 20 %")
        self.assertContains(response, "0 de 3 · 20 %")
        self.assertContains(response, "Opcional · 5 %")
        self.assertNotContains(response, "Completa · 25 %")

    def test_pagina_perfil_marca_seccion_completa(self):
        self._completar_datos_personales()
        self._subir_cv()
        self.agregar_habilidades = self._agregar_habilidades()

        response = self.client.get(reverse("postulantes:perfil"))

        self.assertContains(response, "Completa · 25 %")
        self.assertContains(response, "Completa · 10 %")
        self.assertContains(response, "Completa · 20 %")
        self.assertNotContains(response, "0 de 3 · 20 %")
        self.assertNotContains(response, "Pendiente · Obligatorio")

    def test_dashboard_muestra_completitud(self):
        response = self.client.get(reverse("dashboard:postulante"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "0 % completo")

    def test_cv_se_descarga_solo_para_el_dueno(self):
        self._subir_cv()

        response = self.client.get(reverse("postulantes:perfil_cv_descargar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

        otro = User.objects.create_user(
            email="otro@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.POSTULANTE),
            celular="+59170001002",
        )
        PostulanteProfile.objects.create(user=otro, ci="2222222 OR")
        self.client.force_login(otro)

        response = self.client.get(reverse("postulantes:perfil_cv_descargar"))
        self.assertEqual(response.status_code, 404)

    def test_cv_invalido_no_se_guarda(self):
        response = self.client.post(
            reverse("postulantes:perfil_cv"),
            {
                "cv": SimpleUploadedFile(
                    "cv.txt",
                    b"no es un pdf",
                    content_type="text/plain",
                )
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El CV debe ser un archivo PDF.")
        self.perfil.refresh_from_db()
        self.assertFalse(self.perfil.cv)

    def test_empresa_no_puede_entrar_al_perfil(self):
        empresa = User.objects.create_user(
            email="empresa@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.EMPRESA),
            celular="+59170001003",
        )
        self.client.force_login(empresa)

        response = self.client.get(reverse("postulantes:perfil"))
        self.assertEqual(response.status_code, 403)

    def test_anonimo_redirige_al_login(self):
        self.client.logout()
        response = self.client.get(reverse("postulantes:perfil"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('postulantes:perfil')}",
            fetch_redirect_response=False,
        )

    def test_usuario_sin_perfil_redirige_al_dashboard(self):
        user = User.objects.create_user(
            email="sinperfil@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.POSTULANTE),
            celular="+59170001004",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("postulantes:perfil"))
        self.assertRedirects(
            response,
            reverse("dashboard:postulante"),
            fetch_redirect_response=False,
        )

    def test_eliminar_formacion(self):
        self._agregar_formacion()
        Formacion.objects.create(
            profile=self.perfil,
            titulo="Técnico Superior",
            institucion="Instituto Demo",
            anio_titulacion=2021,
        )
        formacion = Formacion.objects.first()

        response = self.client.post(
            reverse("postulantes:formacion_eliminar", args=[formacion.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Formacion.objects.filter(pk=formacion.pk).exists())
        self.assertEqual(Formacion.objects.filter(profile=self.perfil).count(), 1)

    def test_no_elimina_ultima_formacion(self):
        self._agregar_formacion()
        formacion = Formacion.objects.get(profile=self.perfil)

        response = self.client.post(
            reverse("postulantes:formacion_eliminar", args=[formacion.pk]),
            follow=True,
        )

        self.assertContains(response, "al menos una formación")
        self.assertTrue(Formacion.objects.filter(pk=formacion.pk).exists())

    def test_ui_oculta_eliminar_ultima_formacion(self):
        self._agregar_formacion()
        formacion = Formacion.objects.get(profile=self.perfil)

        response = self.client.get(reverse("postulantes:perfil"))

        self.assertNotContains(
            response,
            reverse("postulantes:formacion_eliminar", args=[formacion.pk]),
        )

    def test_htmx_informa_error_al_no_eliminar_ultima_formacion(self):
        self._agregar_formacion()
        formacion = Formacion.objects.get(profile=self.perfil)

        response = self.client.post(
            reverse("postulantes:formacion_eliminar", args=[formacion.pk]),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('"nivel": "error"', response["HX-Trigger"])
        self.assertTrue(Formacion.objects.filter(pk=formacion.pk).exists())

    def test_no_elimina_ultima_experiencia(self):
        self._agregar_experiencia()
        experiencia = Experiencia.objects.get(profile=self.perfil)

        response = self.client.post(
            reverse("postulantes:experiencia_eliminar", args=[experiencia.pk]),
            follow=True,
        )

        self.assertContains(response, "al menos una experiencia")
        self.assertTrue(Experiencia.objects.filter(pk=experiencia.pk).exists())

    def test_elimina_experiencia_si_hay_dos(self):
        self._agregar_experiencia()
        Experiencia.objects.create(
            profile=self.perfil,
            empresa="Otra empresa",
            cargo="Analista",
            anos=1,
        )
        experiencia = Experiencia.objects.first()

        response = self.client.post(
            reverse("postulantes:experiencia_eliminar", args=[experiencia.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Experiencia.objects.filter(pk=experiencia.pk).exists())
        self.assertEqual(Experiencia.objects.filter(profile=self.perfil).count(), 1)

    def test_no_elimina_habilidad_si_quedan_tres(self):
        self._agregar_habilidades()
        habilidad = PostulanteHabilidad.objects.first()

        response = self.client.post(
            reverse("postulantes:habilidad_eliminar", args=[habilidad.pk]),
            follow=True,
        )

        self.assertContains(response, "al menos 3 habilidades")
        self.assertTrue(PostulanteHabilidad.objects.filter(pk=habilidad.pk).exists())

    def test_ui_oculta_eliminar_habilidad_con_tres(self):
        self._agregar_habilidades()
        habilidad = PostulanteHabilidad.objects.first()

        response = self.client.get(reverse("postulantes:perfil"))

        self.assertNotContains(
            response,
            reverse("postulantes:habilidad_eliminar", args=[habilidad.pk]),
        )

    def test_elimina_habilidad_si_hay_cuatro(self):
        self._agregar_habilidades()
        self.client.post(
            reverse("postulantes:habilidad_agregar"),
            {"nombre": "Extra", "nivel": "BASICO"},
        )
        habilidad = PostulanteHabilidad.objects.first()

        response = self.client.post(
            reverse("postulantes:habilidad_eliminar", args=[habilidad.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(PostulanteHabilidad.objects.filter(pk=habilidad.pk).exists())
        self.assertEqual(
            PostulanteHabilidad.objects.filter(profile=self.perfil).count(),
            3,
        )

    def test_no_se_puede_eliminar_cv(self):
        self._subir_cv()

        response = self.client.post("/postulante/perfil/cv/eliminar/")

        self.assertEqual(response.status_code, 404)
        self.perfil.refresh_from_db()
        self.assertTrue(self.perfil.cv)

    def test_reemplazar_cv_elimina_archivo_anterior(self):
        self._subir_cv()
        self.perfil.refresh_from_db()
        archivo_anterior = self.perfil.cv.name
        storage = self.perfil.cv.storage

        response = self.client.post(
            reverse("postulantes:perfil_cv"),
            {
                "cv": SimpleUploadedFile(
                    "cv-nuevo.pdf",
                    b"%PDF-1.4 contenido nuevo",
                    content_type="application/pdf",
                )
            },
        )

        self.assertEqual(response.status_code, 302)
        self.perfil.refresh_from_db()
        self.assertNotEqual(self.perfil.cv.name, archivo_anterior)
        self.assertFalse(storage.exists(archivo_anterior))
        self.assertTrue(storage.exists(self.perfil.cv.name))

    def test_habilidad_duplicada_actualiza_nivel_sin_error(self):
        self.client.post(
            reverse("postulantes:habilidad_agregar"),
            {"nombre": "SQL", "nivel": "BASICO"},
        )
        response = self.client.post(
            reverse("postulantes:habilidad_agregar"),
            {"nombre": "sql", "nivel": "AVANZADO"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            PostulanteHabilidad.objects.filter(profile=self.perfil).count(),
            1,
        )
        habilidad = PostulanteHabilidad.objects.get(profile=self.perfil)
        self.assertEqual(habilidad.nivel, "AVANZADO")
        self.assertEqual(
            Habilidad.objects.filter(nombre__iexact="sql").count(),
            1,
        )

    def test_habilidad_texto_libre_crea_catalogo(self):
        response = self.client.post(
            reverse("postulantes:habilidad_agregar"),
            {"nombre": "Soldadura", "nivel": "INTERMEDIO"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Habilidad.objects.filter(nombre="Soldadura").exists())
        self.assertTrue(
            PostulanteHabilidad.objects.filter(
                profile=self.perfil,
                habilidad__nombre="Soldadura",
            ).exists()
        )

    def test_idioma_texto_libre_crea_catalogo(self):
        response = self.client.post(
            reverse("postulantes:idioma_agregar"),
            {"nombre": "Francés", "nivel": "BASICO"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Idioma.objects.filter(nombre="Francés").exists())
        self.assertTrue(
            PostulanteIdioma.objects.filter(
                profile=self.perfil,
                idioma__nombre="Francés",
            ).exists()
        )

    def test_no_elimina_ultimo_idioma(self):
        self.client.post(
            reverse("postulantes:idioma_agregar"),
            {"nombre": self.idioma.nombre, "nivel": "AVANZADO"},
        )
        idioma = PostulanteIdioma.objects.get(profile=self.perfil)

        response = self.client.post(
            reverse("postulantes:idioma_eliminar", args=[idioma.pk]),
            follow=True,
        )

        self.assertContains(response, "al menos un idioma")
        self.assertTrue(PostulanteIdioma.objects.filter(pk=idioma.pk).exists())

    def test_elimina_idioma_si_hay_dos(self):
        PostulanteIdioma.objects.create(
            profile=self.perfil,
            idioma=self.idioma,
            nivel="AVANZADO",
        )
        otro_idioma = Idioma.objects.create(nombre="Portugués")
        PostulanteIdioma.objects.create(
            profile=self.perfil,
            idioma=otro_idioma,
            nivel="BASICO",
        )
        idioma = PostulanteIdioma.objects.first()

        response = self.client.post(
            reverse("postulantes:idioma_eliminar", args=[idioma.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(PostulanteIdioma.objects.filter(pk=idioma.pk).exists())
        self.assertEqual(
            PostulanteIdioma.objects.filter(profile=self.perfil).count(),
            1,
        )

    def test_ui_oculta_eliminar_ultimo_idioma(self):
        PostulanteIdioma.objects.create(
            profile=self.perfil,
            idioma=self.idioma,
            nivel="AVANZADO",
        )
        idioma = PostulanteIdioma.objects.get(profile=self.perfil)

        response = self.client.get(reverse("postulantes:perfil"))

        self.assertNotContains(
            response,
            reverse("postulantes:idioma_eliminar", args=[idioma.pk]),
        )

    def test_profesion_no_esta_en_datos_personales(self):
        response = self.client.get(reverse("postulantes:perfil"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'name="profesion"')

    def test_htmx_devuelve_trigger_de_actualizacion(self):
        response = self.client.post(
            reverse("postulantes:habilidad_agregar"),
            {"nombre": "Excel", "nivel": "INTERMEDIO"},
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("HX-Trigger", response)
        self.assertIn("perfilActualizado", response["HX-Trigger"])
        self.assertContains(response, 'id="seccion-habilidades"')

    def test_empresa_no_puede_entrar_a_empleos(self):
        empresa = User.objects.create_user(
            email="empresa2@example.com",
            password="ClaveSegura123!",
            role=Role.objects.get(codigo=Role.Code.EMPRESA),
            celular="+59170001005",
        )
        self.client.force_login(empresa)

        response = self.client.get(reverse("ofertas:publicas"))
        self.assertEqual(response.status_code, 403)
