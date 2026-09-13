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
| `cap05/objetivo_r2.pdf` | 5 · R² de las tres candidatas | elaboración propia (`notebooks/01_eda/01c`) | — |
| `cap05/umbral_barrido.pdf` | 5 · barrido del umbral de señal | elaboración propia (`notebooks/01_eda/01d`) | — |
| `cap05/f_distribuciones.pdf` | 5 · distribución del factor | elaboración propia (`notebooks/01_eda/01e`) | — |
| `cap05/f_vs_tamano.pdf` | 5 · factor frente al número de qubits | elaboración propia (`notebooks/01_eda/01e`) | — |
| `cap05/reconstruccion_tikz.tex` | 5 · dónde entra cada dato | elaboración propia (TikZ) | — |
| `cap05/pauli_tikz.tex` | 5 · los tres operadores de Pauli | elaboración propia (TikZ) | — |
| `cap05/obs_rangos_y_efecto.pdf` | 5 · dónde vive cada observable y qué le hace el ruido | elaboración propia (`notebooks/01_eda/01b`) | — |
| `cap05/f_correlaciones.pdf` | 5 · correlación entre los cinco objetivos | elaboración propia (`notebooks/01_eda/01e`) | — |
| `cap05/umbral_huecos.pdf` | 5 · casillas que pierde cada observable | elaboración propia (`notebooks/01_eda/01f`) | — |
| `cap06/tres_ejes_tikz.tex` | 6 · los tres ejes de generalización | elaboración propia (TikZ) | — |
| `cap06/drift_t1.pdf` | 6 · la deriva real del chip en 42 días | elaboración propia (`notebooks/00_anatomia`) | — |
| `cap06/nodo_escalas.pdf` | 6 · el recorrido de cada dimensión del nodo | elaboración propia (`notebooks/04_gnn`) | — |
| `cap06/nodo_ceros.pdf` | 6 · el cero que significa «no aplica» | elaboración propia (`notebooks/04_gnn`) | — |
| `cap06/campo_receptivo.pdf` | 6 · alcance del paso de mensajes | elaboración propia (`notebooks/04_gnn`) | — |
| `cap06/mapa_averias.pdf` | 6 · las averías crónicas del chip | elaboración propia (`notebooks/00_anatomia/00b`) | — |
| `cap06/region_chip.pdf` | 6 · la región conexa de un circuito | elaboración propia (`notebooks/00_anatomia/00b`) | — |

⚠️ **Pendiente sobre `cap01/ibm_cuantico.jpg`.** La fuente es un medio que republica la
imagen sin declarar licencia; con toda probabilidad es material gráfico de IBM o una
fotografía tomada en una feria. **Antes de la entrega** hay que localizar el origen primario
y sus condiciones de uso, o sustituirla por una del banco de imágenes de IBM Research, que
sí las publica.

`cap01/mlqem_flujo.pdf` se regenera con
`rsvg-convert -f pdf -o mlqem_flujo.pdf mlqem_flujo.svg`.

Convertido con `rsvg-convert -f pdf -o bloch.pdf bloch.svg`. Se conserva el SVG para
poder regenerarlo o editarlo.

Las siete figuras `cap05/*.pdf` se generan en `TFM-Quantum/figures/eda/` y se copian aquí.
Para regenerarlas hay que reejecutar los cuadernos `01b`, `01c`, `01d`, `01e` y `01f` de la EDA y
volver a copiar. Origen de cada una:

| fichero en la memoria | origen en `figures/eda/` | cuaderno |
|---|---|---|
| `obs_rangos_y_efecto.pdf` | `observables/02_rangos_y_efecto` | `01b` |
| `objetivo_r2.pdf` | `objetivo/02_variable_objetivo_memoria` | `01c` |
| `umbral_barrido.pdf` | `umbral/04_barrido_memoria` | `01d` |
| `umbral_huecos.pdf` | `nulos/02_huecos_memoria` | `01f` |
| `f_distribuciones.pdf` | `factor/06_distribuciones_memoria` | `01e` |
| `f_vs_tamano.pdf` | `factor/02_f_vs_tamano` | `01e` |
| `f_correlaciones.pdf` | `factor/05_correlaciones_memoria` | `01e` |

⚠️ **Las seis salen sin título dentro de la imagen**, porque el título lo pone el `\caption`
de LaTeX (norma del TFE, apartado 1.3). Todas las genera una función `*_memoria()` **aparte**;
las originales, con título, se conservan intactas para los cuadernos:

| figura | función que la dibuja |
|---|---|
| `obs_rangos_y_efecto.pdf` | `observable.dibujar_rangos_y_efecto()` |
| `objetivo_r2.pdf` | `variable_objetivo.dibujar_comparativa_memoria()` |
| `umbral_barrido.pdf` | `umbral.dibujar_barrido_memoria()` |
| `umbral_huecos.pdf` | `nulos.dibujar_perfil_memoria()` |
| `f_distribuciones.pdf` | `factor.dibujar_distribuciones_memoria()` |
| `f_correlaciones.pdf` | `factor.dibujar_correlaciones_memoria()` |

(`f_vs_tamano.pdf` sigue saliendo de `factor.dibujar_tendencia()`, que es genérica.)

⚠️ **El `figsize` de todas ellas está calculado para la caja de 15 cm del TFM**: a
`\textwidth` se imprimen a escala ~0,6, y por eso sus cuerpos de letra son de 11–12 pt en
origen, para llegar al papel como 7–8 pt. Agrandar una figura sin subir sus fuentes deja la
letra ilegible en el PDF; es el motivo por el que existen las variantes `*_memoria()`.

## Figuras copiadas y NO usadas

En `figuras/cap06/` hay cuatro ficheros que **no** se incluyen desde el `.tex`. Se copiaron al
preparar el capítulo 6 y se retiraron al recortarlo a veinte páginas; se dejan en disco por si
se quieren reponer:

| fichero | por qué se retiró |
|---|---|
| `mapa_features.pdf` | ocupaba una página entera y sus 54 nombres de fila salen ilegibles al escalarla |
| `particion.pdf` | un anillo con el reparto 13.344 / 2.656 / 4.000, que es una frase |
| `tres_ejes.pdf` | rehecha en TikZ (`tres_ejes_tikz.tex`): tres cajas en fila no decían que los tres ejes salen del mismo conjunto |
| `colinealidad.pdf` | matriz 54×54 con los nombres ilegibles; su mensaje está en el texto |

(`region_chip.pdf` volvió al capítulo en sep-2026, emparejada con `mapa_averias.pdf`.)

⚠️ **`mapa_averias.pdf` y `region_chip.pdf` van a media anchura y sus números de qubit NO se
leen.** Es una decisión consciente del autor: la figura sirve para ver *dónde* están las averías
y *dónde* cae la región, no para localizar un qubit concreto. Las genera el cuaderno `00b` con
`titulo=""`, que es lo que deja la imagen sin título interno.

Las dos que quedaron ilegibles lo están por escala: a `\textwidth` se imprimen a menos de la
mitad de su tamaño de origen. Si se quieren reponer, hay que rehacerlas apaisadas a página
completa, no simplemente volver a incluirlas.
