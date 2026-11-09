# Oruro Trabaja

Bolsa de trabajo digital de la Gobernación de Oruro.

## Stack

- Django 6.1
- SQLite en desarrollo (soporte PostgreSQL previsto en un próximo release)
- Tailwind CSS 4
- HTMX
- Storage local o S3 compatible con Cloudflare R2

## Estructura

```text
core/                       # kernel transversal
apps/
  platform/
    accounts/               # User, Role, OTP, login
    audit/                  # auditoría (servicio)
    notifications/          # notificaciones y correos (servicio)
  recruitment/
    postulantes/            # perfil y hoja de vida
    empresas/               # empresa y validación GADOR
    catalogos/              # catálogos del dominio
    ofertas/                # ofertas, postulaciones y favoritas
  dashboard/                # presentación y read models
```

Ver `docs/ARQUITECTURA.md` para reglas de dependencia.

## Instalación

```bash
cp .env.example .env
# completar credenciales en .env

uv sync
npm install
npm run css:build

python manage.py migrate
python manage.py seed_catalogos
python manage.py seed_usuarios
python manage.py seed_empresas
python manage.py seed_ofertas

python manage.py runserver
```

## Tests

```bash
python manage.py test --settings=config.settings.test
python manage.py check
python manage.py makemigrations --check --dry-run
```

## Storage

### Local

```env
STORAGE_BACKEND=local
```

- Fotos públicas: `media/`
- CV privados: `private_media/`

### Cloudflare R2 / S3

```env
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=<bucket-publico>
AWS_PRIVATE_STORAGE_BUCKET_NAME=<bucket-privado>
AWS_S3_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
AWS_S3_REGION_NAME=auto
AWS_S3_CUSTOM_DOMAIN=
AWS_S3_ADDRESSING_STYLE=
AWS_S3_SIGNATURE_VERSION=s3v4
AWS_QUERYSTRING_EXPIRE=3600
```

- Las fotos usan el storage público.
- Los CV usan el storage privado.
- La descarga de CV sigue pasando por la vista con permisos.
- El seed usa el storage configurado porque guarda mediante `perfil.cv.save(...)`.
- Si cambiás de local a R2, los archivos existentes **no se migran solos**. Hay que correr el seed con el storage destino o migrar los archivos con un comando aparte.

## SMS con Textbee

Para enviar SMS reales:

```env
DEMO_MODE=False
TEXTBEE_API_KEY=...
TEXTBEE_DEVICE_ID=...
TEXTBEE_BASE_URL=https://api.textbee.dev/api/v1
TEXTBEE_TIMEOUT_SECONDS=10
```

El teléfono Android de Textbee debe estar online y con la app activa.

Prueba manual:

```bash
python manage.py probar_sms +59171234567
```

Con `DEMO_MODE=True` el código se muestra en la pantalla de verificación y no se envía SMS.

## Login

El login tiene throttle por IP, no bloquea cuentas:

- 5 intentos fallidos desde una IP → timeout de 15 minutos.
- Un login exitoso limpia el contador.
- El mensaje se muestra en el mismo formulario.

Variables:

```env
LOGIN_MAX_ATTEMPTS=5
LOGIN_TIMEOUT_SECONDS=900
```

En producción con varios workers, usar una cache compartida como Redis.

## Flujo de demo

1. Registrar empresa.
2. GADOR valida la empresa.
3. Empresa crea una oferta.
4. GADOR revisa y publica.
5. Registrar postulante y completar perfil + CV.
6. Postular a una oferta.
7. Empresa ve el postulante y descarga su CV.
8. Empresa cambia el estado de la postulación.
9. Postulante ve el estado en “Mis postulaciones”.

## Roadmap

- Soporte PostgreSQL como base de datos principal.
- Migrar el throttle de login a una cache compartida (Redis) en producción.
- Cambio de contraseña para usuarios autenticados.
- Recuperación de contraseña por email.
- Aplicación PWA instalable (manifest, service worker y página offline).
- Correos transaccionales con Brevo.
- Push notifications.
- Configurar buckets reales de R2/Cloudflare.
