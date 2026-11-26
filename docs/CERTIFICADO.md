# CERTIFICADO.md: certificado del curso y publicación en LinkedIn

Instrucciones para implementar lo que pasa cuando el alumno llega a la cima. Están pensadas para que un agente de código (Claude Code u otro) las siga sin tener que tomar decisiones de diseño. Depende de `MONTANA.md` (el montañista) y de `DESIGN.md` (colores y tipografía).

**Regla para el agente:** implementa lo que pone aquí. Si algo no está especificado, elige la opción más simple y anótalo en BITACORA.md.

## 1. Qué es

Al completar el curso, el alumno obtiene un certificado visual con **su montañista en la cima**, equipado con los objetos que ha ganado. Desde ahí puede:

1. **Publicar un post en LinkedIn** con la imagen del certificado y un texto ya redactado.
2. **Añadir el certificado a su perfil de LinkedIn**, en la sección "Licencias y certificaciones".
3. **Descargar la imagen.**

Para 480 Academy, cada publicación es publicidad gratuita. Para el alumno, el personaje hace que el certificado sea suyo y no una plantilla genérica.

## 2. Flujo

1. El alumno completa el módulo 4 y el montañista sube a la cima (`MONTANA.md`, apartado 5).
2. La hoja de "¡Has llegado a la cima!" tiene un botón principal nuevo: **"Ver mi certificado"**.
3. Se abre la pantalla del certificado:
   - Arriba, la imagen del certificado (apartado 3), a todo el ancho.
   - Un interruptor **"Mostrar mi nombre"**, activado por defecto.
   - Botón principal **"Publicar en LinkedIn"** (apartado 5).
   - Botón secundario **"Añadir a mi perfil de LinkedIn"** (apartado 6).
   - Enlace **"Descargar imagen"**.
4. Si el alumno es menor de edad, la pantalla muestra solo la imagen y "Descargar imagen", sin los botones de LinkedIn (apartado 8).

## 3. La imagen del certificado

Cuadrada, **1080 × 1080 px**, PNG. Es el formato que mejor se ve en el móvil dentro del feed de LinkedIn.

Se genera **en el móvil del alumno**, nunca en el servidor ni con IA: se monta un SVG de 1080 × 1080, se dibuja en un `<canvas>` y se exporta con `canvas.toBlob(..., 'image/png')`. Antes de dibujar, hay que esperar a que cargue la fuente (`await document.fonts.ready`) para que el texto salga en DM Sans y no con la fuente por defecto.

### Composición (coordenadas en el lienzo de 1080 × 1080)

| Elemento | Posición y estilo |
|---|---|
| Fondo | `#1F2222` |
| Brillo | Círculo `cx=540 cy=420 r=420`, degradado radial de `#39FE90` al 18 % a transparente |
| Logo 480 | `480 Color White fondo.svg` sin el fondo, arriba a la izquierda: `x=72 y=72`, alto 56 |
| Etiqueta | "CERTIFICADO_DE_FINALIZACIÓN", `x=72 y=190`, DM Sans 28px, weight 500, `#1CF9FC`, espaciado de letras 2px |
| Montaña | La silueta y el camino de `MONTANA.md`, escalados ×1,5 y centrados en `x=540`, con la base en `y=860`. Todas las paradas en estado `completado` y la bandera de la cima en verde |
| Montañista | En la cima, escala ×4, con los objetos **equipados** en ese momento |
| Nombre del curso | "Introducción a Python", centrado, `y=920`, DM Sans 56px, weight 700, blanco |
| Nombre del alumno | Centrado, `y=975`, DM Sans 32px, weight 400, `#D0D5D2`. **Solo si "Mostrar mi nombre" está activado** |
| Pie | "480 Academy · Noviembre 2026 · Código: X7K2-9QPM", centrado, `y=1030`, DM Sans 22px, `#D0D5D2` al 70 % |

Si "Mostrar mi nombre" está desactivado, el nombre del curso baja a `y=950` y no se deja hueco.

## 4. El texto del post

Se genera con una **plantilla, sin IA**. Así no tiene coste y no sale ningún dato del alumno hacia Mistral. El alumno puede editarlo en un cuadro de texto antes de publicar.

```
🏔️ ¡He llegado a la cima del curso {curso} de 480 Academy!

Han sido {n_modulos} módulos: {lista_modulos}.

Ahora sé {habilidades}.

Mi montañista ha subido con {objetos}. Siguiente montaña: ¿cuál me recomendáis?

Certificado verificable: {url_certificado}

#480Academy #{hashtag_curso} #AprendizajeContinuo
```

Variables, todas salen de `catalogo.json` y de la base de datos:

| Variable | Ejemplo |
|---|---|
| `{curso}` | Introducción a Python |
| `{n_modulos}` | 4 |
| `{lista_modulos}` | primeros pasos, control de flujo, estructuras de datos y funciones y ficheros |
| `{habilidades}` | escribir programas en Python con condicionales, bucles, listas, diccionarios y funciones |
| `{objetos}` | botas, camiseta técnica, gorro y mochila (solo los equipados; si no lleva ninguno, se quita esa frase) |
| `{url_certificado}` | `https://<dominio>/certificado/X7K2-9QPM` |
| `{hashtag_curso}` | Python |

Añadir a `catalogo.json`, dentro del curso:

```json
"certificado": {
  "habilidades": "escribir programas en Python con condicionales, bucles, listas, diccionarios y funciones",
  "hashtag": "Python"
}
```

## 5. "Publicar en LinkedIn"

LinkedIn no permite que una web externa le pase una imagen y un texto ya escritos por enlace. Por eso se usa el menú "Compartir" del propio móvil, que sí permite enviar la imagen a la app de LinkedIn.

Al pulsar el botón:

1. **Copiar el texto** del post al portapapeles (`navigator.clipboard.writeText`) y mostrar un aviso: "Texto copiado. Pégalo en LinkedIn si no aparece". Algunas versiones de la app de LinkedIn ignoran el texto cuando se comparte una imagen, así que este paso es necesario.
2. Si el navegador lo permite (`navigator.canShare({ files: [archivoPng] })`), abrir el menú de compartir del móvil:
   ```js
   await navigator.share({ files: [archivoPng], text: textoPost, title: 'Mi certificado de 480 Academy' });
   ```
   El alumno elige LinkedIn en el menú.
3. Si no lo permite (por ejemplo, en un ordenador): descargar el PNG y abrir `https://www.linkedin.com/feed/` en una pestaña nueva, con el aviso "Imagen descargada y texto copiado. Crea una publicación en LinkedIn y adjunta la imagen".

## 6. "Añadir a mi perfil de LinkedIn"

LinkedIn tiene un enlace oficial ("Add to Profile") que abre el formulario de añadir certificación con los datos ya rellenados:

```
https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME
  &name=Introducción%20a%20Python
  &organizationName=480%20Academy
  &issueYear=2026
  &issueMonth=11
  &certUrl=https%3A%2F%2F<dominio>%2Fcertificado%2FX7K2-9QPM
  &certId=X7K2-9QPM
```

- Todos los valores van codificados con `encodeURIComponent`.
- Se usa `organizationName` (texto) porque no tenemos el identificador de la página de LinkedIn de 480. En producción se cambiaría por `organizationId`, y así en el perfil saldría el logo de 480.
- El curso no caduca, así que no se envían `expirationYear` ni `expirationMonth`.
- Se abre en una pestaña nueva. No hace falta ninguna API ni clave de LinkedIn.

## 7. Página pública de verificación

`GET /certificado/{codigo}`: página sencilla, sin necesidad de iniciar sesión, que confirma que el certificado es real. Es la URL que va en el post y en el perfil de LinkedIn.

- Muestra la imagen del certificado, el curso, la fecha y "Certificado verificado por 480 Academy".
- Muestra el nombre del alumno **solo si** al generarlo tenía activado "Mostrar mi nombre".
- Lleva etiquetas Open Graph (`og:title`, `og:description`, `og:image` con la imagen de 1080 × 1080) para que el enlace se vea con vista previa al compartirlo.
- Si el código no existe: "No encontramos este certificado", con estado 404.

Para la página y la vista previa, el PNG se sube al backend una vez generado (`POST /api/certificados/{codigo}/imagen`) y se guarda en el servidor. Si el alumno vuelve a generarlo, se sustituye.

## 8. Privacidad

- **Nada de este flujo pasa por la IA.** La imagen se genera en el móvil y el texto, con una plantilla.
- El nombre del alumno solo aparece si él lo decide, y puede desactivarlo en cualquier momento. Al desactivarlo, la página de verificación deja de mostrarlo.
- **Menores de edad:** si el alumno está marcado como menor, no se muestran los botones de LinkedIn ni se crea la página pública. Solo puede descargar la imagen, y esta se genera sin nombre.
- El código del certificado es aleatorio (8 caracteres en el formato `XXXX-XXXX`, letras mayúsculas y números, sin `O`, `0`, `I` ni `1` para evitar confusiones) y no permite deducir quién es el alumno.

## 9. Datos

Nueva entidad **Certificado** en PostgreSQL:

| Campo | Tipo | Notas |
|---|---|---|
| `codigo` | texto, clave primaria | `X7K2-9QPM` |
| `alumno_id` | UUID | Relación con Alumno |
| `curso_id` | texto | |
| `fecha_emision` | fecha | |
| `mostrar_nombre` | booleano | |
| `objetos_equipados` | lista de textos | Foto del montañista en el momento de generarlo |
| `ruta_imagen` | texto | PNG guardado en el servidor |

¿Sale hacia la IA? **No, nunca.**

## 10. Criterios de aceptación

- [ ] Al completar el curso, aparece "Ver mi certificado" en la hoja de la cima.
- [ ] La imagen de 1080 × 1080 muestra el montañista con los objetos que lleva equipados y respeta el interruptor del nombre.
- [ ] "Publicar en LinkedIn" copia el texto y abre el menú de compartir del móvil con la imagen.
- [ ] "Añadir a mi perfil de LinkedIn" abre el formulario de LinkedIn con el nombre del curso, 480 Academy, la fecha, la URL y el código ya rellenados.
- [ ] La URL del certificado abre la página de verificación con vista previa.
- [ ] Un alumno menor solo ve la opción de descargar la imagen, sin nombre.
- [ ] Ningún dato de este flujo se envía a Mistral.
