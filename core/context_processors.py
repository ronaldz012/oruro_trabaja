from django.conf import settings


def demo_mode(request):
    """Expone DEMO_MODE a todas las plantillas."""
    return {"DEMO_MODE": settings.DEMO_MODE}
