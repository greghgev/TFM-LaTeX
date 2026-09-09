# Figuras de la memoria

## Convención de organización

Una carpeta por capítulo, con el número a dos dígitos:

```
figuras/
├── cap01/   Introducción
├── cap02/   Fundamentos
├── cap03/   El ruido cuántico
├── ...
└── cap12/   Conclusiones
```

En el `.tex` se referencia **con la subcarpeta y sin extensión**:

```latex
\includegraphics[width=0.4\textwidth]{cap02/bloch}
```

`\graphicspath` en `preambulo.tex` apunta solo a `figuras/`, así que la ruta del
capítulo forma parte del nombre. Es lo que evita tener que tocar el preámbulo cada vez
que se añade un capítulo con figuras.

## Formatos admitidos

`pdflatex` acepta **PDF, PNG y JPG**. No acepta WebP, SVG, GIF ni TIFF.

* **Diagramas y esquemas → PDF.** Es vectorial: se ve nítido a cualquier tamaño y no
  engorda el fichero. Si el original es un SVG, convertirlo con
  `rsvg-convert -f pdf -o salida.pdf entrada.svg`.
* **Capturas y gráficas rasterizadas → PNG.**
* **Fotografías → JPG.**

### Resolución mínima

Para que una imagen no se vea pixelada impresa hacen falta **300 dpi al tamaño final**.
El ancho de caja de esta memoria es de 15,02 cm, así que:

| ancho en el texto | cm | píxeles necesarios para 300 dpi |
|---|---|---|
| `0.4\textwidth` | 6,0 | ~710 |
| `0.6\textwidth` | 9,0 | ~1060 |
| `\textwidth`    | 15,0 | ~1770 |

Si la imagen no llega, la solución **no** es escalarla: es conseguir el original en
vectorial y exportarlo a PDF.

## Formato exigido por la normativa

Instrucciones del TFE, apartado 1.3, **página 6**:

* **Título en la parte superior** de la tabla o figura → el `\caption` va **antes** del
  `\includegraphics`.
* **Fuente en la parte inferior**, centrada y en cuerpo menor.

⚠️ La plantilla oficial de LaTeX hace lo contrario en su ejemplo (pone el `\caption`
debajo). Aquí manda la norma escrita, que es la que lee el tribunal.

## Atribución

Toda figura lleva su fuente. `Fuente: elaboración propia.` **solo** si es tuya de
verdad. Si procede de un tercero hay que citarla, respetar su licencia y, si es
*copyleft* (CC BY-SA y similares), indicar autor y licencia.

## Inventario

| fichero | capítulo | origen | licencia |
|---|---|---|---|
| `cap01/ibm_cuantico.jpg` | 1 · criostato de IBM | Clipset (2018), `i0.wp.com/clipset.com/wp-content/uploads/2018/01/ibm-cuantico4.jpg` | ⚠️ **SIN LICENCIA DECLARADA** — ver aviso abajo |
| `cap01/mlqem_flujo.pdf` | 1 · flujo ML-QEM | elaboración propia | — |
| `cap01/mlqem_flujo.svg` | — | fuente editable del anterior | — |
| `cap02/bloch.pdf` | 2 · esfera de Bloch | Glosser.ca (2012), Wikimedia Commons | **CC BY-SA 3.0** — obliga a citar autor y licencia |
| `cap02/bloch.svg` | — | fuente editable del anterior | ídem |
| `cap02/dag_circuito.pdf` | 2 · **retirada de la memoria** en sep-2026 | elaboración propia | se conserva por si hay que reponerla |

⚠️ **Pendiente sobre `cap01/ibm_cuantico.jpg`.** La fuente es un medio que republica la
imagen sin declarar licencia; con toda probabilidad es material gráfico de IBM o una
fotografía tomada en una feria. **Antes de la entrega** hay que localizar el origen primario
y sus condiciones de uso, o sustituirla por una del banco de imágenes de IBM Research, que
sí las publica.

`cap01/mlqem_flujo.pdf` se regenera con
`rsvg-convert -f pdf -o mlqem_flujo.pdf mlqem_flujo.svg`.

Convertido con `rsvg-convert -f pdf -o bloch.pdf bloch.svg`. Se conserva el SVG para
poder regenerarlo o editarlo.
