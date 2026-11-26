# Cómo trabajamos

## Roles

| Persona | Rol técnico | Función en el equipo |
| --- | --- | --- |
| Francisco (Paco) | Infraestructura: Docker Compose, nginx, PostgreSQL y despliegue | Responsable del repositorio: da acceso al equipo, revisa que el código y la documentación estén en orden |
| Ricardo | Datos: modelo de datos, `catalogo.json`, telemetría y Analizador de datos | Contacto con el cliente: reúne las dudas del equipo y apunta las respuestas |
| Gabriel | IA: agentes, instrucciones (prompts), filtro de datos personales e integración con Mistral | Bitácora: apunta en cada sesión quién hace qué, qué problemas surgen y qué se decide |
| David | Diseño y frontend: pantallas de la PWA mobile-first (HTML, Tailwind y Alpine.js) | Coherencia visual y usabilidad con una mano |

El resto del trabajo (historias de usuario, pruebas, presentación y demo) lo hacemos entre todos.

## Comunicación

- **Día a día:** grupo de WhatsApp.
- **Tareas:** cada historia de usuario es una issue de GitHub con persona asignada y estimación.
- Las decisiones importantes se apuntan en `docs/decisiones.md` y en `BITACORA.md`.

## Ramas

- `main`: siempre tiene una versión que funciona. Nadie sube cambios directamente a `main`.
- Una rama por tarea, creada desde `main`, con el formato `tipo/descripcion-corta`:
  - `feature/hu3-video-fragmentado`
  - `fix/login-movil`
  - `docs/spec-arquitectura`
- Los mensajes de commit se escriben en español y explican qué cambia, por ejemplo: `"Añade pantalla de progreso del módulo"`.

## Pull requests

- Al terminar la tarea, se abre un pull request de la rama hacia `main`.
- En la descripción se indica qué issue cierra (por ejemplo, `"Closes #3"`) y cómo probarlo.
- Otra persona del equipo lo revisa y lo aprueba. Nadie aprueba su propio pull request.
- Si hay conflictos, los resuelve quien abrió el pull request.
- Una vez aprobado, se fusiona en `main` y se borra la rama.

## Cuándo damos algo por terminado

Una tarea está terminada cuando:

- Cumple todos los criterios de aceptación de su historia de usuario (`SPEC.md`, apartado 4).
- Funciona en el móvil y se puede usar con una mano.
- No envía datos personales a la IA (pasa por el filtro del backend).
- Se ha probado con `docker compose up` y el resto de la aplicación sigue funcionando.
- Otra persona del equipo ha revisado y aprobado el pull request.
- Si cambia algo de un agente de IA, sus instrucciones están actualizadas en la carpeta `agentes/`.
- Privacidad y seguridad (RGPD): no se han subido claves (`.env` / API Keys) al repositorio y ningún agente de IA recibe datos personales identificables.
- Si se ha tomado una decisión o surgido un problema, está apuntado en `BITACORA.md`.
