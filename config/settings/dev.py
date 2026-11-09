from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# En desarrollo el OTP se muestra en pantalla y no se envía SMS real.
DEMO_MODE = env.bool("DEMO_MODE", default=True)

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}
