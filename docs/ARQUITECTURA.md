# Arquitectura — Bolsa de Trabajo GADOR

## Decisión

Monolito modular en Django, con dos módulos principales y un kernel compartido.

```text
core/                         # Kernel transversal, sin dependencias de dominio
apps/
  platform/
    accounts/                 # User, Role, OTP, login y permisos
    audit/                    # Auditoría transversal (servicio)
    notifications/            # Correos y notificaciones (servicio)
  recruitment/
    postulantes/              # Perfil, formación, experiencia, habilidades
    empresas/                 # Empresa y validación GADOR
    catalogos/                # Catálogos del dominio de empleo
    ofertas/                  # Ofertas, postulaciones y favoritas
  dashboard/                  # Presentación y read models
```

## Dirección de dependencias

```text
core         → no depende de nadie
platform     → core
recruitment  → core + platform/accounts
dashboard    → core + platform + recruitment
```

Reglas:

- `platform` no importa modelos de `recruitment`.
- `recruitment` puede referenciar `User` de `platform`.
- `dashboard` puede leer todos los módulos, pero ningún módulo depende de `dashboard`.
- `core` no conoce modelos de negocio.

## Módulos

### `core`

Infraestructura reutilizable:

- `TimeStampedModel`
- paginación
- permisos por rol
- excepciones de dominio
- storage privado
- normalizers
- context processors
- PWA: manifest, service worker y página offline

No es un módulo de negocio. Por eso vive fuera de `apps/`.

### `platform`

Identidad y servicios técnicos:

- `accounts`: usuario, roles, OTP, login, sesión.
- `audit`: registro de eventos de plataforma y negocio. Debe guardar `entity`/`entity_id`, no FKs directas a ofertas o postulaciones.
- `notifications`: correo y notificaciones internas. Puede depender de `User`.

### `recruitment`

Dominio de la bolsa de trabajo:

- `postulantes`: perfil del postulante y su hoja de vida.
- `empresas`: empresa, rubro y validación GADOR.
- `catalogos`: profesiones, habilidades, idiomas, rubros, contratos, modalidades y departamentos.
- `ofertas`: oferta, postulación y ofertas guardadas.

Los catálogos viven en `recruitment` porque todos sus consumidores pertenecen al dominio:

- perfil del postulante,
- perfil de la empresa,
- ofertas.

No se duplican catálogos entre módulos.

### `dashboard`

Módulo de presentación:

- dashboards por rol,
- selectores y agregaciones,
- reportes futuros.

Puede leer `platform` y `recruitment`, pero no debe ser importado por ellos.

## FKs entre módulos

Se mantienen las FKs porque aportan integridad referencial:

```text
PostulanteProfile.user       → accounts.User
Empresa.user                 → accounts.User
Oferta.empresa               → empresas.Empresa
Postulacion.postulante       → postulantes.PostulanteProfile
OfertaGuardada.postulante    → postulantes.PostulanteProfile
```

La regla es que la dependencia vaya en una sola dirección:

```text
recruitment → platform/accounts
```

Nunca al revés.

## App labels

Los `AppConfig` conservan los labels originales:

```python
name = "apps.recruitment.ofertas"
label = "ofertas"
```

Esto mantiene:

- `AUTH_USER_MODEL = "accounts.User"`
- dependencias de migraciones,
- nombres de tablas,
- URLs y namespaces.

## Auditoría y notificaciones

No viven en `core` porque no son primitivas. Tampoco en `recruitment` porque registran eventos de varios módulos.

Quedan en `platform`:

- `audit`: servicio `audit_action(...)`.
- `notifications`: servicio `notify(...)`.

`recruitment` los invoca desde sus casos de uso. `platform` no importa modelos de `recruitment`.

## Migraciones

El refactor no cambió tablas ni migraciones. Los movimientos preservan los app labels, por lo que:

```bash
python manage.py makemigrations --check --dry-run
```

debe responder `No changes detected`.

## Verificación del refactor

```bash
python manage.py check
python manage.py test --settings=config.settings.test
python manage.py makemigrations --check --dry-run
```
