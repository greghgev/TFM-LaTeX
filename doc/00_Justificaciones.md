# Justificaciones de diseño

> **Reescrito en ago-2026.** La versión anterior describía el alcance original del proyecto
> (mitigación de lectura con GNN, drift sintético, dos módulos GEM+REM). Ese alcance cambió:
> el vigente, acordado con el director, es **el módulo GEM planteado como comparativa de tres
> modelos**. La corrección de lectura vive únicamente en `IDEAS_FUTURAS.md`.
>
> Estado real del proyecto: `TFM-Quantum/ESTADO_ACTUAL.md`.

---

## 1. Por qué un gemelo digital y no hardware real

El entrenamiento necesita decenas de miles de muestras etiquetadas. Ejecutarlas en hardware
cuántico público es inviable por tres motivos independientes, y el tercero es el que de
verdad cierra la puerta:

* **Cuota.** El Open Plan de IBM da **10 minutos de QPU al mes**. Generar 20 000 circuitos
  ahí es imposible por varios órdenes de magnitud.
* **Latencia.** Las colas de ejecución hacen que un barrido de este tamaño tarde meses.
* **No existe la etiqueta.** Y este es el argumento decisivo: el modelo aprende la
  **diferencia** entre el resultado ideal y el ruidoso. El hardware real devuelve **solo el
  ruidoso**. El valor exacto no se puede medir en un ordenador cuántico — si se pudiera, no
  haría falta mitigar nada.

El simulador resuelve las tres: calcula el valor exacto de forma analítica y el ruidoso con un
modelo calibrado contra datos reales del chip.

⚠️ **Y tiene un coste que hay que declarar en la memoria:** el modelo de ruido incluye los
tres canales canónicos (despolarización calibrada, relajación térmica y lectura asimétrica)
pero **no incluye crosstalk**. Las conclusiones son válidas dentro de ese modelo; extrapolar a
hardware real requeriría validación adicional.

## 2. Por qué la calibración es real y no simulada

Los procesadores cuánticos se recalibran a diario y sus parámetros fluctúan. Un modelo
entrenado con la calibración de un solo instante no generalizaría al día siguiente.

El diseño original **simulaba** esa deriva degradando T1/T2 progresivamente. Se sustituyó por
**42 días de calibración real** de `ibm_kingston`, descargados con `BackendProperties`.

**Por qué importa el cambio:** la deriva real **no es gradual**. Hirasaki et al. (2023)
demuestran que las tasas de error cambian de forma **escalonada**, con saltos bruscos. Una
degradación lineal simulada habría enseñado al modelo un patrón que no existe.

Además, los datos reales traen cosas que nadie simularía: **puertas 100 % averiadas que IBM no
repara en 42 días**, y qubits cuya calibración viola la cota física T2 ≤ 2·T1.

## 3. Por qué el circuito se representa como grafo

Un circuito cuántico **es** un grafo acíclico dirigido: cada puerta es un nodo y las
dependencias entre puertas son las aristas. Esa representación conserva lo que importa —qué
opera sobre qué, y en qué orden— sin imponer una linealización artificial.

Cada nodo lleva **25 dimensiones**: el tipo de puerta, su ángulo, su posición en la
profundidad, el grado en el DAG, y **la telemetría real de los qubits físicos concretos sobre
los que actúa** ese día.

**Decisión de diseño deliberada: no se codifica la identidad del qubit**, solo su telemetría.
Así el modelo generaliza a cualquier número de qubits — que es justamente la crítica que se
le hace a QEMFormer, cuyo *multi-hot* de qubits lo ata al tamaño con el que se entrenó.

## 4. Por qué tres modelos y no uno

El TFM no busca demostrar que un modelo concreto es excelente, sino **medir si la estructura
del circuito aporta información real**. Eso exige una comparación controlada:

| Modelo | Qué consume | Qué representa |
|---|---|---|
| **Ridge** | una fila de features agregadas | el baseline lineal |
| **Random Forest** | la misma fila | el mejor baseline tabular según Liao et al. (2024) |
| **GEM** (Graph Transformer) | **el grafo entero** | la hipótesis del trabajo |

La agregación circuito → fila **pierde el orden y la estructura**: dos circuitos con las
mismas puertas en distinto orden dan la misma fila, y son físicamente distintos. **La
comparativa mide exactamente cuánto vale esa información que el GEM conserva y la tabla
tira.** Con protocolo idéntico para los tres, la diferencia no puede atribuirse a otra cosa.

## 5. Por qué un Graph Transformer y no una GNN convolucional

Las GNN clásicas (GCN, GraphSAGE) propagan información **entre vecinos**. En un circuito
cuántico, el entrelazamiento crea dependencias entre puertas que están **muy separadas en el
grafo**, y una GNN necesitaría tantas capas como distancia haya entre ellas.

El mecanismo de atención relaciona cualquier par de nodos **en una sola capa**. Se añade
además un **nodo virtual QCR** conectado a todos los demás: su embedding final resume el
circuito entero y es el que produce la predicción, en lugar de un promedio sobre nodos.

Arquitectura respaldada empíricamente por GTraQEM (Bao et al., ICLR 2025).

## 6. Por qué se predice *f* y no Δ

Esta es la decisión menos evidente del trabajo, y está medida, no supuesta.

El objetivo natural era **Δ = ⟨O⟩exacto − ⟨O⟩ruidoso**. Se midió que **no es predecible antes
de ejecutar**: R² ≈ 0 incluso en validación, o sea que no es un problema de generalización.

La causa es aritmética: **Δ = (1 − f)·⟨O⟩exacto**. Es el producto de un factor **aprendible**
—cuánta señal destruye el ruido, que es física del hardware— por uno que **no lo es**: cuánta
señal había, que depende del algoritmo.

La solución, **aprobada por el director**: predecir el factor de supervivencia *f* y
reconstruir Δ con el valor medido. **No rompe el paradigma pre-ejecución**, porque la entrada
del modelo no cambia — el valor medido entra solo en la aritmética final de la corrección.

Detalle completo en `TFM-Quantum/doc/hallazgo_objetivo.md`.

## 7. Por qué ocho observables

Un target escalar único habría sido una elección arbitraria imposible de justificar: para
varios tipos de circuito, algunos observables valen **cero por construcción física** — un
estado GHZ tiene magnetización media nula siempre.

La batería cubre las tres bases de Pauli (Z, X, Y), sus tres dispersiones, la paridad global y
el correlador de vecinos. **Con ocho no queda ninguna asimetría que explicar.**

**Y no cuesta nada:** el simulador calcula el estado una vez y proyecta cada observable sobre
él. Medido: 5 observables y 100 tardan lo mismo. Lo caro es el estado, no las proyecciones.

⚠️ **Matiz honesto para la memoria:** las tres dispersiones **correlacionan fuertemente entre
sí** (hasta 0,85). La justificación de las ocho es de **simetría de diseño**, no de
independencia estadística.
