from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.platform.accounts import views as account_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.platform.accounts.urls")),
    path("", include("apps.recruitment.empresas.urls")),
    path("", include("apps.recruitment.catalogos.urls")),
    path("", include("apps.recruitment.ofertas.urls")),
    path("", include("apps.recruitment.postulantes.urls")),
    path("", account_views.home, name="home"),
    path("", include("apps.dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)