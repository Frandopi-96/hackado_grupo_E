# DESIGN.md: 480 Academy (prototipo PWA)

Guía visual del prototipo. Los valores salen de dos fuentes:

- El paquete de logos oficial **480 Media Brand 2025** (colores exactos en los SVG).
- Los estilos calculados de **cuatroochenta.com**, leídos desde el navegador el 25/11/2026.

No copiamos la web: tomamos su lenguaje visual (colores, tipografía, formas) y lo adaptamos a una app de estudio mobile-first.

## 1. Personalidad

Tecnológica, directa y con contraste alto. La web de Cuatroochenta usa una cabecera casi negra con un brillo verde neón, titulares en verde y bloques de contenido en blanco más abajo. Esquinas casi rectas, pocas sombras y mucho peso en la tipografía.

Para la app usamos **modo oscuro por defecto**: es donde los colores neón de la marca funcionan (sobre blanco no se leen) y gasta menos batería en muchos móviles.

## 2. Colores

| Token | Hex | Uso en la app | Contraste |
|---|---|---|---|
| `marca-oscuro` | `#1F2222` | Fondo principal | — |
| `marca-verde` | `#39FE90` | Aciertos, progreso, subida en la montaña, botón principal | 12,0 sobre oscuro |
| `marca-cian` | `#1CF9FC` | Enlaces, elementos interactivos secundarios, foco | 12,2 sobre oscuro |
| `marca-rojo` | `#FF4950` | Errores y alertas (en la web, el botón "Contacto") | 4,8 sobre oscuro |
| `blanco` | `#FFFFFF` | Texto principal sobre oscuro | 16,0 sobre oscuro |
| `gris-claro` | `#D0D5D2` | Texto secundario sobre oscuro, bordes | 10,8 sobre oscuro |
| `gris-texto` | `#4D4D4D` | Texto sobre fondos claros (tarjetas claras, si se usan) | 8,5 sobre blanco |
| `superficie-clara` | `#F7F7F7` | Fondos claros puntuales | — |

Reglas:
- **Nunca** texto verde, cian o rojo sobre blanco (contraste 1,3 a 3,3, ilegible).
- Botón principal: fondo verde con texto `#1F2222` (contraste 12).
- El rojo solo para errores, que es también su significado natural en un test.

## 3. Tipografía

La web usa **LL Circular** (Book 400, Medium, Bold), una fuente comercial de Lineto. No tenemos licencia, así que usamos **DM Sans** (Google Fonts, gratuita), que es geométrica y muy parecida.

```
font-family: "DM Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
```

| Elemento | Web (escritorio) | App (móvil) | Peso |
|---|---|---|---|
| Título de pantalla | 44px | 28px | Bold (700) |
| Subtítulo | 31px | 22px | Bold (700) |
| Texto normal | 17,4px | 16px, interlineado 1,5 | Regular (400) |
| Texto pequeño / etiquetas | 14px | 14px | Medium (500) |

En la web, algunos titulares de noticias van en mayúsculas con guiones bajos (`CUATROOCHENTA_CRECE_UN_14%`), un guiño "de código". Se puede usar con moderación en etiquetas, por ejemplo `MÓDULO_02`.

## 4. Espaciado y maquetación

- Escala de espaciado de 4 en 4: 4, 8, 12, 16, 24, 32, 48px.
- Margen lateral en móvil: 16px.
- Botones y zonas táctiles de al menos 44px de alto.
- Acciones principales en la mitad inferior de la pantalla, para usar la app con una mano.

## 5. Bordes, radios y sombras

- Radios pequeños, casi rectos: **2 a 4px** en botones y tarjetas (en la web, 3,2px es el más usado).
- Radio de píldora (**50px**) solo para chips y etiquetas.
- Sombras casi inexistentes. Para separar capas usamos bordes `#D0D5D2` al 20 % de opacidad o un fondo ligeramente más claro (`#2A2E2E`).

## 6. Componentes

- **Botón principal:** fondo `marca-verde`, texto `marca-oscuro`, Bold 16px, radio 4px, alto 48px, ancho completo en móvil.
- **Botón secundario:** borde de 2px `marca-cian`, fondo transparente, texto `marca-cian`.
- **Tarjeta (fragmento, tarjeta del Modo 4G):** fondo `#2A2E2E`, radio 4px, padding 16px, borde sutil.
- **Respuesta de test:** neutra con borde gris; al acertar, borde y check en verde; al fallar, borde rojo y explicación debajo.
- **Barra de progreso:** fondo `#2A2E2E`, relleno `marca-verde`.
- **Logo:** `480 Color White fondo.svg` (carpeta `Sin margen seguridad/RGB Digital`) sobre fondo oscuro. Pesa menos de 2 KB.

## 7. Imagen, iconos y movimiento

- Brillo verde difuminado detrás de la cabecera, como en la web (degradado radial de `#39FE90` al 15 % hacia transparente).
- Iconos de trazo simple, en blanco o cian.
- Animaciones cortas (150 a 200ms), sobre todo al acertar una pregunta y al subir el personaje en la montaña.

## 8. Implementación (Tailwind)

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        marca: {
          oscuro: '#1F2222',
          superficie: '#2A2E2E',
          verde: '#39FE90',
          cian: '#1CF9FC',
          rojo: '#FF4950',
          gris: '#D0D5D2',
        },
      },
      fontFamily: {
        sans: ['"DM Sans"', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'sans-serif'],
      },
      borderRadius: {
        marca: '4px',
      },
    },
  },
};
```

Botón principal:

```html
<button class="w-full h-12 rounded-marca bg-marca-verde text-marca-oscuro font-bold">
  Continuar
</button>
```

Tarjeta de pregunta:

```html
<div class="rounded-marca bg-marca-superficie p-4 border border-marca-gris/20">
  <p class="text-sm font-medium text-marca-cian">MÓDULO_02</p>
  <p class="mt-2 text-white">¿Qué devuelve len([1, 2, 3])?</p>
</div>
```

## 9. Fuentes

- Paquete de logos **480 Media Brand 2025** (SVG en `RGB Digital`).
- Estilos calculados de la portada de **cuatroochenta.com**, leídos con el navegador el 25/11/2026.
- Contrastes calculados con la fórmula WCAG 2.1 (mínimo recomendado para texto: 4,5).
