
# AGENTS.md

## 1. Contexto del proyecto

Desarrollamos un prototipo de plataforma educativa para 480 Academy.

El objetivo es transformar el aprendizaje basado en vídeos en una experiencia personalizada, interactiva y mobile-first, mediante IA, actividades y gamificación.

Antes de implementar una funcionalidad, consulta la documentación relevante:

- `SPEC.md`: requisitos, historias de usuario, criterios de aceptación y alcance.
- `docs/decisiones.md`: decisiones técnicas y de producto.
- `CONTRIBUTING.md`: normas de colaboración y revisión.
- `docs/DESIGN.md`: sistema de diseño e interfaz.
- `docs/MONTANA.md`: montaña, personaje y recompensas.
- `docs/CERTIFICADO.md`: certificados de finalización.

No inventes requisitos ni funcionalidades. Si encuentras contradicciones entre documentos, informa antes de implementar.

## 2. Stack tecnológico

- Frontend: HTML, Tailwind CSS y Alpine.js.
- Aplicación: PWA mobile-first.
- Backend: Python, FastAPI y Pydantic.
- Base de datos: PostgreSQL.
- Contenido educativo: `catalogo.json`.
- Inteligencia artificial: Mistral AI, mediante el backend.
- Infraestructura: Docker Compose y nginx.

Respeta el stack acordado. No introduzcas frameworks, servicios o dependencias importantes sin justificarlo y obtener aprobación.

## 3. Estructura y responsabilidades

Mantén la separación de responsabilidades:

- `frontend/`: interfaz, navegación e interacciones del alumno.
- `backend/`: API REST, autenticación y lógica de negocio.
- `agentes/`: agentes educativos e integración con Mistral.
- `tests/`: pruebas automatizadas.
- `docs/`: especificaciones y decisiones.

El frontend se comunica con el backend mediante la API. No debe acceder directamente a PostgreSQL ni a Mistral AI.

Consulta los contratos de la API antes de utilizarlos. No inventes endpoints ni estructuras de respuesta.

Estas rutas representan la organización prevista. Comprueba la estructura real del repositorio antes de crear archivos.

## 4. Comandos del proyecto

Los comandos definitivos se documentarán cuando esté configurado el repositorio.

- Instalación de dependencias: PENDIENTE.
- Arranque: previsto mediante Docker Compose.
- Tests: PENDIENTE.
- Linter y análisis estático: PENDIENTE.
- Verificación completa: PENDIENTE.

No inventes comandos ni afirmes que una comprobación se ha ejecutado si no es cierto.

## 5. Convenciones y reglas de negocio

- La interfaz debe ser mobile-first y usable con una mano.
- Los itinerarios se personalizan según el perfil del alumno.
- El alumno puede avanzar sin estar obligado a reproducir todos los vídeos.
- El contenido combina scrolling, fragmentos de vídeo y actividades interactivas.
- El progreso y las recompensas dependen de las reglas definidas en el SPEC.
- La IA educativa se utiliza únicamente en las funciones previstas.
- Las preguntas tipo test se corrigen mediante código convencional cuando no necesitan IA.
- Las funcionalidades opcionales no se implementan sin aprobación.

El detalle de estas reglas está en `SPEC.md`. No lo dupliques aquí.

## 6. Flujo de trabajo obligatorio

Para cada tarea:

1. EXPLORAR: lee el código y la documentación relevante.
2. PLANIFICAR: identifica archivos afectados, dependencias y criterios de aceptación. Presenta el plan antes de editar.
3. PREPARAR PRUEBAS: define tests basados en los criterios de aceptación y comprueba el fallo inicial cuando corresponda.
4. IMPLEMENTAR: realiza cambios pequeños y limitados al alcance acordado.
5. VERIFICAR: ejecuta los tests y comprobaciones disponibles. Comprueba que se cumplen los criterios de aceptación, que no se han introducido vulnerabilidades ni se compromete la privacidad de los alumnos y que los cambios no afectan a otras funcionalidades.
6. REVISAR: arranca la aplicación con Docker Compose, comprueba que los servicios necesarios funcionan y verifica que el resto de la aplicación sigue funcionando correctamente. Revisa también los cambios realizados y las pruebas de integración.
7. ENTREGAR: comprueba que se cumple la definición de terminado de `CONTRIBUTING.md`. Resume los cambios, las pruebas ejecutadas, sus resultados y cualquier problema pendiente. No declares una tarea completada si quedan verificaciones obligatorias sin realizar.

No consideres terminada una tarea sin verificarla. Si no puedes ejecutar una prueba, indica el motivo.

## 7. Seguridad y límites

- No incluyas API keys, contraseñas ni secretos en el repositorio.
- No envíes datos personales identificables a servicios de IA.
- Toda comunicación con Mistral debe pasar por el backend y sus filtros de privacidad.
- No realices llamadas externas de pago ni acciones destructivas sin aprobación.
- No elimines archivos ni modifiques componentes ajenos a la tarea sin autorización.
- No cambies el stack ni la arquitectura por iniciativa propia.
- No publiques código directamente en `main`.
- No realices commits, pushes ni merges sin autorización explícita.
- Antes de finalizar cualquier tarea, verifica que no se exponen datos personales, secretos ni credenciales; que las peticiones a la IA pasan por los filtros del backend; y que se respetan los permisos de acceso. No basta con que los tests funcionales pasen: la privacidad y la seguridad también forman parte de la definición de terminado.

## 8. Colaboración y cierre

Sigue las normas de `CONTRIBUTING.md`:

- Una rama por tarea.
- Commits descriptivos en español.
- Pull requests revisados por otra persona.
- Documentar decisiones relevantes y problemas en `BITACORA.md`.

Al terminar una tarea, informa de:

- Qué has implementado.
- Qué archivos has modificado.
- Qué pruebas has ejecutado y su resultado.
- Qué queda pendiente o necesita revisión humana.

Si un error revela una carencia en las instrucciones, tests o herramientas, propón una mejora del harness en lugar de limitarte a corregir el código.
