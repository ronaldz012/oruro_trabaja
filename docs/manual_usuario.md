# Manual de usuario — Oruro Trabaja

**Bolsa de trabajo digital de la Gobernación Autónoma Departamental de Oruro (GADOR)**

Versión 1.0 · Noviembre 2026

> **Nota para el editor:** cada sección incluye un marcador `CAP-XX` con la
> instrucción de la captura (página, usuario demo, estado y viewport). Las
> imágenes van en `docs/capturas/CAP-XX.png` con ese nombre exacto.

---

## 1. Introducción

Oruro Trabaja conecta a postulantes con empresas de todo el departamento de
Oruro. El sistema tiene tres roles:

| Rol | Qué hace |
|---|---|
| **Postulante** | Crea su perfil, sube su hoja de vida (CV) y postula a ofertas |
| **Empresa** | Se registra, publica ofertas y gestiona las postulaciones recibidas |
| **GADOR** | Valida empresas, revisa ofertas, administra catálogos y audita la plataforma |

![CAP-01](capturas/CAP-01.png)

> 📷 **CAP-01 — Pantalla de inicio (login).**
> Página: `/login/` · Sin usuario · Desktop 1366px.
> Se ve la marca "Oruro Trabaja", la imagen del monumento a la Virgen del
> Socavón y el formulario de acceso.

---

## 2. Registro y verificación (postulante)

1. En la pantalla de inicio, clic en **Crear cuenta**.
2. Completá el formulario: cédula de identidad, nombres y apellidos, celular,
   correo electrónico y contraseña.
3. El sistema envía un **código de verificación por SMS** a tu celular.
4. Ingresás el código de 6 dígitos y tu cuenta queda activa.

![CAP-02](capturas/CAP-02.png)

> 📷 **CAP-02 — Formulario de registro.**
> Página: `/registro/` · Sin usuario · Desktop 1366px.
> Formulario completo con los campos visibles.

![CAP-03](capturas/CAP-03.png)

> 📷 **CAP-03 — Verificación del celular.**
> Página: `/registro/verificar/` · Sin usuario · Desktop 1366px.
> Pantalla pidiendo el código de 6 dígitos. *(Modo demostración: el código se
> muestra en la misma pantalla; con SMS real llega al celular.)*

![CAP-04](capturas/CAP-04.png)

> 📷 **CAP-04 — Panel del postulante tras verificar.**
> Página: `/postulante/` · Rol: postulante · Desktop 1366px.
> Se ve el mensaje de bienvenida y la tarjeta "Completa tu perfil" con el
> porcentaje inicial (25 %).

## 3. Iniciar sesión

Ingresá tu correo y contraseña y presioná **Iniciar sesión**. Por seguridad,
si se acumulan 5 intentos fallidos desde una misma conexión, el acceso espera
15 minutos.

![CAP-05](capturas/CAP-05.png)

> 📷 **CAP-05 — Inicio de sesión completado.**
> Página: `/login/` · Rol: cualquiera · Desktop 1366px.
> Formulario lleno con correo válido y botón "Iniciar sesión".

---

## 4. Perfil del postulante

Tu perfil se completa por secciones; cada tarjeta muestra un **check verde**
cuando ya cuenta para el porcentaje, o un aviso ámbar con lo que falta:

- **Datos personales**: foto, dirección, fecha de nacimiento y presentación.
- **CV en PDF**: obligatorio — sin CV el perfil no supera el 80 % ni permite postular.
- **Formación académica** y **experiencia laboral**: al menos una de cada una.
- **Habilidades**: mínimo 3.
- **Idiomas**: opcional.

Al llegar a **más de 80 %**, el perfil muestra **"Podés postular"** en verde.

![CAP-06](capturas/CAP-06.png)

> 📷 **CAP-06 — Perfil incompleto (80 %).**
> Página: `/postulante/perfil/` · Rol: postulante · Desktop 1366px.
> Con CV subido y solo 1 habilidad: se ve el chip ámbar "1 de 3 · 20 %" en
> Habilidades, la etiqueta "Falta para postular" y la barra de progreso ámbar.

![CAP-07](capturas/CAP-07.png)

> 📷 **CAP-07 — Perfil completo (100 %).**
> Página: `/postulante/perfil/` · Rol: postulante · Desktop 1366px.
> Todas las secciones con check verde "Completa · X %", barra verde y
> "Podés postular" bajo el porcentaje 100 %.

Para agregar formación, experiencia, habilidades o idiomas usá el botón
**"+ Agregar …"** de cada tarjeta. El sistema guarda al instante y actualiza
el porcentaje con una notificación.

## 5. Buscar empleo y postular

1. En el menú lateral entrá a **Empleos**.
2. Explorá las ofertas publicadas y abrí la que te interese: verás requisitos,
   salario, modalidad y la empresa que la publica.
3. Presioná **Postular** — el sistema confirma con una notificación.

![CAP-08](capturas/CAP-08.png)

> 📷 **CAP-08 — Lista de ofertas públicas.**
> Página: `/empleos/` · Rol: postulante · Desktop 1366px.
> Ofertas disponibles con sus filtros (se ve la publicada "Desarrollador Full Stack").

![CAP-09](capturas/CAP-09.png)

> 📷 **CAP-09 — Detalle de una oferta.**
> Página: `/empleos/<id>/` · Rol: postulante · Desktop 1366px.
> Requisitos, salario, habilidades y botón "Postular".

![CAP-10](capturas/CAP-10.png)

> 📷 **CAP-10 — Postulación confirmada.**
> Página: `/empleos/<id>/` · Rol: postulante · Desktop 1366px.
> Notificación de éxito tras presionar Postular (y el botón en estado ya postulado).

En **Mis postulaciones** seguí el estado de cada proceso: *Visto*,
*Preseleccionado*, *Descartado*, *Contratado*.

![CAP-11](capturas/CAP-11.png)

> 📷 **CAP-11 — Mis postulaciones.**
> Página: `/postulante/postulaciones/` · Rol: postulante · Desktop 1366px.
> Tabla con la oferta postulada y su estado actual.

---

## 6. Registro de empresa

1. Desde el inicio, elegí **Registrarse como empresa** (pestaña "Empresa").
2. Completá el formulario: NIT, razón social, rubro, datos del representante,
   celular y correo.
3. La cuenta queda **pendiente de validación por GADOR**; al aprobarse, podés
   iniciar sesión y publicar ofertas.

![CAP-12](capturas/CAP-12.png)

> 📷 **CAP-12 — Formulario de registro de empresa.**
> Página: `/registro/empresa/` · Sin usuario · Desktop 1366px.
> Formulario completo con NIT, razón social y datos del representante.

![CAP-13](capturas/CAP-13.png)

> 📷 **CAP-13 — Panel de empresa recién registrada.**
> Página: `/empresa/` · Rol: empresa (pendiente) · Desktop 1366px.
> Aviso de que la empresa está pendiente de validación por GADOR.

## 7. Ofertas (empresa)

1. En **Mis ofertas**, botón **Nueva oferta**: completá el formulario en pasos
   (información, requisitos, condiciones) y guardá como borrador.
2. Con la oferta lista, presioná **Enviar a revisión** para que GADOR la
   apruebe; una vez publicada la verán los postulantes.
3. En el detalle de cada oferta ves las **postulaciones recibidas**:
   podés descargar el CV del postulante y cambiar el estado de su postulación
   (*Visto*, *Preseleccionado*, *Descartado*, *Contratado*).

![CAP-14](capturas/CAP-14.png)

> 📷 **CAP-14 — Mis ofertas de la empresa.**
> Página: `/empresa/ofertas/` · Rol: empresa · Desktop 1366px.
> Tabla con las ofertas en sus estados (publicada, en revisión, borrador).

![CAP-15](capturas/CAP-15.png)

> 📷 **CAP-15 — Creación de oferta (formulario en pasos).**
> Página: `/empresa/ofertas/nueva/` · Rol: empresa · Desktop 1366px.
> Formulario con los campos principales visibles.

![CAP-16](capturas/CAP-16.png)

> 📷 **CAP-16 — Postulaciones recibidas en el detalle de la oferta.**
> Página: `/empresa/ofertas/<id>/` · Rol: empresa · Desktop 1366px.
> Detalle de la oferta con la lista de postulantes, opción de descargar CV y
> selector de estado.

![CAP-17](capturas/CAP-17.png)

> 📷 **CAP-17 — Cambio de estado de una postulación.**
> Página: `/empresa/ofertas/<id>/` · Rol: empresa · Desktop 1366px.
> Postulación marcada como **Preseleccionado** con la notificación de éxito.

---

## 8. Panel GADOR

El panel de gestión permite:

- **Dashboard**: indicadores generales (empresas, postulantes, ofertas, postulaciones).
- **Empresas**: validar, rechazar o suspender empresas registradas.
- **Ofertas**: revisar las ofertas enviadas y publicarlas o devolverlas con motivo.
- **Catálogos**: administrar profesiones, habilidades, idiomas, rubros, tipos de
  contrato, modalidades y departamentos.
- **Reportes**: indicadores y exportables.
- **Auditoría**: registro de las acciones relevantes (creaciones y cambios de
  estado) con el detalle de los datos anteriores y posteriores de cada cambio.

![CAP-18](capturas/CAP-18.png)

> 📷 **CAP-18 — Panel GADOR.**
> Página: `/gador/` · Rol: GADOR · Desktop 1366px.
> Tarjetas de indicadores con los contadores generales.

![CAP-19](capturas/CAP-19.png)

> 📷 **CAP-19 — Validación de empresas.**
> Página: `/gador/empresas/` · Rol: GADOR · Desktop 1366px.
> Lista de empresas con estado "Pendiente de validación" (ámbra) y acción de revisar.

![CAP-20](capturas/CAP-20.png)

> 📷 **CAP-20 — Revisión de ofertas.**
> Página: `/gador/ofertas/` · Rol: GADOR · Desktop 1366px.
> Oferta en revisión con las acciones de aprobar (publicar) o devolver.

![CAP-21](capturas/CAP-21.png)

> 📷 **CAP-21 — Catálogos.**
> Página: `/gador/catalogos/` · Rol: GADOR · Desktop 1366px.
> Catálogo de profesiones (u otro) con paginación.

![CAP-22](capturas/CAP-22.png)

> 📷 **CAP-22 — Auditoría: lista de acciones.**
> Página: `/gador/auditoria/` · Rol: GADOR · Desktop 1366px.
> Tabla con fecha, usuario, acción (chips de color), tabla afectada y registro.

![CAP-23](capturas/CAP-23.png)

> 📷 **CAP-23 — Auditoría: detalle del cambio.**
> Página: `/gador/auditoria/<id>/` · Rol: GADOR · Desktop 1366px.
> Detalle con IP, usuario y los JSON "Estado antes" / "Estado después"
> (por ejemplo EN_REVISION_GADOR → PUBLICADA).

---

## 9. Mi cuenta

En la esquina superior derecha, el menú con tu foto o iniciales ofrece
**Mi cuenta** (datos de la cuenta y credenciales) y **Salir**.

![CAP-24](capturas/CAP-24.png)

> 📷 **CAP-24 — Menú de usuario y pantalla Mi cuenta.**
> Página: `/mi-cuenta/` · Rol: cualquiera · Desktop 1366px.
> Menú desplegado con "Mi cuenta" y "Salir", y la pantalla con los datos de la
> cuenta deshabilitados con el aviso "No disponible en demo".

## 10. Instalación en el celular (PWA)

Oruro Trabaja es una **aplicación web progresiva**: desde el navegador del
celular podés instalarla (menú → *Añadir a pantalla de inicio*) y usarla como
app. Si perdés la conexión, la pantalla offline te avisa y la app retoma el
funcionamiento al reconectar.

![CAP-25](capturas/CAP-25.png)

> 📷 **CAP-25 — Vista móvil del perfil (100 %).**
> Vista: `/postulante/perfil/` · Rol: postulante · **Viewport móvil (≈390px)**
> o Chrome DevTools responsive. Se ve el perfil completo en formato celular.

![CAP-26](capturas/CAP-26.png)

> 📷 **CAP-26 — Vista móvil de la postulación.**
> Vista: `/empleos/<id>/` · Rol: postulante · **Viewport móvil (≈390px)**.
> Detalle de oferta y botón "Postular" en el celular.

---

## Anexo A — Estados de una postulación

| Estado | Significado |
|---|---|
| Postulado | La postulación fue recibida |
| Visto | La empresa la revisó |
| Preseleccionado | El postulante pasa a la siguiente etapa |
| Descartado | No continúa en el proceso |
| Contratado | El postulante fue contratado |

## Anexo B — Estados de una oferta

| Estado | Significado |
|---|---|
| Borrador | La empresa la está redactando |
| En revisión | Enviada a GADOR para su aprobación |
| Publicada | Visible para los postulantes |
| En proceso de selección | Se reciben y gestionan postulaciones |
| Cerrada / Anulada | Ya no admite postulaciones |

## Anexo C — Avisos de la versión demo

- El cambio de contraseña y la recuperación por correo se presentan con estado
  **No disponible en demo** (ver sección *Mi cuenta*).
- En modo demostración el código de verificación se muestra en pantalla en
  lugar de enviarse por SMS.
