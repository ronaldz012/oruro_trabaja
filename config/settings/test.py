from .base import *

DEBUG = False
ALLOWED_HOSTS = ["*"]

DEMO_MODE = True  # los tests usan el backend demo por defecto

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Los tests siempre usan storage local, aunque el entorno apunte a R2/S3.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {"location": str(BASE_DIR / "media")},
    },
    "private": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": str(BASE_DIR / "private_media"),
            "base_url": None,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    },
}
