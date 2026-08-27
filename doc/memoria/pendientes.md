# Pendientes antes de cerrar la memoria

> Fichero **durable**. Lo que falta medir, lo que está bloqueado y las trampas concretas en
> las que **no** hay que volver a caer al rehacer las cifras.

---

## 1. 🔴 Bloqueante: las cifras de la EDA son del dataset v1

Los cuatro cuadernos de `notebooks/eda/`, `doc/plan_eda.md` y `doc/hallazgo_objetivo.md`
tienen números medidos sobre el **v1**, cuyas etiquetas de n ≥ 10 llevaban ruido estocástico.

**Las conclusiones no cambiarán** — los efectos son órdenes de magnitud mayores que el
σ ≈ 1,5×10⁻³ del bug — **pero los números concretos sí**.

⚠️ **No citar ninguna cifra `[v1]` en la memoria sin rehacerla.**

**Cuándo rehacerlas:** cuando lleguen las 369 muestras de n=15. Hacerlo antes obligaría a
repetirlo, porque las figuras del eje tamaño cambiarían.

---

## 2. 🔴 Contradicción entre documentos — resolver con UNA sola medida

`ESTADO_ACTUAL.md` §4.7 e `IDEA_GENERAL_TFM.md` §7 traen **dos tablas del observable óptimo
por tipo que no coinciden**. No es un error de tecleo: son dos ejecuciones distintas que ni
siquiera listan los mismos tipos.

| tipo | `ESTADO_ACTUAL.md` | `IDEA_GENERAL_TFM.md` |
|---|---|---|
| qft | 45,4× | 42,7× |
| hea | 3,3× | 3,0× |
| tfim | 1,3× | 1,4× |
| bv | 1,3× | 1,2× |
| ghz / qaoa | *no concluyente* (53 % / 75 %) | 1,4× / 1,4× |

Y hay una **tercera** medida, rápida, de ago-2026 sobre el v2: QFT **3,7×**. Se hizo con
`|Δ| medio`, que **no es el mismo estadístico** que el bootstrap de las otras dos.

### La regla

➡️ **Recalcular con el BOOTSTRAP con estabilidad, nunca con `|Δ| medio`.** Producir **una
sola tabla**, sobre el v2, y **borrar las dos antiguas de los dos ficheros**.

⚠️ Mezclar las tres en la memoria sería arrastrar números que no significan lo mismo.

### Y ojo con la interpretación

Al pasar de 5 a 8 observables **la ventaja del QFT se desploma**: de ~45× a ~3,7×, porque el
nuevo `mean_Y` le recoge señal. Varios "óptimos" pasan a ser empates técnicos (`random`
1,08×, `hea` 1,01×). **La conclusión se sostiene** —sigue habiendo un óptimo distinto por
tipo, y QFT y GHZ son diferencias reales— **pero el argumento hay que reformularlo**: ya no
es "un tipo necesita 45× más señal", sino "la elección de observable no es cosmética".

---

## 3. ⏳ Las 369 muestras de n=15

Se están generando en una VM de Google Cloud. **No se pueden generar en local**: con
`density_matrix` forzado, n=15 pide **17,2 GB por proceso** y la máquina de desarrollo tiene
11. No es lentitud, es imposibilidad.

**Qué desbloquean:**
* el eje OOD de **tamaño** completo (ahora al 76,8 %),
* los 2 tests que fallan por índices ausentes,
* el capítulo 10 de la memoria (y, en cascada, el 11 y el 12).

**Qué NO bloquean:** absolutamente nada de los capítulos 1–7 y 9. `train_val` está **completo
(16 000/16 000)** porque los n=15 son todos de test por diseño.

---

## 4. Decisión abierta: los grafos grandes del GEM

La atención de un Transformer es cuadrática y no cabe en el peor caso.

| Opción | Coste | Pega |
|---|---|---|
| **A. Truncar a ~2 000 nodos** ⭐ | afecta al **10,16 %**, coste ÷11,9, ~$3 | pierde información en los circuitos más difíciles |
| B. Sin truncar, A100 de 80 GB | ~15 h, ~$18 | más caro, pero ya asumible |
| C. Atención eficiente (Performer/Linformer) | lineal | aleja el diseño de GTraQEM, la referencia |

**Recomendación:** empezar por **A**, medir si el GEM falla *específicamente* en circuitos
grandes, y pasar a **B** solo si falla. Es reversible y el 90 % de los datos ni se entera.

---

## 5. Lo que falta implementar

| Fichero | Estado | Qué debe hacer |
|---|---|---|
| `src/dataset.py` | ❌ vacío | Preprocesado: normalizar (**solo con train**), podar las 3 dims muertas, envolver ángulos, logaritmos, excluir `day` |
| `src/baselines.py` | ❌ no existe | Ridge + Random Forest |
| `src/gem_model.py` | ❌ vacío | Graph Transformer sin paso de mensajes + nodo virtual QCR, salida de 8 |
| `src/train.py` | ⚠️ esqueleto | Bucle + MLflow, **protocolo idéntico** para los tres modelos |
| `src/utils.py` | ⚠️ esqueleto | Métricas desglosadas por eje OOD |

⚠️ **Cuestión de diseño abierta:** el preprocesado tabular y el de grafos **no son el mismo**.
Probablemente sean dos módulos, no uno.

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
