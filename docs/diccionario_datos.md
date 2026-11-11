# Diccionario de datos — Oruro Trabaja

Motor: PostgreSQL 15 · Fuente de verdad: modelos Django (apps/platform, apps/recruitment).

Tablas ordenadas por módulo para reflejar la arquitectura del monolito:
cuentas/auditoría (plataforma) y luego el dominio de negocio (catálogos, empresas,
postulantes, ofertas). Las tablas administrativas del framework Django se listan al final.

## Módulo de cuentas y acceso

Credenciales, roles, OTP y registros pendientes.

### codigos_otp

Tabla `codigos_otp` — modelo `CodigoOTP` (app `accounts`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `user` | FK → `users` | sí | FK | Referencia a `users`. |
| `registro_pendiente` | FK → `registros_pendientes` | sí | FK | Referencia a `registros_pendientes`. |
| `celular` | VARCHAR(20) | no | — | Celular |
| `codigo_hash` | VARCHAR(128) | no | — | Código (hash) |
| `proposito` | VARCHAR(20) | no | valores: REGISTRO, REGISTRO_PENDIENTE | Propósito |
| `expira_en` | TIMESTAMP | no | — | Expira en |
| `intentos` | SMALLINT | no | — | Intentos |
| `consumido_en` | TIMESTAMP | sí | — | Consumido en |
| `ip` | INET | sí | — | IP |

### registros_pendientes

Tabla `registros_pendientes` — modelo `RegistroPendiente` (app `accounts`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `id` | UUID | no | PK · único · no editable | id |
| `ci` | VARCHAR(20) | no | — | Cédula de identidad |
| `nombres` | VARCHAR(150) | no | — | Nombres |
| `apellidos` | VARCHAR(150) | no | — | Apellidos |
| `celular` | VARCHAR(20) | no | único | Celular |
| `email` | VARCHAR(254) | no | — | Correo electrónico |
| `password_hash` | VARCHAR(128) | no | — | Contraseña (hash) |
| `expira_en` | TIMESTAMP | no | — | Expira en |
| `ip` | INET | sí | — | IP |

### roles

Tabla `roles` — modelo `Role` (app `accounts`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `codigo` | VARCHAR(20) | no | único · valores: SUPERADMIN, EMPRESA, POSTULANTE | Código |
| `nombre` | VARCHAR(80) | no | — | Nombre |

### users

Tabla `users` — modelo `User` (app `accounts`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `password` | VARCHAR(128) | no | — | Hash de la contraseña (bcrypt). |
| `last_login` | TIMESTAMP | sí | — | Último inicio de sesión. |
| `is_superuser` | BOOLEAN | no | — | Acceso total al panel de Django. |
| `first_name` | VARCHAR(150) | no | — | Nombres del usuario. |
| `last_name` | VARCHAR(150) | no | — | Apellidos del usuario. |
| `is_staff` | BOOLEAN | no | — | Puede entrar al panel admin de Django. |
| `is_active` | BOOLEAN | no | — | Cuenta activa (deshabilitar = cerrar sesión). |
| `date_joined` | TIMESTAMP | no | — | Fecha de alta en la plataforma. |
| `email` | VARCHAR(254) | no | único | Correo electrónico |
| `celular` | VARCHAR(20) | sí | único | Celular |
| `role` | FK → `roles` | no | FK | Referencia a `roles`. |
| `celular_verificado` | BOOLEAN | no | — | Celular verificado |

## Módulo de auditoría

Registro de acciones relevantes del dominio.

### audit_auditlog

Tabla `audit_auditlog` — modelo `AuditLog` (app `audit`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `usuario` | FK → `users` | sí | FK | Referencia a `users`. |
| `accion` | VARCHAR(20) | no | valores: CREAR, ACTUALIZAR, ELIMINAR, LOGIN, CAMBIO_ESTADO | accion |
| `tabla` | VARCHAR(64) | no | — | tabla |
| `registro_id` | INTEGER | sí | — | registro id |
| `datos_antes` | JSONB | sí | — | datos antes |
| `datos_despues` | JSONB | sí | — | datos despues |
| `ip` | INET | sí | — | ip |
| `fecha` | TIMESTAMP | no | no editable | fecha |

## Módulo de catálogos

Catálogos base del dominio.

### departamentos

Tabla `departamentos` — modelo `Departamento` (app `catalogos`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `nombre` | VARCHAR(80) | no | único | Nombre |

### habilidades

Tabla `habilidades` — modelo `Habilidad` (app `catalogos`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `nombre` | VARCHAR(120) | no | único | Nombre |

### idiomas

Tabla `idiomas` — modelo `Idioma` (app `catalogos`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `nombre` | VARCHAR(80) | no | único | Nombre |

### modalidades

Tabla `modalidades` — modelo `Modalidad` (app `catalogos`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `nombre` | VARCHAR(80) | no | único | Nombre |

### profesiones

Tabla `profesiones` — modelo `Profesion` (app `catalogos`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `nombre` | VARCHAR(120) | no | único | Nombre |

### rubros

Tabla `rubros` — modelo `Rubro` (app `catalogos`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `nombre` | VARCHAR(120) | no | único | Nombre |

### tipos_contrato

Tabla `tipos_contrato` — modelo `TipoContrato` (app `catalogos`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `nombre` | VARCHAR(80) | no | único | Nombre |

## Módulo de empresas

Registro y validación de empresas.

### empresas

Tabla `empresas` — modelo `Empresa` (app `empresas`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `user` | FK → `users` | no | único | Referencia a `users`. |
| `nit` | VARCHAR(20) | no | único | NIT |
| `razon_social` | VARCHAR(200) | no | — | Razón social |
| `rubro` | FK → `rubros` | no | FK | Referencia a `rubros`. |
| `representante_nombres` | VARCHAR(150) | no | — | Nombres del representante |
| `representante_apellidos` | VARCHAR(150) | no | — | Apellidos del representante |
| `representante_ci` | VARCHAR(20) | no | — | CI del representante |
| `direccion` | VARCHAR(255) | no | — | Dirección |
| `logo` | VARCHAR(100) · archivo | no | — | Logo |
| `descripcion` | TEXT | no | — | Descripción |
| `estado` | VARCHAR(30) | no | valores: PENDIENTE_VALIDACION, APROBADA, RECHAZADA, SUSPENDIDA | Estado |
| `motivo_rechazo` | TEXT | no | — | Motivo de rechazo |
| `revisada_por` | FK → `users` | sí | FK | Referencia a `users`. |
| `revisada_en` | TIMESTAMP | sí | — | Revisada en |

## Módulo de postulantes

Perfil, CV y completitud.

### experiencias

Tabla `experiencias` — modelo `Experiencia` (app `postulantes`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `profile` | FK → `postulante_profiles` | no | FK | Referencia a `postulante_profiles`. |
| `empresa` | VARCHAR(160) | no | — | Empresa |
| `cargo` | VARCHAR(160) | no | — | Cargo |
| `anos` | SMALLINT | no | — | Años |
| `descripcion` | TEXT | no | — | Descripción |

### formaciones

Tabla `formaciones` — modelo `Formacion` (app `postulantes`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `profile` | FK → `postulante_profiles` | no | FK | Referencia a `postulante_profiles`. |
| `titulo` | VARCHAR(160) | no | — | Título |
| `institucion` | VARCHAR(160) | no | — | Universidad o instituto |
| `anio_titulacion` | SMALLINT | no | — | Año de titulación |
| `nro_titulo` | VARCHAR(60) | no | — | Nro. de título nacional |

### postulante_habilidades

Tabla `postulante_habilidades` — modelo `PostulanteHabilidad` (app `postulantes`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `profile` | FK → `postulante_profiles` | no | FK | Referencia a `postulante_profiles`. |
| `habilidad` | FK → `habilidades` | no | FK | Referencia a `habilidades`. |
| `nivel` | VARCHAR(20) | no | valores: BASICO, INTERMEDIO, AVANZADO, EXPERTO | Nivel |

### postulante_idiomas

Tabla `postulante_idiomas` — modelo `PostulanteIdioma` (app `postulantes`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `profile` | FK → `postulante_profiles` | no | FK | Referencia a `postulante_profiles`. |
| `idioma` | FK → `idiomas` | no | FK | Referencia a `idiomas`. |
| `nivel` | VARCHAR(20) | no | valores: BASICO, INTERMEDIO, AVANZADO, EXPERTO | Nivel |

### postulante_profiles

Tabla `postulante_profiles` — modelo `PostulanteProfile` (app `postulantes`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `user` | FK → `users` | no | único | Referencia a `users`. |
| `ci` | VARCHAR(20) | no | único | Cédula de identidad |
| `foto` | VARCHAR(100) · archivo | no | — | Foto de perfil |
| `direccion` | VARCHAR(255) | no | — | Dirección |
| `fecha_nacimiento` | DATE | sí | — | Fecha de nacimiento |
| `presentacion` | TEXT | no | — | Presentación |
| `profesion` | FK → `profesiones` | sí | FK | Referencia a `profesiones`. |
| `cv` | VARCHAR(100) · archivo | no | — | CV en PDF |

## Módulo de ofertas

Ofertas, postulaciones y guardadas.

### oferta_habilidades

Tabla `oferta_habilidades` — modelo `OfertaHabilidad` (app `ofertas`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `oferta` | FK → `ofertas` | no | FK | Referencia a `ofertas`. |
| `habilidad` | FK → `habilidades` | no | FK | Referencia a `habilidades`. |
| `obligatoria` | BOOLEAN | no | — | Obligatoria |

### ofertas

Tabla `ofertas` — modelo `Oferta` (app `ofertas`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `empresa` | FK → `empresas` | no | FK | Referencia a `empresas`. |
| `titulo` | VARCHAR(200) | no | — | Título |
| `descripcion` | TEXT | no | — | Descripción |
| `requisitos_obligatorios` | TEXT | no | — | Requisitos obligatorios |
| `requisitos_deseables` | TEXT | no | — | Requisitos deseables |
| `anos_experiencia` | SMALLINT | no | — | Años de experiencia |
| `tipo_contrato` | FK → `tipos_contrato` | no | FK | Referencia a `tipos_contrato`. |
| `modalidad` | FK → `modalidades` | no | FK | Referencia a `modalidades`. |
| `departamento` | FK → `departamentos` | no | FK | Referencia a `departamentos`. |
| `municipio` | VARCHAR(120) | no | — | Municipio |
| `salario_min` | NUMERIC(12,2) | sí | — | Salario mínimo |
| `salario_max` | NUMERIC(12,2) | sí | — | Salario máximo |
| `a_tratar` | BOOLEAN | no | — | Salario a tratar |
| `beneficios` | TEXT | no | — | Beneficios |
| `fecha_cierre` | DATE | no | — | Fecha de cierre |
| `plazas` | SMALLINT | no | — | Número de plazas |
| `vistas` | INTEGER | no | — | Vistas |
| `estado` | VARCHAR(30) | no | valores: BORRADOR, EN_REVISION_GADOR, PUBLICADA, EN_PROCESO_SELECCION, CERRADA, ANULADA | Estado |
| `motivo_revision` | TEXT | no | — | Motivo de revisión |
| `publicada_en` | TIMESTAMP | sí | — | Publicada en |
| `revisada_por` | FK → `users` | sí | FK | Referencia a `users`. |
| `revisada_en` | TIMESTAMP | sí | — | Revisada en |

### ofertas_guardadas

Tabla `ofertas_guardadas` — modelo `OfertaGuardada` (app `ofertas`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `postulante` | FK → `postulante_profiles` | no | FK | Referencia a `postulante_profiles`. |
| `oferta` | FK → `ofertas` | no | FK | Referencia a `ofertas`. |

### postulaciones

Tabla `postulaciones` — modelo `Postulacion` (app `ofertas`).

| Campo | Tipo | Nulo | Restricciones | Descripción |
|---|---|---|---|---|
| `id` | BIGSERIAL · PK | no | PK · único | ID |
| `creado_en` | TIMESTAMP | no | no editable | Creado en |
| `actualizado_en` | TIMESTAMP | no | no editable | Actualizado en |
| `oferta` | FK → `ofertas` | no | FK | Referencia a `ofertas`. |
| `postulante` | FK → `postulante_profiles` | no | FK | Referencia a `postulante_profiles`. |
| `estado` | VARCHAR(20) | no | valores: POSTULADO, VISTO, PRESELECCIONADO, ENTREVISTA, FINALISTA, CONTRATADO, RECHAZADO | Estado |
| `visto_en` | TIMESTAMP | sí | — | Visto en |

## Tablas del framework Django

Tablas administrativas que Django crea y gestiona; no pertenecen al dominio.

| Tabla | Propósito |
|---|---|
| `auth_group` | Grupos de permisos de Django (no se usa el RBAC por grupos: los roles viven en `roles`). |
| `auth_permission` | Catálogo de permisos por modelo. |
| `django_content_type` | Registro de tipos de contenido (app · modelo). |
| `django_session` | Sesiones de usuario (backend de base de datos). |
| `django_admin_log` | Bitácora de acciones del panel admin de Django. |
