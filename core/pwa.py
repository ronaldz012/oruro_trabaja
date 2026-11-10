from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.templatetags.static import static

PWA_NAME = "Oruro Trabaja"
PWA_SHORT_NAME = "OruroTrabaja"
PWA_THEME_COLOR = "#7A1014"
PWA_BACKGROUND_COLOR = "#f7f7f7"


def manifest(request):
    """Manifiesto PWA de Oruro Trabaja."""
    data = {
        "id": "/",
        "name": PWA_NAME,
        "short_name": PWA_SHORT_NAME,
        "description": "Bolsa de trabajo de la Gobernación de Oruro.",
        "lang": "es-BO",
        "dir": "ltr",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "any",
        "background_color": PWA_BACKGROUND_COLOR,
        "theme_color": PWA_THEME_COLOR,
        "categories": ["jobs", "business"],
        "icons": [
            {
                "src": static("icons/icon-192.png"),
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": static("icons/icon-512.png"),
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": static("icons/maskable-512.png"),
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable",
            },
            {
                "src": static("icons/icon.svg"),
                "sizes": "any",
                "type": "image/svg+xml",
                "purpose": "any",
            },
        ],
    }
    return JsonResponse(
        data,
        json_dumps_params={"ensure_ascii": False},
        content_type="application/manifest+json",
    )


def service_worker(request):
    """Sirve el service worker desde la raíz para que controle todo el scope."""
    path = Path(settings.BASE_DIR) / "static" / "js" / "sw.js"
    if not path.exists():
        raise Http404("No existe el service worker.")

    response = FileResponse(path.open("rb"), content_type="application/javascript")
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache"
    return response


def offline(request):
    """Página de respaldo cuando no hay conexión."""
    return render(request, "pwa/offline.html")
