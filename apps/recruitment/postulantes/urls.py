from django.urls import path

from apps.recruitment.postulantes import views

app_name = "postulantes"

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("registro/verificar/", views.verificar_celular, name="verificar_celular"),
    path("registro/reenviar/", views.reenviar_codigo, name="reenviar_codigo"),
    path("registro/cambiar-celular/", views.cambiar_celular, name="cambiar_celular"),
    path("postulante/perfil/", views.perfil, name="perfil"),
    path("postulante/perfil/datos/", views.perfil_datos, name="perfil_datos"),
    path("postulante/perfil/cv/", views.perfil_cv, name="perfil_cv"),
    path("postulante/perfil/cv/descargar/", views.perfil_cv_descargar, name="perfil_cv_descargar"),
    path("postulante/perfil/formacion/agregar/", views.formacion_agregar, name="formacion_agregar"),
    path("postulante/perfil/formacion/<int:pk>/eliminar/", views.formacion_eliminar, name="formacion_eliminar"),
    path("postulante/perfil/experiencia/agregar/", views.experiencia_agregar, name="experiencia_agregar"),
    path("postulante/perfil/experiencia/<int:pk>/eliminar/", views.experiencia_eliminar, name="experiencia_eliminar"),
    path("postulante/perfil/habilidad/agregar/", views.habilidad_agregar, name="habilidad_agregar"),
    path("postulante/perfil/habilidad/<int:pk>/eliminar/", views.habilidad_eliminar, name="habilidad_eliminar"),
    path("postulante/perfil/idioma/agregar/", views.idioma_agregar, name="idioma_agregar"),
    path("postulante/perfil/idioma/<int:pk>/eliminar/", views.idioma_eliminar, name="idioma_eliminar"),
]
