from django.urls import path

from apps.recruitment.ofertas import views

app_name = "ofertas"

urlpatterns = [
    path("empleos/", views.publicas, name="publicas"),
    path("empleos/<int:pk>/", views.detalle, name="detalle"),
    path("empleos/<int:pk>/postular/", views.postular, name="postular"),
    path("empleos/<int:pk>/guardar/", views.guardar, name="guardar"),
    path(
        "postulante/postulaciones/",
        views.mis_postulaciones,
        name="mis_postulaciones",
    ),
    path(
        "postulante/postulaciones/<int:pk>/retirar/",
        views.postulacion_retirar,
        name="postulacion_retirar",
    ),
    path("empresa/ofertas/", views.empresa_lista, name="empresa_lista"),
    path("empresa/ofertas/nueva/", views.empresa_crear, name="empresa_crear"),
    path(
        "empresa/ofertas/<int:pk>/",
        views.empresa_detalle,
        name="empresa_detalle",
    ),
    path(
        "empresa/ofertas/<int:pk>/accion/",
        views.empresa_accion,
        name="empresa_accion",
    ),
    path(
        "empresa/ofertas/<int:pk>/editar/",
        views.empresa_editar,
        name="empresa_editar",
    ),
    path(
        "empresa/ofertas/<int:pk>/enviar/",
        views.empresa_enviar,
        name="empresa_enviar",
    ),
    path(
        "empresa/ofertas/<int:pk>/postulantes/<int:postulacion_pk>/",
        views.empresa_postulante,
        name="empresa_postulante",
    ),
    path(
        "empresa/ofertas/<int:pk>/postulantes/<int:postulacion_pk>/estado/",
        views.empresa_postulante_estado,
        name="empresa_postulante_estado",
    ),
    path(
        "empresa/ofertas/<int:pk>/postulantes/<int:postulacion_pk>/cv/",
        views.empresa_postulante_cv,
        name="empresa_postulante_cv",
    ),
    path("gador/ofertas/", views.gador_lista, name="gador_lista"),
    path("gador/ofertas/<int:pk>/", views.gador_detalle, name="gador_detalle"),
    path(
        "gador/ofertas/<int:pk>/accion/",
        views.gador_accion,
        name="gador_accion",
    ),
]
