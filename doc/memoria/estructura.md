# Estructura de la memoria del TFM

> Fichero **durable**. Define qué va en cada capítulo y, sobre todo, **qué se puede escribir
> ya y qué está bloqueado**. Los materiales (hallazgos y cifras) están en `materiales.md`;
> lo que falta medir, en `pendientes.md`.
>
> **Título:** Mitigación de Ruido Cuántico en Hardware NISQ mediante Deep Learning
> **Autor:** Gregory Harutyunyan Gevorgyan · **Director:** Pablo Abellán Galiana
> **Repositorio del código:** `TFM-Quantum` (rama `v2-dataset-exacto`)
>
> **Tipo de trabajo:** 3 — *Comparativa de soluciones*
> **Líneas:** 3 (aprendizaje automático: Ridge y Random Forest) y 4 (aprendizaje
> profundo: el *Graph Transformer*)
>
> ⚠️ **Reestructurado en ago-2026** para encajar en la estructura oficial del tipo 3
> (*Instrucciones para la redacción del TFE* §2.6). Cambios: se añadieron los capítulos
> **5 (Objetivos y metodología)** y **11 (Discusión)**, y se fusionaron los antiguos 8 y 9.

---

## El argumento de la memoria en cinco frases

1. Los ordenadores cuánticos actuales tienen tanto ruido que sus resultados son inservibles
   sin corregirlos, y la corrección de errores completa todavía no es viable.
2. La mitigación por software funciona, pero los métodos clásicos (ZNE, PEC) **cuestan
   ejecuciones extra** y los de *machine learning* del estado del arte **necesitan haber
   ejecutado ya el circuito**.
3. Este TFM pregunta si se puede predecir la degradación **antes de ejecutar**, mirando solo
   el circuito y la calibración del chip.
4. Para responderlo se construye un dataset con **tres ejes de generalización
   independientes** y se comparan **tres modelos** con protocolo idéntico: Ridge, Random
   Forest y un Graph Transformer.
5. La respuesta tiene dos partes, y **la primera obligó a replantear el objetivo**: lo que se
   quería predecir no era predecible, y averiguar por qué es el resultado central.

---

## Los doce capítulos

Cada capítulo se corresponde con un apartado de la estructura oficial del **tipo 3**.
La columna «bloque» es lo que el tribunal espera encontrar; la memoria debe decirlo
explícitamente en §1.4 para que no haya que reconstruirlo.

| # | Capítulo | Fichero | Bloque oficial | ¿Se puede escribir ya? |
|---|---|---|---|---|
| 1 | Introducción | `01_introduccion.tex` | Introducción | ✅ |
| 2 | Fundamentos de computación cuántica | `02_fundamentos.tex` | Contexto y estado del arte | ✅ |
| 3 | El ruido cuántico | `03_ruido_cuantico.tex` | Contexto y estado del arte | ✅ |
| 4 | Estado del arte | `04_estado_del_arte.tex` | Contexto y estado del arte | ✅ |
| 5 | **Objetivos y metodología de trabajo** | `05_objetivos_metodologia.tex` | Objetivos y metodología | ✅ ⚠️ nuevo |
| 6 | Planteamiento de la comparativa: el conjunto de datos | `06_dataset.tex` | Planteamiento | ✅ |
| 7 | Rigor metodológico ⭐ | `07_rigor_metodologico.tex` | Planteamiento | ✅ |
| 8 | La variable objetivo ⭐ | `08_variable_objetivo.tex` | Planteamiento | ⚠️ estructura sí, cifras no |
| 9 | Desarrollo de la comparativa: modelos y protocolo | `09_comparativa.tex` | Desarrollo | ⚠️ diseño sí, resultados no |
| 10 | Resultados | `10_resultados.tex` | Desarrollo | ❌ bloqueado |
| 11 | **Discusión y análisis de resultados** | `11_discusion.tex` | Discusión | ❌ bloqueado ⚠️ nuevo |
| 12 | Conclusiones y trabajo futuro | `12_conclusiones.tex` | Conclusiones | ❌ bloqueado |

Además: **Anexos A–C** y un **Índice de acrónimos** (§2.10, opcional pero recomendable
con la cantidad de siglas de este trabajo).

### La regla que separa el capítulo 10 del 11

No es cosmética. La norma dice del capítulo de resultados: *«Es una exposición objetiva,
**sin valorar** los resultados ni justificarlos»*. Toda interpretación —por qué gana un
modelo, qué significa, ventajas y desventajas— vive en el 11. Si al redactar el 10 aparece
un «porque» o un «esto sugiere», está en el capítulo equivocado.

Importa porque *«Desarrollo específico de la contribución»* pesa el **20 %** de la rúbrica
y nombra *«Discusión correcta de los resultados»* en las bandas de notable y sobresaliente.

**⭐ Los capítulos 7 y 8 son el diferencial de este TFM.** No son relleno metodológico: son
dos resultados propios. El 7 documenta un bug encontrado en las propias etiquetas del
dataset, medido y corregido, junto con la razón por la que el test que lo daba por bueno no
demostraba nada. El 8 documenta que la variable objetivo original no era predecible y por
qué. Un trabajo que encuentra y corrige sus propios errores vale más que uno donde todo
salió a la primera; enterrarlos en un anexo sería desperdiciarlos.

### ✅ Qué escribir ahora (capítulos 1–7 y 9)

No dependen de ninguna cifra pendiente. Son **ocho capítulos completos**, la mayor parte del
volumen de la memoria. El 5 es nuevo y se puede escribir entero desde hoy.

### ❌ Qué NO escribir todavía

* **Capítulo 10 (Resultados):** los modelos aún no están entrenados.
* **Capítulo 11 (Discusión):** depende del 10.
* **Capítulo 12 (Conclusiones):** depende del 10 y del 11.
* **Las cifras del 8 y del 9:** están medidas sobre el **dataset v1**, que tenía el bug de
  las etiquetas. Hay que rehacerlas. Ver `pendientes.md`.

---

## Qué va en cada capítulo

Entre paréntesis, la extensión objetivo. Total ≈ 71 páginas, dentro de la horquilla
**50–90** de la norma (sin contar portada, índices y anexos).

### 1 · Introducción (4 pp.)
Estructura fijada por la norma (§2.3): **Motivación · Planteamiento del problema ·
Estructura del trabajo**. Contexto NISQ · por qué el ruido bloquea la escalabilidad · por
qué la corrección completa de errores no es viable hoy · el hueco concreto que ataca el TFM
(predicción **pre-ejecución**) · **contribuciones** · recorrido por los doce capítulos.

⚠️ Aquí los objetivos van solo **a grandes rasgos**. Los objetivos formales viven en el 5.
⚠️ La norma acota este capítulo a **3–5 páginas**.

### 2 · Fundamentos de computación cuántica (4 pp.)
Lo mínimo imprescindible, sin convertirlo en un libro de texto: qubit y espacio de Hilbert ·
evolución unitaria · puertas de uno y dos qubits · medición y valores esperados · **qué es un
observable** y por qué el trabajo predice observables y no distribuciones completas.

### 3 · El ruido cuántico (5 pp.)
Estados mixtos y matriz de densidad · canales cuánticos y operadores de Kraus · las tres
fuentes físicas: decoherencia (T1/T2), error de puerta y error de lectura · **el modelo de
ruido concreto de este trabajo**: los tres canónicos de Qiskit Aer calibrados contra datos
reales de IBM · por qué el crosstalk queda fuera y qué implica.

### 4 · Estado del arte (6 pp.)
Mitigación clásica (ZNE, PEC, M3) y su coste en ejecuciones · ML aplicado a QEM (Liao 2024,
GTraQEM, QEMFormer) · el paradigma **pre-ejecución** (mapomatic, Q-CTRL) · *concept drift*
(Hirasaki, Anchor) · **el hueco**: nadie predice la magnitud del error antes de ejecutar
usando estructura del circuito más telemetría.

🔴 **Restricción dura:** los capítulos 2, 3 y 4 son el bloque «Contexto y estado del arte»,
y la norma lo acota a **10–15 páginas en total**. 4+5+6 = 15 es el techo, no un objetivo.

### 5 · Objetivos y metodología de trabajo (4 pp.) ⚠️ NUEVO
Los tres elementos que exige la norma (§2.5): **objetivo general · objetivos específicos ·
metodología de trabajo**. Los objetivos **deben ser SMART** —la norma lo llama
*imprescindible*—, y su criterio de éxito medible es el del capítulo 9: **batir a no
mitigar**. Incluye además el tipo de trabajo y las líneas, las fases, y la sección de
**herramientas empleadas** —donde va la declaración obligatoria de uso de IA—.

### 6 · Planteamiento de la comparativa: el conjunto de datos (7 pp.)
Gemelo digital de `ibm_kingston` (Heron r2) · **calibración real de 42 días**, no simulada ·
los siete tipos de circuito · **los tres ejes OOD** y por qué son independientes · la batería
de **ocho observables** y por qué ocho · el vector de 25 dimensiones por puerta · el grafo
como representación · reproducibilidad y sus límites.

### 7 · Rigor metodológico ⭐ (5 pp.)
El bug de las etiquetas del v1 y cómo se descubrió · **la lección**: repetir con la misma
semilla prueba reproducibilidad, no exactitud · la regeneración v2 y su validación · el
límite de determinismo del transpilador · las dos trampas de medición detectadas (el eje
tiempo confundido con el eje tipo; soporte fino disfrazado de tendencia).

### 8 · La variable objetivo ⭐ (5 pp.)
Qué se quería predecir (Δ) · **la medida de que no es predecible** · la explicación
aritmética: Δ = (1−f)·⟨O⟩exacto · la reformulación a *f* · por qué **no** rompe el paradigma
pre-ejecución · el límite honesto de la solución · aprobado por el director.

**Por qué el 6, el 7 y el 8 van juntos:** el bloque «Planteamiento de la comparativa» pide
*«identificar los criterios de éxito para la comparativa, las medidas que se van a tomar»*.
El capítulo 8 **es** la definición de la medida, y el 7 es lo que la hace fiable.

### 9 · Desarrollo de la comparativa: modelos y protocolo (10 pp.)
Fusión de los antiguos 8 y 9. La agregación circuito → fila y **qué información pierde** (el
núcleo de la comparativa) · el catálogo de features · las tres soluciones: Ridge y por qué no
mínimos cuadrados, Random Forest, el Graph Transformer con nodo virtual QCR · la decisión
sobre los grafos grandes · **el protocolo idéntico**: partición temporal, preprocesado,
métricas desglosadas, el listón · MLflow e infraestructura.

### 10 · Resultados — ❌ BLOQUEADO (8 pp.)
Comparativa de los tres modelos · desglose por los tres ejes y por observable · distribución
del error. **Exposición objetiva, sin valorar.**

### 11 · Discusión y análisis de resultados — ❌ BLOQUEADO (5 pp.) ⚠️ NUEVO
¿Aporta algo la estructura del circuito? · ventajas y desventajas de cada solución · qué
transfiere y qué no, eje por eje · datos anómalos · contraste con el estado del arte ·
amenazas a la validez.

### 12 · Conclusiones y trabajo futuro — ❌ BLOQUEADO (4 pp.)
Cumplimiento de objetivos —**uno a uno**, que la norma lo exige: *«cada objetivo del trabajo
se enlazará con una conclusión»*— · limitaciones sin adornar · líneas futuras
(`IDEAS_FUTURAS.md`).

---

## Reglas de redacción

1. **Toda cifra debe poder rastrearse** hasta un fichero del repositorio. Si no se sabe de
   dónde sale, no entra.
2. **Marcar el origen**: `[REPO]` lo medido por nosotros, `[EXTERNO]` lo que viene de la
   literatura, `[SUPOSICIÓN]` lo no verificado.
3. **Ninguna cita sin DOI verificado.** Los *preprints* se citan indicando que lo son.
4. **No citar cifras del v1** sin rehacerlas. Ver `pendientes.md`.
5. Las figuras salen de `TFM-Quantum/figures/`, con la paleta única del proyecto.
