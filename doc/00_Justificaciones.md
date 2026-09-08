# Justificaciones de diseño

> **Reescrito en ago-2026.** La versión anterior describía el alcance original del proyecto
> (mitigación de lectura con GNN, drift sintético, dos módulos GEM+REM). Ese alcance cambió:
> el vigente, acordado con el director, es **la mitigación de error de puerta planteada
> como comparativa de tres
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
| **GNN** (red de grafos MPNN) | **el grafo entero** | la hipótesis del trabajo |

La agregación circuito → fila **pierde el orden y la estructura**: dos circuitos con las
mismas puertas en distinto orden dan la misma fila, y son físicamente distintos. **La
comparativa mide exactamente cuánto vale esa información que el GNN conserva y la tabla
tira.** Con protocolo idéntico para los tres, la diferencia no puede atribuirse a otra cosa.

## 5. Por qué una red de grafos con nodo virtual, y no un Graph Transformer

🔴 **Esta decisión cambió el 31-ago-2026, y el cambio está medido.**

**El planteamiento inicial** era un *Graph Transformer sin paso de mensajes*, siguiendo a
GTraQEM (Bao et al., ICLR 2025). Su lógica: las GNN clásicas propagan información **entre
vecinos**, y en un circuito el entrelazamiento crea dependencias entre puertas **muy
separadas**, así que harían falta tantas capas como distancia haya. La atención relaciona
cualquier par de nodos **en una sola capa**.

**El problema, medido sobre nuestros circuitos:** para que la atención sepa que el grafo *es*
un grafo, esa arquitectura inyecta la topología mediante una **matriz de estructura** —la
distancia entre cada par de nodos, sumada al score de atención—. Pero en nuestros grafos la
**distancia mediana entre nodos conectados es de 30 a 70 pasos** (p99 hasta 157), así que con
el recorte habitual la matriz queda **constante en más del 99 % de sus entradas**. Sin recorte
no cabe en memoria. **A nuestra escala, el mecanismo no informa.**

Y hay una segunda razón: GTraQEM alimenta su modelo con el **valor ruidoso ya medido**, que
este trabajo **excluye por diseño**. Quitarle esa entrada *y* dejarla sin una matriz de
estructura útil deja lo peor de los dos mundos.

**La arquitectura vigente** es un **MPNN con paso de mensajes** —donde la topología entra
gratis por las aristas, sin matriz ninguna— **más un nodo virtual bidireccional** conectado a
todos los nodos, cuyo embedding se concatena con el *pooling* de los nodos físicos para
producir la predicción.

🔴 **El nodo virtual debe ser BIDIRECCIONAL**, y ésta es la diferencia clave con el diseño del
paper. En un Transformer la atención ya conecta todo con todo, así que un nodo virtual que solo
*lee* basta. En una red de paso de mensajes **no**: los mensajes viajan un salto por capa y solo
por aristas, de modo que un nodo virtual sin salidas **acumula pero no devuelve**. Y con 4-6
capas frente a distancias de 30-70 pasos, la propagación por aristas es **puramente local**:
el nodo virtual es la **única vía al largo alcance** del modelo.

**Efecto colateral favorable:** con paso de mensajes la memoria es **lineal** en nodos y
aristas en vez de cuadrática, así que **desaparece la necesidad de truncar los grafos** — y con
ella un sesgo metodológico que castigaba más al entrenamiento que al test.

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

## 7. Por qué una batería de observables — y por qué cinco, no ocho

Un target escalar único habría sido una elección arbitraria imposible de justificar: para
varios tipos de circuito, algunos observables valen **cero por construcción física** — un
estado GHZ tiene magnetización media nula siempre.

✅ **Confirmado con bootstrap sobre el v2:** 6 de los 7 tipos tienen observable óptimo con
veredicto sólido y hay **cuatro óptimos distintos**. La cifra citable del QFT es **3,69×**
(nunca 42,7× ni 45,4×: eran del v1 y se contradecían entre sí).

**Y ampliar la batería no cuesta nada:** el simulador calcula el estado una vez y proyecta cada
observable sobre él. Medido: 5 observables y 100 tardan lo mismo. Lo caro es el estado.

### 🔴 El dataset guarda 8; el modelo entrena sobre 5

```
mean_Z · mean_X · mean_Y · paridad · corr_vecinos
└── las tres bases de Pauli ──┘  └── dos correladores ──┘
```

Se retiraron las tres dispersiones (`std_Z`, `std_X`, `std_Y`) en ago-2026, por dos motivos:

1. **Simetría.** «Las tres bases de Pauli y dos correladores»: no queda ninguna dispersión
   elegida a dedo, que era justamente la asimetría que motivó ampliar de 5 a 8. **El conjunto
   final es más simétrico que el original.**
2. **Medido.** El ruido no solo atenúa, también desplaza (`ruidoso = f·exacto + b`), y en ese
   bloque el desplazamiento vale el **135–149 %** de la degradación que se quiere predecir,
   además de variar con el tamaño ~14× más que en el resto. Contaminaría un modelo
   multi-salida con estructura compartida.

⚠️ **Siguen guardadas en el dataset**: retirarlas del objetivo no obligó a regenerar nada y
permite reactivarlas para un estudio de ablación.

---

## 8. Por qué hay una cola de *f* desmedida, y por qué no es un fallo

Con el umbral de señal en 0,002, el **7,85 %** de las etiquetas de `train` queda por encima
de 1 y el máximo de |*f*| llega a **6,67**. Un factor de supervivencia mayor que 1 significa
que el circuito ruidoso da un valor esperado *más grande* que el ideal, que no es lo que uno
espera del ruido. La explicación no es física: es aritmética.

El ruido de este hardware es **afín**, no solo multiplicativo:

$$\text{ruidoso} = f \cdot \text{exacto} + b$$

donde *b* es el desplazamiento aditivo que introducen sobre todo los errores de lectura. Al
construir la etiqueta se divide por el valor exacto:

$$\frac{\text{ruidoso}}{\text{exacto}} = f + \frac{b}{\text{exacto}}$$

Es decir, **la etiqueta no es *f*: es *f* más un término *b*/exacto**. Ese segundo término es
despreciable mientras el denominador sea grande, pero crece sin límite según el observable se
acerca a cero. Como la mediana de |exacto| en este dataset es **0,0347**, hay bastantes
circuitos en los que un *b* pequeñísimo se convierte en una contribución enorme.

La cola es, por tanto, **el sesgo aditivo dividido por un denominador diminuto**, y no una
degradación anómala. Es también lo que justifica el umbral de señal: al exigir
|exacto| > 0,002 se corta la parte del recorrido donde ese cociente domina por completo a la
etiqueta. Lo que queda por encima de 1 después del umbral es la cola residual del mismo
efecto.

⚠️ *b* se ha **medido** pero no se modela: el objetivo del TFM es *f*, y añadir un segundo
objetivo para *b* no compensaba por lo poco que aporta.
