# Bitácora de trabajo · Equipo E

- **Responsable:** Gabriel
- **Equipo:** Francisco (Paco), Ricardo, Gabriel y David

---

## Sesión 1 — Lunes 23/11/2026 (10:00–14:00 · Presencial)

### Cómo trabajamos
- **Arranque en papel (10:00–10:35):** Sin ordenadores ni móviles, cerramos la hoja de acuerdos, repartimos roles base (Paco: repositorio; Ricardo: contacto con el cliente; Gabriel: bitácora) y preparamos las preguntas iniciales.
- **Primera ronda con el cliente (11:10):** Planteamos nuestras dudas y anotamos las respuestas, tanto las nuestras como las del resto de equipos.
- **Diseño en papel (11:30–12:10):** Bocetamos las pantallas móviles (login, formulario, cursos, visor de la montaña y scroll) y el diagrama de arquitectura.
- **Segunda ronda con el cliente:** Con el diseño en papel delante, resolvimos dudas más concretas para afinar la propuesta.
- **Reparto y paso a limpio (12:10–13:10):** Ya con ordenadores, abrimos una carpeta en Google Drive para redactar en paralelo antes de pasar todo a GitHub y preparamos la exposición.
- **Presentación al cliente (13:10):** Expusimos el diseño en 5 minutos con la arquitectura en papel y respondimos a las preguntas.

### Quién hizo qué
- **Ricardo:** Propuso preguntas para el cliente, dibujó el diseño inicial en papel y planteó mecánicas de gamificación.
- **Paco:** Creó el repositorio en GitHub, dio acceso al equipo, subió las fotos de los bocetos y montó la carpeta de Google Drive.
- **Gabriel:** Definió la tabla de agentes, la estimación de costes, `docs/decisiones.md` y la primera entrada de la bitácora.
- **David:** Definió parte del flujo del alumno y la respuesta a los problemas de la plataforma actual de 480 Academy.

### Problemas y ajustes
- **Alcance demasiado amplio al principio:** Separamos las historias de usuario en qué entra, si da tiempo y qué queda fuera para asegurar una demo completa el lunes 30.
- **Evitar "otro chatbot más":** Reajustamos el diseño para separar los roles de IA en agentes especializados que actúen solo en momentos clave del flujo.

---

## Martes 24/11/2026 (Trabajo asíncrono · WhatsApp y Drive)

### Quién hizo qué
- **Paco:** Pulió `SPEC.md` y `docs/decisiones.md` (apoyándose en Claude para dar coherencia al diseño), detalló la mecánica de la montaña, redactó `CONTRIBUTING.md`, unificó la arquitectura (PostgreSQL + FastAPI) y preparó el reparto de issues.
- **Ricardo:** Sintetizó los apartados de Ideas y Costes y colaboró en las historias de usuario.
- **David:** Revisó el paquete de diseño, propuso reorientar la HU7 hacia las tarjetas sin conexión (Modo 4G) y validó el alcance de costes.
- **Gabriel:** Avanzó en la documentación de IA y el borrador del stack tecnológico, y actualizó la bitácora con el trabajo del lunes y del martes.

### Problemas y ajustes
- **Encaje de la HU7:** David vio que la historia original quedaba descolgada; acordamos sustituirla por las tarjetas de repaso sin conexión (Modo 4G).
- **Dudas de alcance y organización:** Aclaramos en equipo que el presupuesto cubre solo los costes de IA (no el desarrollo completo), concretamos cómo bajar cada historia de usuario a una issue de GitHub y revisamos cómo servir los vídeos de YouTube de muestra en el prototipo.

---

## Miércoles 25/11/2026 (Trabajo asíncrono · Cierre de documentación)

### Quién hizo qué
- **Paco:** Añadió el certificado de fin de curso al `SPEC.md` y dejó comentarios de mejora para cerrar (HUs, costes y redacción).
- **David:** Revisó y reformuló el punto 3 de `docs/decisiones.md` para centrarlo en transformar el vídeo tradicional en una experiencia interactiva, personalizada con IA y gamificada.
- **Gabriel:** Propuso dar mayor peso estratégico a la IA en las decisiones como parte principal del proyecto.
- Entre todos revisamos la documentación y decidimos empezar ya con el desarrollo del proyecto.

### Problemas y ajustes
- **Incoherencia en `docs/decisiones.md` (punto 3):** David detectó que las alternativas redactadas inicialmente no cuadraban con nuestro formato en scroll. Lo reenfocamos en equipo para destacar la integración no intrusiva de la IA y la gamificación.
