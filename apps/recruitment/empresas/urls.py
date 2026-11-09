from django.urls import path

from apps.recruitment.empresas import views

app_name = "empresas"

urlpatterns = [
    path("registro/empresa/", views.registro, name="registro"),
    path("gador/empresas/", views.gador_lista, name="gador_lista"),
    path("gador/empresas/<int:pk>/", views.gador_detalle, name="gador_detalle"),
    path(
        "gador/empresas/<int:pk>/accion/",
        views.gador_accion,
        name="gador_accion",
    ),
]
