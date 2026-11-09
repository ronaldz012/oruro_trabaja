from django.urls import path

from apps.recruitment.catalogos import views

app_name = "catalogos"

urlpatterns = [
    path("gador/catalogos/", views.gador_lista, name="gador_lista"),
]
