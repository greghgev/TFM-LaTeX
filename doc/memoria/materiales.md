# Materiales para la memoria — hallazgos y cifras con su origen

> Fichero **durable**. Recoge todo lo medido en el proyecto, **con la fuente de cada cifra**
> y marcado si procede del dataset v1 (obsoleto) o del v2 (vigente).
>
> 🔴 **Regla:** ninguna cifra marcada `[v1]` puede ir a la memoria sin rehacerla. Ver
> `pendientes.md`.

**Leyenda:** `[REPO]` medido por nosotros · `[EXTERNO]` de la literatura ·
`[SUPOSICIÓN]` no verificado · `[v1]` dataset viejo, con el bug · `[v2]` dataset vigente.

---

## 1. El dataset

| Dato | Valor | Origen |
|---|---|---|
| Backend simulado | `ibm_kingston` — IBM Heron r2, 156 qubits, puerta 2q nativa **CZ** | `[REPO]` |
| Días de calibración **real** | **42** (13-jun → 27-jul-2026) | `[REPO]` `[v2]` |
| Muestras generadas | **19 631** de 20 000 ⏳ faltan 369 de n=15 | `[REPO]` `[v2]` |
| Reparto | 16 000 `train_val` + 3 631 `test` | `[REPO]` `[v2]` |
| Nodos totales | **17 812 123** | `[REPO]` `[v2]` |
| Método de simulación | `density_matrix` **forzado** | `[REPO]` `[v2]` |
| Observables | **8**: mean_Z, mean_X, mean_Y, std_Z, std_X, std_Y, paridad, corr_vecinos | `[REPO]` `[v2]` |
| Features por puerta | 25 dimensiones | `[REPO]` |
| Puertas 100 % rotas | 1,47 % de los nodos — **dato real de IBM**, no un error | `[REPO]` |

### Los tres ejes OOD

| Eje | Cómo se consigue | Estado |
|---|---|---|
| **Tipo** | train = 100 % random; test = 6 tipos nunca vistos | ✅ completo |
| **Tamaño** | train n ≤ 11; test n = 12–15 | ⚠️ **76,8 %** (1 220 muestras; faltan 369) |
| **Tiempo** | días de calibración disjuntos entre grupos | ✅ completo |

### Tamaño de los grafos `[REPO]` `[v2]`

| | valor |
|---|---|
| mediana | 686 nodos |
| p90 | 2 016 |
| p99 | 3 619 |
| máximo | 6 894 ⏳ (subirá a ~8 000 con los n=15) |

Coste de la atención completa en el peor caso: **190 MB** por cabeza y muestra (≈276 MB con
los n=15). Truncar a 2 000 nodos afecta al **10,16 %** de las muestras y divide el coste por
**11,9**.

---

## 2. Hallazgos sobre el hardware `[REPO]`

1. **La `rz` tiene error exactamente cero** en las 6 552 medidas. No es un hueco del dato: en
   hardware IBM la `rz` es **virtual** — cambia la fase de referencia del pulso siguiente y
   no emite ningún pulso. Es gratis, y por eso el transpilador la usa sin límite.
2. **`id`, `sx` y `x` traen valores IDÉNTICOS** de `gate_error` (correlación 1,000000 en el
   100 % de los qubits): IBM las deriva del mismo pulso calibrado. ⚠️ La variable
   `gate_error` **no distingue** una `sx` de una `x`; quien las distingue es el one-hot.
3. **IBM no repara las averías.** De 27 puertas que fallaron alguna vez, **17 están rotas los
   42 días sin excepción**, concentradas en la mitad inferior del chip.
4. **El 0,92 % de las medidas viola la cota física T2 ≤ 2·T1**, pero **55 de las 60 son solo
   dos qubits vecinos averiados**. La calibración de un qubit roto no es fiable.
5. **La calibración trae 1 952 registros de puerta, pero de 10 tipos** — incluye `rx`, `rzz`,
   `reset`, `measure`. Las de la base nativa son **976 por día**. Cualquier estadística de
   error de puerta debe filtrar por `BASIS_GATES`.

---

## 3. 🔴 El bug de las etiquetas (capítulo 7)

**Qué pasaba.** El estimador ruidoso no fijaba `method`, así que Aer usaba `automatic` y
elegía según **la RAM libre**: `density_matrix` (exacto) mientras cupiera, y **trayectorias
de Kraus (Montecarlo) en cuanto dejaba de caber** — sin avisar. En una máquina de 11 GB el
cambio ocurría en **n = 10**.

| | Valor | Origen |
|---|---|---|
| Ruido metido en las etiquetas | σ ≈ **1,5×10⁻³** | `[REPO]` |
| Muestras afectadas | **33,9 %** del total · **56,3 % del test** | `[REPO]` |
| Techo de R² que imponía | 0,98–0,997 (no era grave) | `[REPO]` |
| Suelo de MAE que imponía | 0,0012 → **el 40 % del listón** en `mean_Z` (sí era grave) | `[REPO]` |

### La lección metodológica — el corazón del capítulo 7

La documentación afirmaba que las etiquetas eran analíticas, *"verificado ejecutando el mismo
circuito 5 veces con resultado idéntico bit a bit"*.

**Ese test no probaba lo que decía probar.** Repetir con la misma semilla demuestra
**reproducibilidad**, no ausencia de ruido: un simulador estocástico con semilla fija
devuelve siempre el mismo número, y ese número puede estar igual de equivocado las cinco
veces.

⚠️ Y el mismo error se repitió al investigarlo: la primera comprobación con semillas
distintas se hizo en **n = 8**, donde el método todavía era exacto, y dio "sin dispersión".
Solo al repetirla en n = 10 y n = 12 apareció el problema.

**Regla que queda:** para afirmar que un cálculo es exacto hay que variar **la fuente de
aleatoriedad**, y hacerlo **en todo el rango de parámetros**, no en un punto cómodo.

### Qué se arregló

* `method="density_matrix"` **forzado**: si no cabe en memoria, **falla ruidosamente** en vez
  de degradar la exactitud en silencio. Coste: 4ⁿ × 16 bytes por proceso.
* Cada `.pt` registra `metodo`. **Es lo que habría delatado el bug en dos segundos.**
* `MANIFEST.json` con versiones, semilla y configuración.
* De paso: 5 → 8 observables, y `z_per_qubit` → `por_qubit [3,n]`.

### El límite de reproducibilidad del transpilador `[REPO]`

**`transpile()` con `seed_transpiler` fijado NO produce siempre el mismo circuito.**

⚠️ **Cifras corregidas (ago-2026).** Las primeras salían de una prueba de **24 muestras** y se
quedaban muy cortas. Medido sobre **13.217 muestras** de n ≤ 9 comparables con el v1:

| | primera estimación (24 muestras) | **medido (13.217 muestras)** |
|---|---|---|
| muestras afectadas | ~4 % | **12,65 %** |
| divergencia en `ruidoso` | 2×10⁻⁵ – 1,6×10⁻⁴ | **hasta 1,45×10⁻²** (mediana 0 · p90 3×10⁻⁵ · p99 5,9×10⁻⁴) |
| divergencia en `exacto` | idéntico | **idéntico** (máx 1,2×10⁻⁶, ruido de float32) |

🔴 **En la memoria citar 12,65 % y 1,45×10⁻², NUNCA 4 % ni 1,6×10⁻⁴.**

**Sigue siendo benigno**, y que el `exacto` sea idéntico es justamente la prueba: las dos
transpilaciones implementan **la misma unitaria**. Solo el `ruidoso` difiere, porque el ruido
no conmuta con la unitaria.

**Lo que hay que matizar en la memoria:** el dataset es reproducible a partir de las semillas
para el **plan** (qué tipo, cuántos qubits, qué día, qué región), pero **no al bit** para el
circuito transpilado.

---

## 4. 🔴 La variable objetivo (capítulo 8)

**El hallazgo:** Δ con signo **no es predecible antes de ejecutar**. R² ≈ 0 **en validación**,
o sea que no es un problema de generalización.

| Objetivo | R² val (Ridge) | R² val (RF) | Origen |
|---|---|---|---|
| **Δ con signo** | −0,005 … +0,001 | −0,025 … −0,011 | `[REPO]` **`[v1]`** |
| \|Δ\| (magnitud) | +0,20 … +0,39 | +0,22 … +0,43 | `[REPO]` **`[v1]`** |
| **f = ⟨O⟩ruidoso/⟨O⟩exacto** | **+0,74 … +0,83** | **+0,75 … +0,84** | `[REPO]` **`[v1]`** |

**La causa es aritmética, no estadística:**

$$\Delta = (1 - f)\cdot\langle O \rangle_{\text{exacto}}$$

Δ es el producto de **un factor aprendible** —cuánta señal destruye el ruido, que es física
del hardware y está en el circuito y la calibración— por **uno que no lo es**: cuánta señal
había, que depende del algoritmo y es justo la incógnita para la que haría falta un ordenador
cuántico.

**La excepción confirma la explicación:** `std_Z` es el único observable cuyo Δ tiene signo
sistemático (positivo el 99,9 % de las veces), y es el único con R² positivo sobre Δ.

### La solución, aprobada por el director

Predecir *f* y reconstruir Δ con el valor **medido**:

$$\hat\Delta = \langle O \rangle_{\text{ruidoso}}\cdot\frac{1 - \hat f}{\hat f}$$

**No rompe el paradigma pre-ejecución** — y este es el punto que hay que defender ante el
tribunal: la **entrada del modelo no cambia**, sigue siendo solo circuito y calibración. El
valor medido entra únicamente en la aritmética final de la corrección, exactamente donde ya
entraba en `⟨O⟩mitigado = ⟨O⟩ruidoso − Δ`. QEMFormer, en cambio, necesita el valor ruidoso
**como entrada del modelo**: la diferencia sigue siendo real.

**Ventaja adicional:** el caso degenerado se resuelve solo. Si el valor medido es ≈ 0,
entonces Δ̂ ≈ 0 — que es la respuesta correcta cuando no hay señal que corregir.

### El límite honesto `[v1]`

En test **solo transfiere `paridad`** (R² 0,62, −37 % de MAE). En los otros cuatro el R² se
hunde en negativo pese al 0,8 de validación.

**No es un fracaso: es el resultado central.** El dataset se diseñó para medir exactamente
esto, y deja a la comparativa una pregunta real — **¿transfiere el GEM, que ve la estructura
del grafo, donde la agregación no lo hace?**

---

## 5. Hallazgos de la EDA `[REPO]` **`[v1]` — rehacer**

1. Δ ocupa **menos del 17 %** de su rango físico → problema de precisión, no de magnitud.
2. Colas muy pesadas: **curtosis hasta 48** → el MAE lo dominan pocas muestras.
3. El ruido **no siempre encoge** el observable: falla hasta el **15 %** de las veces, y
   siempre donde el valor exacto es diminuto.
4. Entre el **22 % y el 37 %** de las muestras **no tienen señal que perder** y aportan menos
   del 8 % del target.
5. **Estructura aprendible y fuerte:** el factor de supervivencia correlaciona **−0,92**
   (Spearman) con el tamaño del circuito, de forma monótona pero **no lineal** → logaritmos.
6. **La telemetría del hardware NO predice**: 13 columnas, |r| medio **0,054**.
7. **La calidad de puerta se desvanece al fijar el tamaño**: 0,344 → **0,035**. Alcanza al
   score de **mapomatic** (−0,341 → −0,034). ⚠️ **No es una refutación de Nation & Treinish**:
   ellos comparan layouts del *mismo* circuito, donde el tamaño es constante por construcción.
8. **Colinealidad extrema**: un bloque de 8 features es «el tamaño» repetido, |r| hasta 0,999
   → justifica Ridge sobre mínimos cuadrados.
9. **`day` cae fuera del rango de train el 100 % del tiempo** → excluirla de los tabulares.
   Random Forest, además, **no puede extrapolar**.
10. **Label shift en `std_Z`**: la media de train es **3,2× peor** que no mitigar.

### Dos trampas metodológicas detectadas — van al capítulo 7

* **El eje TIEMPO está confundido con el eje TIPO.** Sobre el dataset completo, la
  correlación de |Δ| con el día es −0,26/−0,39 y parece drift fuerte; **dentro de `train_val`
  cae a −0,03/−0,08**. Casi todo era el eje tipo disfrazado.
* **Soporte fino disfrazado de tendencia.** La mediana de daño relativo por número de qubits
  parecía caer a partir de 10 qubits; eran 73, 3 y 2 muestras. **Publicar siempre el `n`.**

### ⚠️ Corrección del v2: los observables ya no son todos independientes

Con los 5 del v1 la correlación máxima entre dos Δ era 0,19. Con los **8** del v2 aparece un
bloque muy correlado `[REPO]` `[v2]`:

Matriz medida sobre **8.000 muestras del v2**, con el signo (importa, ver abajo):

| pareja | r | lectura |
|---|---|---|
| `std_X` – `std_Y` | **+0,840** | ┐ |
| `std_Z` – `std_Y` | **+0,786** | ├ el bloque de **dispersiones**: miden lo mismo en tres bases |
| `std_Z` – `std_X` | **+0,777** | ┘ |
| `mean_X` – `mean_Y` | **−0,552** | ⚠️ **anticorreladas**, no redundantes |
| `mean_X` – `std_X` | **−0,484** | ⚠️ ídem |

🔴 **Cuidado con el signo — cambia el argumento.** «Redundante» significa *miden lo mismo,
sobra uno*. **Anticorrelado significa que llevan información opuesta**, y eso es un argumento
**a favor** de conservar las dos, no en contra. Dos de las cinco parejas son negativas.

Solo **3 de las 28 parejas** llegan a 0,6. Hay **dos bloques** con estructura, no uno.

**No escribir en la memoria «los observables son independientes».** Decir cuáles: las tres
dispersiones son casi la misma magnitud en tres bases; `mean_X` y `mean_Y` están
anticorreladas. La justificación de los ocho es de **simetría de diseño** —no dejar ninguna
elección arbitraria sin explicar— no de independencia estadística.

---

## 6. Referencias clave y qué aporta cada una `[EXTERNO]`

| Referencia | Para qué se cita | Estado |
|---|---|---|
| **GTraQEM** — Bao et al., ICLR 2025 | La arquitectura base: Graph Transformer sin paso de mensajes + nodo virtual QCR | ✅ revisado |
| **Liao et al.**, Nature Mach. Intell. 2024 | Referencia central de ML-QEM; **Random Forest como mejor baseline** | ✅ revisado |
| **QEMFormer** — Bao et al., ICML 2025 | El techo de rendimiento a superar; **y el contraste**: necesita el valor ruidoso como entrada | ✅ revisado |
| **mapomatic** — Nation & Treinish, PRX Quantum 2023 | El pre-ejecución **heurístico** de IBM; nuestro `log_fidelidad_total` es su score | ✅ revisado |
| **Q-CTRL** — Hartnett et al., Quantum 2024 | ML pre-ejecución que **rankea**, no corrige | ✅ revisado |
| **Hirasaki et al.**, Appl. Phys. Lett. 2023 | Evidencia empírica del drift **escalonado**; justifica el eje temporal | ✅ revisado |
| **Anchor** — Huo et al., SIGMETRICS 2026 | Variabilidad operacional; complementa a Hirasaki | ✅ revisado |
| **Liu et al.**, Front. Phys. 2026 | GNN sobre el DAG con vector de nodo comparable (31 dims vs nuestras 25) | ✅ revisado |
| **Q-Cluster** — Patil et al., IEEE QCE 2025 | Contraste de paradigma: QEM **no supervisado** | ✅ revisado |
| **Liao et al.**, npj QI 2025 | Mitigación **sin ground truth**; va en limitaciones | ✅ revisado |
| **Placidi et al.** (Quantinuum), arXiv 2026 | Comparativa sistemática de arquitecturas DL | ⚠️ **preprint** |

**Diferenciadores del TFM frente al SOTA** — el argumento del capítulo 4:

1. **Opera pre-ejecución**: la entrada es solo circuito + telemetría, nunca el resultado.
2. **No codifica la identidad del qubit** → generaliza a cualquier número de qubits, que es
   la crítica que se le hace a QEMFormer.
3. **Modela el drift temporal** explícitamente, con calibración real de 42 días.
4. **Evalúa QFT sistemáticamente**, algo que ningún trabajo de ML-QEM hace.
