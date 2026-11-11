# Oruro Trabaja

Bolsa de trabajo digital de la Gobernación Autónoma Departamental de Oruro.
Los postulantes registran su perfil y hoja de vida, las empresas publican
ofertas y GADOR valida, publica y audita todo el proceso.

## Entregables

| Entregable | Enlace |
|---|---|
| Demo en vivo | https://demo-gador.ronaldzepita.com |
| Video de demostración (2 min) | https://youtu.be/sa92ydyRYA8 |
| Manual de usuario | docs/manual_usuario.pdf |
| Manual técnico | docs/manual_tecnico.pdf |
| Diccionario de datos (PDF) | docs/diccionario_datos.pdf |
| Diccionario de datos (fuente) | docs/diccionario_datos.md |
| Dump de la base de datos | docs/oruro_trabaja.sql |
| Arquitectura | docs/ARQUITECTURA.md |

Las credenciales de la demo se envían en el correo de presentación y no se
versionan en este repositorio. Los evaluadores también pueden registrarse con
su propio celular.

## Objetivo del sistema

El registro de empresas y la publicación de ofertas laborales de la Gobernación
de Oruro dependen hoy de formularios en papel y revisiones manuales. Eso hace
lento el proceso, deja la información dispersa y no deja ningún registro
verificable de quién autorizó qué.

Oruro Trabaja digitaliza el ciclo completo. Una empresa se registra y queda
pendiente de validación; una vez validada por GADOR crea sus ofertas, que
también pasan por revisión institucional antes de ser públicas. El postulante
arma su perfil con CV obligatorio, postula y sigue el estado de cada proceso.
La empresa revisa las postulaciones y las mueve hasta el contrato.

Cada acción relevante (validaciones, publicaciones, cambios de estado) queda
registrada en una auditoría con los datos anteriores y posteriores, visible
desde el panel de GADOR.

## Decisiones de diseño

- **Django como monolito modular.** Proyecto de una persona con plazo corto:
  un solo deploy y un solo runtime. La modularidad está en la disciplina, apps
  por dominio con dependencias en una sola dirección y un kernel compartido
  (core/), de modo que si el sistema crece se puede dividir en servicios sin
  reescribirlo.
- **Server rendered con HTMX, sin SPA.** La interactividad real del producto
  son cuatro o cinco puntos: perfil que se guarda en vivo, tags de habilidades,
  wizard de ofertas y notificaciones. HTMX los resuelve sin build de frontend
  ni doble estado: menos código y menos superficie de bugs.
- **Tailwind.** Sistema de diseño rápido y consistente, sin CSS custom grande.
- **SQLite en desarrollo, PostgreSQL en producción, por configuración.** El
  juez levanta el sistema local sin instalar nada de base de datos; el server
  corre el mismo esquema en Postgres. La selección vive en el .env.
- **Cloudflare R2 para archivos.** Compatible S3 y sin costo de salida. Las
  fotos de perfil y logos son públicas; los CV nunca se exponen: se descargan
  solo por URL firmada con expiración.
- **Verificación por OTP con modo demo.** El celular verifica identidad mejor
  que el correo y no exige infraestructura de email. DEMO_MODE muestra el
  código en pantalla para que el flujo sea evaluable sin SMS real.
- **Perfil con completitud y CV obligatorio (más de 80 por ciento).** Protege
  a las empresas de postulaciones sin contenido. Cada sección muestra un check
  o un aviso con lo que falta, para que el usuario no se pierda en el proceso.
- **Auditoría desde el día uno.** Registro JSON antes y después en cada acción
  que importa, consultable en el panel de GADOR.
- **PWA.** Instalable en el celular, con service worker y página offline,
  pensada para usuarios con conexiones intermitentes.
- **Seeds idempotentes.** La demo es repetible y restaurable con comandos, sin
  datos de prueba quemados en el código.

## Estructura

```text
core/                       kernel transversal (modelos base, permisos, storage)
apps/platform/              cuentas, auditoría, notificaciones
apps/recruitment/           catálogos, empresas, postulantes, ofertas
apps/dashboard/             paneles por rol y reportes
templates/, static/, assets/  interfaz y estilos
docs/                       manuales, diagrama, dump SQL y diccionario
```

El detalle de la arquitectura y las reglas de dependencia está en
docs/ARQUITECTURA.md.

## Ejecución en local

```bash
cp .env.example .env         # completar las claves de seed
uv sync

python manage.py migrate
python manage.py seed_catalogos
python manage.py seed_usuarios
python manage.py seed_empresas
python manage.py seed_ofertas

python manage.py runserver
```

Corre en SQLite con DEMO_MODE=True: el código de verificación se muestra en
pantalla y no se envía ningún SMS. Los seeds cargan catálogos, usuarios,
empresas y ofertas de demostración.

## Pruebas

```bash
python manage.py test --settings=config.settings.test
```

159 tests sobre modelos, casos de uso, vistas, permisos, auditoría, storage y
SMS. Verificados en SQLite y en PostgreSQL 15.

## Despliegue

La demo corre en un VPS simple en Vultr, región Chile, para tener bajo ping
desde Oruro y Bolivia. Ubuntu con PostgreSQL, Gunicorn (un worker), Nginx y
HTTPS con Let's Encrypt, sin contenedores. El detalle operativo está en el
manual técnico.

## Siguientes pasos

1. Redis como cache compartida si se escala a más de un worker.
2. CAPTCHA en el registro público.
3. Notificaciones push de la PWA y correos transaccionales.
4. Empaquetar la PWA como TWA para publicarla en Google Play.
5. Separar los buckets de R2 en público y privado para producción real.

## Limitaciones de la versión demo

- Cambio de contraseña y recuperación por correo: visibles pero deshabilitados
  en el panel "Mi cuenta".
- El código de verificación se muestra en pantalla (modo demo).
- El bloqueo de intentos de login usa cache en proceso: válido con un worker.

---

Desarrollado por Ronald Zepita. Contacto y portfolio: ronaldzepita.com · hi@ronaldzepita.com
