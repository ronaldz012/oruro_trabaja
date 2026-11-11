from django.urls import path

from apps.platform.audit import views

app_name = "audit"

urlpatterns = [
    path("gador/auditoria/", views.lista, name="lista"),
    path("gador/auditoria/<int:pk>/", views.detalle, name="detalle"),
]
