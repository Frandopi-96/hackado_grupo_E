# MONTANA.md: especificación de la montaña y el montañista (HU6)

Instrucciones para implementar la pantalla de progreso del curso. Están pensadas para que un agente de código (Claude Code u otro) las siga sin tener que tomar decisiones de diseño. Los colores y la tipografía salen de `DESIGN.md`.

**Regla para el agente:** implementa lo que pone aquí. Si algo no está especificado, elige la opción más simple y anótalo en BITACORA.md. No cambies las decisiones marcadas como **[DECISIÓN DEL EQUIPO]** sin preguntar.

## 1. Qué es

El progreso de un curso se muestra como una montaña. Cada módulo es una parada del camino hacia la cima. El personaje del alumno (el montañista) está en la parada del módulo actual. Al completar un módulo, sube a la siguiente parada y desbloquea un objeto para su personaje. Al llegar a la cima, el alumno consigue la insignia del curso.

## 2. Decisiones fijadas

- **[DECISIÓN DEL EQUIPO]** Las paradas son los **módulos** (4 en el curso de Python), no los vídeos.
- **[DECISIÓN DEL EQUIPO]** Objetos que se desbloquean, uno por módulo completado:

| Módulo completado | Objeto | id |
|---|---|---|
| 1. Primeros pasos | Botas de montaña | `botas` |
| 2. Control de flujo | Camiseta técnica | `camiseta` |
| 3. Estructuras de datos | Gorro | `gorro` |
| 4. Funciones y ficheros | Mochila + insignia del curso | `mochila` |

- Todo se dibuja con **SVG en línea** dentro del HTML. Sin imágenes, sin librerías de animación. Alpine.js para el estado.
- Estilo plano y geométrico: formas simples, sin degradados salvo el brillo de la parada actual.

## 3. Lienzo

- `<svg viewBox="0 0 360 640">` a todo el ancho de la pantalla, con `preserveAspectRatio="xMidYMax meet"`.
- Fondo de la pantalla: `#1F2222`.

### 3.1 Silueta de la montaña

```html
<polygon points="0,640 0,560 60,470 110,420 150,300 180,90 210,180 250,260 300,330 360,400 360,640"
         fill="#2A2E2E" />
```

### 3.2 Paradas (coordenadas fijas)

| Parada | x | y | Etiqueta | Lado de la etiqueta |
|---|---|---|---|---|
| Inicio (base) | 180 | 625 | — | — |
| Módulo 1 | 90 | 560 | M1 · Primeros pasos | derecha |
| Módulo 2 | 250 | 450 | M2 · Control de flujo | izquierda |
| Módulo 3 | 160 | 340 | M3 · Estructuras de datos | derecha |
| Módulo 4 | 205 | 225 | M4 · Funciones y ficheros | izquierda |
| Cima | 180 | 105 | Cima | encima |

Todas las paradas quedan dentro de la silueta. Si se cambia la silueta, hay que comprobarlo de nuevo.

### 3.3 Camino

Dos trazos con la misma geometría:

```html
<!-- Camino completo, discontinuo, por debajo -->
<path d="M180 625 L90 560 L250 450 L160 340 L205 225 L180 105"
      fill="none" stroke="#1CF9FC" stroke-width="3" stroke-dasharray="6 6" opacity="0.6" />
<!-- Tramo recorrido, continuo, por encima: desde el inicio hasta la parada actual -->
<path :d="caminoRecorrido" fill="none" stroke="#39FE90" stroke-width="3" stroke-linecap="round" />
```

`caminoRecorrido` se calcula uniendo con `L` los puntos desde el inicio hasta la parada actual incluida.

### 3.4 Nodos de las paradas

Círculo de radio 14 en cada parada. Tres estados:

| Estado | Dibujo |
|---|---|
| `completado` | `fill="#39FE90"` y un check encima: `<path d="M-6 0 L-2 4 L6 -5" stroke="#1F2222" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>` (coordenadas relativas al centro del nodo) |
| `actual` | `fill="#1F2222" stroke="#39FE90" stroke-width="3"`, y detrás un círculo de brillo `r="22" fill="#39FE90"` con la animación `pulso` |
| `bloqueado` | `fill="#2A2E2E" stroke="#D0D5D2" stroke-width="2" opacity="0.5"` |

```css
@keyframes pulso {
  0%   { transform: scale(1);   opacity: 0.35; }
  100% { transform: scale(1.4); opacity: 0;    }
}
.brillo { transform-box: fill-box; transform-origin: center; animation: pulso 1.6s ease-out infinite; }
```

- Etiquetas: DM Sans, 12px, weight 500. Color blanco si la parada está completada o es la actual, `#D0D5D2` con opacidad 0,6 si está bloqueada. Separación de 22 unidades respecto al centro del nodo, en el lado indicado en la tabla 3.2 (`text-anchor="start"` a la derecha, `"end"` a la izquierda).
- Zona táctil: cada nodo va dentro de un `<a>` o `<g role="button">` con un círculo invisible de `r="22"` (44px de diámetro mínimo).
- Tocar una parada completada o la actual abre ese módulo. Tocar una bloqueada muestra un aviso breve: "Completa el módulo anterior para desbloquearlo".

### 3.5 Cima

- Mástil: `<line x1="180" y1="105" x2="180" y2="70" stroke="#D0D5D2" stroke-width="2"/>`
- Bandera: `<polygon points="180,70 204,78 180,86"/>` con `fill="#39FE90"` si el curso está completado, o `fill="#2A2E2E" stroke="#D0D5D2"` si no.
- Encima de la bandera, el texto "Cima" (12px, weight 700).

## 4. El montañista

Personaje original y geométrico. Mide unas 50 unidades de alto. Su origen (0,0) está en los pies, en el centro. Se coloca con `transform="translate(x, y - 16)"`, donde (x, y) es la parada actual, para que quede de pie justo encima del nodo.

Cada parte es un `<g>` con `data-capa`. Las capas de objetos se muestran solo si el objeto está **equipado** (`x-show`). El orden de dibujo, de atrás hacia delante, es el del código:

```html
<g id="montanista" :transform="`translate(${pos.x}, ${pos.y - 16})`">
  <g class="balanceo">
    <!-- Mochila (objeto, detrás del cuerpo) -->
    <g data-capa="mochila" x-show="equipado('mochila')">
      <rect x="-11" y="-29" width="6" height="13" rx="1.5" fill="#39FE90"/>
    </g>
    <!-- Piernas (base) -->
    <g data-capa="piernas">
      <rect x="-6" y="-14" width="5" height="13" rx="1" fill="#8A9190"/>
      <rect x="1"  y="-14" width="5" height="13" rx="1" fill="#8A9190"/>
    </g>
    <!-- Botas (objeto) -->
    <g data-capa="botas" x-show="equipado('botas')">
      <rect x="-7" y="-4" width="7" height="4" rx="1" fill="#39FE90"/>
      <rect x="0"  y="-4" width="7" height="4" rx="1" fill="#39FE90"/>
    </g>
    <!-- Torso (base) -->
    <g data-capa="torso">
      <rect x="-7" y="-30" width="14" height="17" rx="3" fill="#D0D5D2"/>
    </g>
    <!-- Camiseta (objeto, tapa el torso). La franja diagonal recuerda a la barra del logo -->
    <g data-capa="camiseta" x-show="equipado('camiseta')">
      <rect x="-7" y="-30" width="14" height="17" rx="3" fill="#1CF9FC"/>
      <polygon points="-2,-30 3,-30 -1,-13 -6,-13" fill="#1F2222" opacity="0.25"/>
    </g>
    <!-- Brazos y bastón (base) -->
    <g data-capa="brazos">
      <line x1="-7" y1="-27" x2="-11" y2="-17" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
      <line x1="7"  y1="-27" x2="11"  y2="-19" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
      <line x1="12" y1="-22" x2="15"  y2="0"   stroke="#D0D5D2" stroke-width="2" stroke-linecap="round"/>
    </g>
    <!-- Cabeza (base) -->
    <g data-capa="cabeza">
      <circle cx="0" cy="-38" r="7" fill="#FFFFFF"/>
    </g>
    <!-- Gorro (objeto) -->
    <g data-capa="gorro" x-show="equipado('gorro')">
      <path d="M -7 -40 A 7 7 0 0 1 7 -40 Z" fill="#FF4950"/>
      <rect x="-8" y="-41" width="16" height="2.5" rx="1" fill="#FF4950"/>
      <circle cx="0" cy="-47.5" r="2" fill="#FFFFFF"/>
    </g>
  </g>
</g>
```

Animación en reposo, un balanceo suave:

```css
@keyframes balanceo { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-2px); } }
.balanceo { animation: balanceo 2s ease-in-out infinite; }
```

## 5. Subir a la siguiente parada

Cuando el backend confirma que un módulo se ha completado:

1. El montañista se mueve en línea recta desde la parada actual hasta la siguiente en **900 ms**, con `requestAnimationFrame` e interpolación lineal entre las dos coordenadas (el tramo es recto, así que basta con eso). Curva: `easeInOutQuad`.
2. Mientras se mueve, el tramo verde del camino crece con él.
3. Al llegar, el nodo anterior pasa a `completado` y el nuevo a `actual`.
4. A continuación aparece una **hoja inferior** (bottom sheet), anclada abajo para alcanzarla con el pulgar:
   - Título: "¡Has desbloqueado: Botas de montaña!" (con el nombre del objeto que toque).
   - Una vista previa del montañista a escala 2 con el objeto ya puesto.
   - Botón principal "Equipar" (verde, texto `#1F2222`, alto 48px, ancho completo).
   - Botón secundario "Más tarde" (borde cian).
5. Si es el módulo 4, el montañista sube hasta la cima, la bandera pasa a verde y la hoja dice "¡Has llegado a la cima! Insignia del curso conseguida", además de desbloquear la mochila.

Si el usuario tiene activado `prefers-reduced-motion`: sin desplazamiento, sin balanceo y sin pulso. El montañista aparece directamente en la nueva parada.

## 6. Pantalla de equipamiento

Accesible desde un botón "Mi montañista" en la pantalla de la montaña.

- Arriba, el montañista a escala 3, centrado.
- Debajo, una cuadrícula de 2 columnas con los 4 objetos. Cada casilla tiene un icono (la propia capa del SVG, ampliada), el nombre y un interruptor de equipar o quitar.
- Objetos bloqueados: en gris con opacidad 0,4 y el texto "Completa el módulo N".
- Cambiar un interruptor actualiza el personaje al instante y llama a `POST /api/personaje/equipar`.

## 7. Datos

### 7.1 Configuración en `catalogo.json`

```json
"recompensas": [
  { "modulo": 1, "objeto": "botas",    "nombre": "Botas de montaña" },
  { "modulo": 2, "objeto": "camiseta", "nombre": "Camiseta técnica" },
  { "modulo": 3, "objeto": "gorro",    "nombre": "Gorro" },
  { "modulo": 4, "objeto": "mochila",  "nombre": "Mochila", "insignia": true }
]
```

### 7.2 API

`GET /api/cursos/{curso_id}/progreso`

```json
{
  "modulos": [
    { "id": 1, "titulo": "Primeros pasos",        "estado": "completado" },
    { "id": 2, "titulo": "Control de flujo",      "estado": "actual" },
    { "id": 3, "titulo": "Estructuras de datos",  "estado": "bloqueado" },
    { "id": 4, "titulo": "Funciones y ficheros",  "estado": "bloqueado" }
  ],
  "objetos": [
    { "id": "botas",    "desbloqueado": true,  "equipado": true },
    { "id": "camiseta", "desbloqueado": false, "equipado": false },
    { "id": "gorro",    "desbloqueado": false, "equipado": false },
    { "id": "mochila",  "desbloqueado": false, "equipado": false }
  ],
  "insignia": false
}
```

`POST /api/personaje/equipar` con `{ "objeto": "botas", "equipado": true }`.

Los datos del personaje se guardan en la entidad "Recompensas y personaje" de PostgreSQL. **Nunca se envían a la IA.**

### 7.3 Regla de estados

- Un módulo está `completado` cuando el alumno ha superado todos sus fragmentos (o los ha saltado aprobando el test de la HU4).
- El primer módulo no completado es el `actual`. Los demás, `bloqueado`.
- Si el itinerario personalizado (HU2) marca un módulo como "opcional" y el alumno lo salta, cuenta como `completado` pero **no** desbloquea su objeto. Así el objeto premia haberlo hecho.

## 8. Accesibilidad

- `<svg role="img" aria-label="Progreso del curso: módulo 2 de 4, Control de flujo">`, con el texto actualizado según el estado.
- Cada parada con `aria-label`, por ejemplo: "Módulo 1, Primeros pasos, completado".
- Debajo del SVG, una lista de texto oculta visualmente (`sr-only`) con los módulos y su estado, para lectores de pantalla.

## 9. Vista del tutor (solo si da tiempo, va con la HU8)

La misma montaña, sin montañista. En cada parada, un punto de `r="4"` por alumno, repartidos en horizontal alrededor del nodo con una separación de 9 unidades, y junto al nodo el número de alumnos en esa parada. Los puntos de alumnos sin actividad en los últimos 7 días van en `#FF4950`, y el resto en `#1CF9FC`. Tocar un punto abre la ficha del alumno (solo con su ID, nunca con el nombre, en la parte que ve la IA).

## 10. Criterios de aceptación (HU6)

- [ ] La montaña muestra 4 paradas y la cima, con el estado correcto según `/progreso`.
- [ ] El montañista está en la parada actual y lleva puestos solo los objetos equipados.
- [ ] Al completar un módulo, el montañista sube con animación y aparece la hoja de objeto desbloqueado.
- [ ] Al completar el módulo 4, la bandera de la cima se pone verde y se muestra la insignia.
- [ ] Desde "Mi montañista" se pueden equipar y quitar los objetos desbloqueados.
- [ ] Todo es usable con una mano en un móvil de 375px de ancho y sin imágenes externas.
- [ ] Con `prefers-reduced-motion` no hay animaciones.
