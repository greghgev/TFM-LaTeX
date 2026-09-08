# Pendientes antes de cerrar la memoria

> Fichero **durable**. Lo que falta medir, lo que está bloqueado y las trampas concretas en
> las que **no** hay que volver a caer al rehacer las cifras.

---

## 1. ✅ RESUELTO — la EDA está rehecha sobre el v2

Los nueve cuadernos de `notebooks/01_eda/` (`01a` a `01i`) están medidos sobre el **v2**, con
20 000 muestras y etiquetas exactas. Los cuatro cuadernos de la EDA v1 se **borraron** en
sep-2026 junto con sus módulos y figuras.

⚠️ **Siguen con cifras del v1**, y no se han rehecho: `doc/plan_eda.md` (marcado como obsoleto
en su cabecera) y `doc/hallazgo_objetivo.md`. **No citar `[v1]` sin comprobar.**

🔴 **Dos cifras del v1 que se han medido FALSAS en el v2** y que estaban circulando por varios
documentos:

* «la calidad de puerta se desvanece al fijar el tamaño, 0,344 → 0,035» → en el v2
  `gate_error_suma` pasa de **0,489 a 0,510**: no se desvanece.
* «42,7×» y «45,4×» para el QFT → la única citable es **3,69×** (bootstrap sobre el v2).

---

## 2. ✅ RESUELTO — el observable óptimo por tipo

Había **dos tablas contradictorias** (`ESTADO_ACTUAL.md` §4.7 con 45,4× para el QFT e
`IDEA_GENERAL_TFM.md` §7 con 42,7×) más una tercera medida rápida con otro estadístico.

✅ **Zanjado en ago-2026 con bootstrap (2 000 remuestreos) sobre el v2.** Las dos antiguas
están borradas. **Ésta es la única citable:**

| tipo | n | óptimo | ventaja sobre el 2º | estabilidad |
|---|---|---|---|---|
| qft | 433 | `mean_X` | **3,69×** | 100 % |
| ghz | 502 | `paridad` | **2,49×** | 100 % |
| qaoa | 481 | `mean_X` | 1,36× | 100 % |
| tfim | 454 | `corr_vecinos` | 1,33× | 100 % |
| bv | 450 | `mean_Z` | 1,28× | 100 % |
| random | 5198 | `std_Z` | 1,06× | 100 % |
| hea | 482 | `std_X` | 1,01× | 67 % → *no concluyente* |

⚠️ **Cómo formular el argumento en la memoria.** Ya **no** es «un tipo necesita 45× más
señal», sino **«la elección de observable no es cosmética: seis de siete tipos tienen un óptimo
estadísticamente sólido, y hay cuatro óptimos distintos»**. Un target escalar único habría
penalizado a varios.

⚠️ **Y encaja con la retirada de las dispersiones:** los dos tipos cuyo óptimo cae en ese
bloque lo hacen por margen despreciable (1,06× y 1,01× no concluyente). Retirarlo **no deja a
ningún tipo sin óptimo propio**.

---

## 3. ✅ RESUELTO — las 369 muestras de n=15 ya están

Llegaron. El dataset v2 está **completo**: 20 000 muestras, y `n_qubits = 15` tiene sus **369**
circuitos, todos en `test` por diseño. El eje OOD de tamaño está cerrado.

<details><summary>Contexto de por qué costaron (se conserva para la memoria)</summary>

### Lo que decía este apartado

Se están generando en una VM de Google Cloud. **No se pueden generar en local**: con
`density_matrix` forzado, n=15 pide **17,2 GB por proceso** y la máquina de desarrollo tiene
11. No es lentitud, es imposibilidad.

**Qué desbloquean:**
* el eje OOD de **tamaño** completo (ahora al 76,8 %),
* los 2 tests que fallan por índices ausentes,
* el capítulo 10 de la memoria (y, en cascada, el 11 y el 12).

**Qué NO bloquean:** absolutamente nada de los capítulos 1–7 y 9. `train_val` está **completo
(16 000/16 000)** porque los n=15 son todos de test por diseño.

</details>

---

## 4. ✅ CERRADO — los grafos grandes del GNN

Este apartado partía de un **Graph Transformer**, cuya atención es cuadrática. La arquitectura
cambió a un **MPNN con paso de mensajes** (31-ago-2026), y ahí la memoria es **lineal** en
nodos y aristas: el truncado a 2 000 nodos deja de hacer falta, y con él desaparece el sesgo
que castigaba a los circuitos profundos del entrenamiento.

⚠️ **Falta confirmarlo con un *dry run***: un lote con el grafo mayor (8 310 nodos), pase
forward y backward, y mirar `torch.cuda.max_memory_allocated()`. La cuenta a mano no incluye
los tensores intermedios ni los momentos de Adam.

<details><summary>La decisión original, cuando la arquitectura era un Transformer</summary>

La atención de un Transformer es cuadrática y no cabe en el peor caso.

| Opción | Coste | Pega |
|---|---|---|
| **A. Truncar a ~2 000 nodos** ⭐ | afecta al **10,16 %**, coste ÷11,9, ~$3 | pierde información en los circuitos más difíciles |
| B. Sin truncar, A100 de 80 GB | ~15 h, ~$18 | más caro, pero ya asumible |
| C. Atención eficiente (Performer/Linformer) | lineal | aleja el diseño de GTraQEM, la referencia |

**Recomendación:** empezar por **A**, medir si el modelo falla *específicamente* en circuitos
grandes, y pasar a **B** solo si falla. Es reversible y el 90 % de los datos ni se entera.

</details>

---

## 5. Lo que falta implementar

| Fichero | Estado | Qué hace |
|---|---|---|
| `src/preprocesado.py` | ✅ hecho | Preprocesado **tabular**: descarte de 20 columnas, `log1p` en 3, escalado ajustado **solo con `train`**, y guardado a `data/processed/tabular_v2/` |
| `src/baselines.py` | ✅ hecho | Ridge simple, Ridge múltiple y Random Forest, con rejilla contra `val` |
| `src/evaluacion.py` | ✅ hecho | Métricas desglosadas por los tres ejes OOD. **El mismo código para los tres modelos** |
| `src/dataset.py` | ⚠️ provisional | Carga de **grafos** para el GNN |
| `src/gnn_model.py` | ⚠️ provisional | 🔴 **MPNN CON paso de mensajes** + **nodo virtual BIDIRECCIONAL** con pesos propios, salida de **5**. Sin truncar. `SAGEConv` → `GATv2Conv` → `GINConv`, escalando |
| `src/train.py` | ⚠️ provisional | Bucle del GNN. Registro en **Weights & Biases**, no MLflow |
| `scripts/evaluate.py` | ❌ esqueleto | Cargar los artefactos de `models/` y llamar a `src/evaluacion.py` |

✅ **Resuelta la cuestión de diseño:** el preprocesado tabular y el de grafos son **dos módulos
distintos** (`src/preprocesado.py` y `src/dataset.py`). Comparten la partición y el umbral, no
el tratamiento.

⚠️ **Y una corrección:** aquí ponía «envolver ángulos». **Se decidió NO envolverlos**: son 12
circuitos de 13 344, el 0,09 %. Solo se menciona en limitaciones.

### Decisiones cerradas que condicionan lo que queda

* **Pérdida de Huber**, no MSE, y enmascarada.
* **Sin techo en `f`.** La única cota es `f_final = max(f̂, |r|)`, se aplica **al evaluar** y
  vive en `evaluacion.aplicar_cota`.
* **La métrica que decide es el R² sobre `f`**, no la mejora sobre el mitigado: el
  diferenciador del TFM es la pre-ejecución, y el mitigado necesita el valor ruidoso, que solo
  existe después de ejecutar.
* **Registro en W&B** (proyecto `tfm-quantum`), con semilla, commit de git y md5 del dataset.
* **El entrenamiento va en scripts, no en cuadernos.** Los cuadernos de `03_ridge_rf` y
  `04_gnn` solo cargan artefactos y evalúan.

---

## 6. Documentación del repositorio pendiente de actualizar

`doc/src_info.md` · `doc/notebooks_info.md` · `ROADMAP.md` · `README.md` · `GUIA_TUTOR.md` ·
`doc/dataset_info.md` · `doc/SoTA/comparative_analysis.md`

*(`doc/changes/*` se dejan como registro histórico, por decisión del usuario.)*

---

## 7. Referencias por verificar antes de citarlas

`doc/00_Justificaciones.md` citaba tres trabajos que **no están en la lista verificada** de
`CLAUDE.md`:

| Referencia | Estado |
|---|---|
| *Output Prediction of Quantum Circuits based on GNN* | ✅ verificado — Liu et al., Front. Phys. 2026 |
| *Scalable QEM with Physically Informed GNN* (2026) | ⚠️ **sin DOI verificado** |
| *QML-PipeGuard* (2026) | ⚠️ **sin DOI verificado** |

➡️ **Verificar DOI antes de meterlas en `bibliografia.bib`.** Una cita inventada en un TFM es
un problema serio, y es exactamente el tipo de error que un tribunal comprueba.

### Autores incompletos en la bibliografía

Cuatro entradas de `bibliografia.bib` llevan `and others` porque **no se inventaron nombres
de coautores**: `bao2025gtraqem`, `liu2026output`, `placidi2026deep`, `hartnett2024learning`.

APA exige la lista completa y BibTeX avisa en cada compilación. **Completarlos consultando el
paper antes de entregar.**

### Referencias fundacionales que faltan

Aún no están en el `.bib` porque no se ha verificado su DOI: NISQ (Preskill 2018), Qiskit y
Qiskit Aer, ZNE (Temme et al. / Li \& Benjamin), PEC (Endo et al.) y M3 (Nation et al.).
⚠️ **Verificar cada DOI, no copiarlos de memoria.**

⚠️ Recordatorio: hay tres trabajos **explícitamente excluidos** por no ser citables
(Wang/Zhengzhou, Stirbu, Al Farib).
