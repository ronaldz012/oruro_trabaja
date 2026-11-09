from django.contrib import admin

from apps.recruitment.empresas.models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "nit", "rubro", "estado", "creado_en")
    list_filter = ("estado", "rubro")
    search_fields = ("razon_social", "nit", "user__email")
    readonly_fields = ("revisada_por", "revisada_en", "creado_en", "actualizado_en")
