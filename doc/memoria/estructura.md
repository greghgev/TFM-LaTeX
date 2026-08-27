# Estructura de la memoria del TFM

> Fichero **durable**. Define qué va en cada capítulo y, sobre todo, **qué se puede escribir
> ya y qué está bloqueado**. Los materiales (hallazgos y cifras) están en `materiales.md`;
> lo que falta medir, en `pendientes.md`.
>
> **Título:** Mitigación de Ruido Cuántico en Hardware NISQ mediante Deep Learning
> **Autor:** Gregory Harutyunyan Gevorgyan · **Director:** Pablo Abellán Galiana
> **Repositorio del código:** `TFM-Quantum` (rama `v2-dataset-exacto`)

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

## Los once capítulos

| # | Capítulo | Fichero | ¿Se puede escribir ya? |
|---|---|---|---|
| 1 | Introducción | `01_introduccion.tex` | ✅ |
| 2 | Fundamentos de computación cuántica | `02_fundamentos.tex` | ✅ |
| 3 | El ruido cuántico | `03_ruido_cuantico.tex` | ✅ |
| 4 | Estado del arte | `04_estado_del_arte.tex` | ✅ |
| 5 | Diseño del dataset | `05_dataset.tex` | ✅ |
| 6 | Rigor metodológico ⭐ | `06_rigor_metodologico.tex` | ✅ |
| 7 | La variable objetivo ⭐ | `07_variable_objetivo.tex` | ⚠️ estructura sí, cifras no |
| 8 | Los tres modelos | `08_modelos.tex` | ⚠️ diseño sí, resultados no |
| 9 | Protocolo experimental | `09_protocolo.tex` | ✅ |
| 10 | Resultados | `10_resultados.tex` | ❌ bloqueado |
| 11 | Conclusiones y trabajo futuro | `11_conclusiones.tex` | ❌ bloqueado |

**⭐ Los capítulos 6 y 7 son el diferencial de este TFM.** No son relleno metodológico: son
dos resultados propios. El 6 documenta un bug encontrado en las propias etiquetas del
dataset, medido y corregido, junto con la razón por la que el test que lo daba por bueno no
demostraba nada. El 7 documenta que la variable objetivo original no era predecible y por
qué. Un trabajo que encuentra y corrige sus propios errores vale más que uno donde todo
salió a la primera; enterrarlos en un anexo sería desperdiciarlos.

### ✅ Qué escribir ahora (capítulos 1–6 y 9)

No dependen de ninguna cifra pendiente. Son **siete capítulos completos**, la mayor parte del
volumen de la memoria.

### ❌ Qué NO escribir todavía

* **Capítulo 10 (Resultados):** los modelos aún no están entrenados.
* **Capítulo 11 (Conclusiones):** dependen del 10.
* **Las cifras del 7 y del 8:** están medidas sobre el **dataset v1**, que tenía el bug de
  las etiquetas. Hay que rehacerlas. Ver `pendientes.md`.

---

## Qué va en cada capítulo

### 1 · Introducción
Contexto NISQ · por qué el ruido bloquea la escalabilidad · por qué la corrección completa de
errores no es viable hoy · el hueco concreto que ataca el TFM (predicción **pre-ejecución**)
· objetivos general y específicos · **contribuciones** · estructura del documento.

⚠️ Los objetivos actuales del esqueleto son del alcance antiguo (hablan de REM y de
validación en hardware). El alcance vigente es **el módulo GEM como comparativa de tres
modelos**, acordado con el director.

### 2 · Fundamentos de computación cuántica
Lo mínimo imprescindible, sin convertirlo en un libro de texto: qubit y espacio de Hilbert ·
evolución unitaria · puertas de uno y dos qubits · medición y valores esperados · **qué es un
observable** y por qué el trabajo predice observables y no distribuciones completas.

### 3 · El ruido cuántico
Estados mixtos y matriz de densidad · canales cuánticos y operadores de Kraus · las tres
fuentes físicas: decoherencia (T1/T2), error de puerta y error de lectura · **el modelo de
ruido concreto de este trabajo**: los tres canónicos de Qiskit Aer calibrados contra datos
reales de IBM · por qué el crosstalk queda fuera y qué implica.

### 4 · Estado del arte
Mitigación clásica (ZNE, PEC, M3) y su coste en ejecuciones · ML aplicado a QEM (Liao 2024,
GTraQEM, QEMFormer) · el paradigma **pre-ejecución** (mapomatic, Q-CTRL) · *concept drift*
(Hirasaki, Anchor) · **el hueco**: nadie predice la magnitud del error antes de ejecutar
usando estructura del circuito más telemetría.

### 5 · Diseño del dataset
Gemelo digital de `ibm_kingston` (Heron r2) · **calibración real de 42 días**, no simulada ·
los siete tipos de circuito · **los tres ejes OOD** y por qué son independientes · la batería
de **ocho observables** y por qué ocho · el vector de 25 dimensiones por puerta · el grafo
como representación · reproducibilidad y sus límites.

### 6 · Rigor metodológico ⭐
El bug de las etiquetas del v1 y cómo se descubrió · **la lección**: repetir con la misma
semilla prueba reproducibilidad, no exactitud · la regeneración v2 y su validación · el
límite de determinismo del transpilador · las dos trampas de medición detectadas (el eje
tiempo confundido con el eje tipo; soporte fino disfrazado de tendencia).

### 7 · La variable objetivo ⭐
Qué se quería predecir (Δ) · **la medida de que no es predecible** · la explicación
aritmética: Δ = (1−f)·⟨O⟩exacto · la reformulación a *f* · por qué **no** rompe el paradigma
pre-ejecución · el límite honesto de la solución · aprobado por el director.

### 8 · Los tres modelos
La agregación circuito → fila y **qué información pierde** (el núcleo de la comparativa) ·
el catálogo de features · Ridge y por qué no mínimos cuadrados · Random Forest · el Graph
Transformer con nodo virtual QCR · la decisión sobre los grafos grandes.

### 9 · Protocolo experimental
La partición temporal y por qué no aleatoria · **el protocolo idéntico** para los tres
modelos · las métricas y su desglose por eje OOD y por observable · MLflow · la
infraestructura de cómputo.

### 10 · Resultados — ❌ BLOQUEADO
Comparativa de los tres modelos · desglose por los tres ejes · qué transfiere y qué no.

### 11 · Conclusiones y trabajo futuro — ❌ BLOQUEADO
Cumplimiento de objetivos · limitaciones sin adornar · líneas futuras (`IDEAS_FUTURAS.md`).

---

## Reglas de redacción

1. **Toda cifra debe poder rastrearse** hasta un fichero del repositorio. Si no se sabe de
   dónde sale, no entra.
2. **Marcar el origen**: `[REPO]` lo medido por nosotros, `[EXTERNO]` lo que viene de la
   literatura, `[SUPOSICIÓN]` lo no verificado.
3. **Ninguna cita sin DOI verificado.** Los *preprints* se citan indicando que lo son.
4. **No citar cifras del v1** sin rehacerlas. Ver `pendientes.md`.
5. Las figuras salen de `TFM-Quantum/figures/`, con la paleta única del proyecto.
