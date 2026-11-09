# GOBIERNO AUTÓNOMO DEPARTAMENTAL DE ORURO
## SECRETARÍA DEPARTAMENTAL DE PLANIFICACIÓN Y DESARROLLO
### UNIDAD DE SISTEMAS E INFORMÁTICA - G.A.D.O.R.

---

# SISTEMA COMPLETO: BOLSA DE TRABAJO DEPARTAMENTAL DIGITAL
**PWA Responsive | Stack: Laravel / Django / NestJS + PostgreSQL/MySQL**

## OBJETIVO GENERAL:
Conectar postulantes orureños con empresas validadas por la Gobernación, con trazabilidad, transparencia y reportes oficiales para la toma de decisiones.

**Roles:** SuperAdmin GADOR | Empresa | Postulante

---

## MÓDULO 1: GESTIÓN DE POSTULANTES Y HOJA DE VIDA DIGITAL
**Objetivo:** Registro Validador y CV digital estructurado.

* **RF01 - Registro y Login:**
  Registro con CI, Nombre completo, Celular (validación OTP), Email, Contraseña segura. Login con bloqueo por 5 intentos, recuperación por email, cambio de contraseña. JWT o Session.
* **RF02 - Perfil Postulante Completo:**
  Datos personales, foto perfil, dirección, fecha nacimiento. Formación académica: Título (Ing. Sistemas, Informática, Software, Técnico Superior en Sistemas Informáticos y afines), Universidad/Instituto, Año titulación, Nro. Título Nacional. Experiencia laboral (Empresa, Cargo, Años, Descripción). Habilidades (ej: Laravel, Python, Redes) con nivel. Idiomas. CV en PDF obligatorio (máx 5MB). Porcentaje de completitud de perfil (0-100%).
* **RF03 - Buscador de Empleo:**
  Ver ofertas publicadas con paginación, filtros por palabra clave, profesión, salario, ubicación, modalidad. Guardar ofertas como favoritas.
* **RF04 - Mi Historial de Postulaciones:**
  Listado de todas mis postulaciones con estado y fecha. Ver detalle de oferta. Retirar postulación si aún no fue vista.

---

## MÓDULO 2: GESTIÓN DE EMPRESAS Y PUBLICACIÓN DE OFERTAS
**Objetivo:** Empresas validadas y ofertas con flujo de aprobación GADOR.

* **RF05 - Registro Empresa:**
  NIT, Razón Social, Rubro (Minería, Tecnología, Comercio, Salud, Educación, etc), Representante Legal, CI Representante, Celular, Email corporativo, Dirección, Logo (PNG/JPG), Descripción empresa. Estado inicial: `PENDIENTE_VALIDACION`.
* **RF06 - Validación por SuperAdmin GADOR:**
  Panel para aprobar/rechazar empresas. Ver documentos, motivo de rechazo. Solo empresas APROBADAS pueden publicar ofertas. Puede suspender empresa.
* **RF07 - CRUD de Ofertas Laborales:**
  Campos: Título (ej: Desarrollador Full Stack), Descripción larga, Requisitos obligatorios, Requisitos deseables, Profesión requerida (puede seleccionar varias), Años experiencia, Tipo contrato (Indefinido, Plazo fijo, Pasantía, Consultoría), Modalidad (Presencial, Remoto, Híbrido), Departamento/Municipio, Salario (Min-Max o A tratar), Beneficios, Fecha cierre, Número de plazas. Validaciones backend.
* **RF08 - Flujo de Estados de Oferta:**
  `BORRADOR` -> `EN_REVISION_GADOR` -> `PUBLICADA` -> `EN_PROCESO_SELECCION` -> `CERRADA/ANULADA`. GADOR aprueba ofertas antes de publicar. Empresa puede editar solo en `BORRADOR`. Duplicar oferta para republicar.
* **RF09 - Panel Empresa Mis Ofertas:**
  Tabla con total vistas, total postulantes, estado, acciones. Límite configurable de ofertas activas (ej: 5).

---

## MÓDULO 3: POSTULACIONES, ADMINISTRACIÓN GADOR, REPORTES Y SISTEMA
**Objetivo:** Cierre del ciclo laboral con transparencia, trazabilidad y reportes.

* **RF10 - Motor de Postulación:**
  Botón Postular en 1 click. Validaciones: Perfil >80% completo, no haber postulado antes a misma oferta, oferta aún PUBLICADA y dentro de fecha. Cálculo automático de % MATCH entre habilidades del postulante y requisitos de oferta.
* **RF11 - Gestión de Postulantes por Empresa:**
  Por cada oferta, listar postulantes ordenados por % MATCH descendente. Ver ficha rápida: Nombre, Foto, Profesión, Años experiencia, % Match. Click para ver perfil completo y descargar CV PDF. Cambiar estado: `POSTULADO` -> `VISTO` -> `PRESELECCIONADO` -> `ENTREVISTA` -> `FINALISTA` -> `CONTRATADO` / `RECHAZADO`.
* **RF12 - Notificaciones Automáticas:**
  Email + Notificación PWA + WhatsApp (opcional): Cuando empresa ve tu CV, cuando cambia estado de tu postulación, cuando GADOR valida empresa, cuando oferta está por vencer en 24h, cuando hay nueva oferta de tu profesión.
* **RF13 - Dashboard SuperAdmin GADOR:**
  KPIs en tiempo real: Total postulantes registrados, Total empresas validadas/pendientes, Ofertas activas/publicadas/cerradas este mes, Postulaciones por mes (gráfico barras), Postulantes por profesión (torta), Empresas por rubro, Tasa de contratación (% CONTRATADO/POSTULADO).
* **RF14 - Reportes Exportables con Membrete GADOR:**
  Reporte empresas (NIT, Razón, Rubro, Estado), Reporte postulantes (CI, Nombre, Profesión, Celular), Reporte ofertas por fecha, Reporte contrataciones por empresa. Exportar Excel y PDF.
* **RF15 - Catálogos y Configuración:**
  SuperAdmin gestiona: Rubros empresas, Profesiones, Habilidades, Tipos contrato, Modalidades, Departamentos/Municipios. Configuración límite ofertas activas.
* **RF16 - Auditoría y Seguridad:**
  Tabla `audit_logs`: `user_id`, `accion` (CREATE, UPDATE, DELETE, LOGIN, CHANGE_STATUS), `tabla afectada`, `registro_id`, `datos anteriores/nuevos` (JSON), `IP`, `fecha`. Log de todas las validaciones de empresas y cambios de estado.

---

## REQUISITOS NO FUNCIONALES PARA LOS 3 MÓDULOS

* **Framework MVC Obligatorio:**
  Laravel 10+, Django 4+, NestJS, Spring Boot. Prohibido código spaghetti.
* **Base de Datos:**
  PostgreSQL/MySQL, 12 tablas mínimo: `users`, `roles`, `postulante_profiles`, `formaciones`, `experiencias`, `empresas`, `ofertas`, `habilidades`, `oferta_habilidad`, `postulaciones`, `catalogos`, `audit_logs`. Diagrama ER + Diccionario de datos.
* **Seguridad:**
  Bcrypt, Middleware roles (SuperAdmin, Empresa, Postulante), Validación backend, CSRF, XSS, `.env` para credenciales. Si hay credencial en repo = descalificado.
* **PWA Responsive:**
  Debe instalarse en celular, funcionar en Chrome móvil, diseño responsive.
* **GitHub:**
  Commits con mensajes claros, `README` con instalación, `.env.example`, migraciones y seeders.

---

## ENTREGABLES

1. GitHub + URL Demo
2. Archivo `.sql` + Diagrama ER + Diccionario de Datos
3. Manual Técnico + Manual de Usuario
4. Video 2 min flujo: Registro Empresa -> Validación GADOR -> Crear Oferta -> Registro Postulante -> Postular -> Empresa ve postulante

---
*Documento generado para la Gobernación Autónoma Departamental de Oruro - Unidad de Sistemas*  
*Fecha: Noviembre 2026 - Oruro, Bolivia*