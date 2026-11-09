from django.urls import path

from apps.dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("gador/", views.dashboard_gador, name="gador"),
    path("gador/reportes/", views.reportes_gador, name="reportes"),
    path("empresa/", views.dashboard_empresa, name="empresa"),
    path("postulante/", views.dashboard_postulante, name="postulante"),
]
