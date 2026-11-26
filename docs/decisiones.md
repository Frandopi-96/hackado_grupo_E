# Decisiones

## 1. Stack tecnológico

Hemos decidido construir una PWA *mobile-first* (HTML, Tailwind CSS y Alpine.js) con backend en Python y FastAPI (SDK de Mistral y Pydantic), PostgreSQL y `catalogo.json` para el contenido, todo desplegado con Docker Compose detrás de nginx. Como alternativas valoramos una app nativa (iOS/Android), una web clásica que depende de conexión constante y React como frontend. Elegimos PWA porque se instala en cualquier móvil sin pasar por tiendas y guarda las tarjetas del Modo 4G para usarlas sin cobertura; Alpine.js porque no necesita compilación y pesa menos en 4G; FastAPI por el dominio de Python del equipo, y PostgreSQL con Docker porque deja el prototipo listo como base para producción.

## 2. Modelo y proveedor de IA

Hemos decidido usar un único proveedor europeo, Mistral AI (región UE), con un modelo por tarea: Voxtral para transcribir, Ministral 3 8B para el Selector de cursos y Mistral Small 4 para el resto. Como alternativas valoramos proveedores de EE. UU. (OpenAI, Anthropic, Google) y modelos gratuitos sin garantías de privacidad. Elegimos Mistral porque los datos no salen de la UE, reduce la integración a una sola API key y su coste por alumno es bajo. Mistral guarda las peticiones 30 días para vigilar abusos y no las usa para entrenar; en producción pediríamos la retención cero (ZDR) y desactivaríamos la mejora con datos anónimos. En todo caso, solo le llegan textos filtrados y con un ID aleatorio.

## 3. La decisión de producto que más condiciona nuestra solución

Hemos decidido transformar la plataforma de vídeos pasivos en una experiencia de aprendizaje personalizada, interactiva y *mobile-first* impulsada por IA: itinerarios adaptados, vídeos segmentados en scroll con preguntas (y test previo para saltar lo ya dominado), profesor IA contextualizado y gamificación con la montaña y el personaje. Como alternativas valoramos centrarnos en una única mejora (solo scroll, solo itinerarios o solo gamificación) o mantener la plataforma actual añadiendo un chatbot. Elegimos la combinación porque es la única que responde a los cuatro problemas de 480 Academy a la vez: frena el abandono, adapta el ritmo a cada alumno, mide el aprendizaje real y libera a los 6 tutores.
