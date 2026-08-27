# El ruido en los ordenadores cuánticos

> Desarrollado en ago-2026 (antes era solo un enlace). Material de apoyo para el **capítulo 3**
> de la memoria. Lo medido sobre nuestro chip está en `memoria/materiales.md` §2.
>
> Lectura externa recomendada:
> [Qiskit Summer School 2021 — Lecture 3](https://github.com/Qiskit/platypus/blob/main/notebooks/summer-school/2021/resources/lecture-notes/Lecture3-slides.pdf)

---

## 1. Por qué hace falta la matriz de densidad

Un estado sin ruido se describe con un vector `|ψ⟩`. En cuanto hay ruido eso deja de valer:
el sistema ya no está en un estado concreto, sino en una **mezcla estadística** de varios.

$$\rho = \sum_i p_i \ket{\psi_i}\bra{\psi_i}$$

Dos consecuencias prácticas para este trabajo:

* El valor esperado pasa a calcularse como $\langle O \rangle = \mathrm{Tr}(\rho O)$.
* **El coste de memoria pasa de $2^n$ a $4^n$ amplitudes.** Para n=15 son **17,2 GB por
  proceso** — el motivo exacto de que esas muestras haya que generarlas en la nube.

## 2. Canales cuánticos: cómo se escribe "lo que el ruido le hace al estado"

Cualquier proceso físico sobre un estado se describe con un conjunto de operadores de Kraus:

$$\mathcal{E}(\rho) = \sum_k E_k \rho E_k^\dagger$$

Es la herramienta que permite tratar el ruido como algo **componible**: cada puerta aplica su
canal, y el efecto total se acumula a lo largo del circuito.

⚠️ **Y de aquí sale una sutileza que aparece medida en el proyecto:** el ruido **no conmuta**
con la unitaria. Dos descomposiciones distintas del mismo circuito —matemáticamente
equivalentes— acumulan decoherencia de forma diferente. Por eso, cuando el transpilador
reparte las rotaciones de otra manera, el valor **exacto** sale idéntico pero el **ruidoso**
cambia. No es un error de cálculo: es física real.

## 3. Las tres fuentes de error, y cuál domina

### Decoherencia — T1 y T2
El qubit no mantiene su estado indefinidamente. **T1** mide cuánto tarda en perder su energía
(relajarse a `|0⟩`); **T2**, cuánto tarda en perder la coherencia de fase.

Cota física: **T2 ≤ 2·T1**. ⚠️ En nuestros datos el 0,92 % de las medidas la viola — y **55 de
las 60 son solo dos qubits vecinos averiados**. La calibración de un qubit roto no es fiable.

Lo que importa no es T1 en absoluto, sino **cuánto dura el circuito comparado con T1**. De ahí
la familia de features `duracion_critica / T1_min`: cuántas "vidas T1" vive el estado.

⚠️ **Y la duración real no es la suma de las puertas**: las que actúan sobre qubits distintos
se ejecutan **a la vez**. Lo que cuenta es el **camino crítico del DAG**, que en nuestro
dataset es entre 2 y 3 veces menor que la suma.

### Error de puerta
Cada operación se implementa con pulsos electromagnéticos imperfectos. IBM publica el
`gate_error` medido de **cada puerta física, cada día**.

Dos cosas que solo se ven mirando los datos reales:

1. **La `rz` tiene error exactamente cero.** No es un hueco: en hardware IBM la `rz` es
   **virtual** — cambia la fase de referencia del pulso siguiente y no emite ningún pulso. Es
   gratis, y por eso el transpilador la usa sin límite.
2. **`id`, `sx` y `x` traen valores idénticos** (correlación 1,000000): IBM las deriva del
   mismo pulso calibrado. ⚠️ El `gate_error` **no distingue** una `sx` de una `x`.

### Error de lectura
Al medir, un `|0⟩` puede leerse como `1` y viceversa. **Es asimétrico**: P(0→1) ≠ P(1→0),
porque relajarse es más fácil que excitarse. El dataset guarda las dos probabilidades por
separado.

### ⚠️ Cuál domina — resultado medido, y no es el esperado

La intuición dice que la calidad del hardware que te toca determina cuánto error acumulas.
**Medido, no es así:** al comparar circuitos **del mismo tamaño**, la correlación entre la
calidad de las puertas y el error observado **se desvanece** (0,344 → 0,035).

Lo que predice el error es el **tamaño y la forma del circuito**. La telemetría del hardware
(13 variables: T1, T2, lectura) da una correlación media de **0,054**.

📌 Es un resultado importante para la memoria, y hay que contarlo **con su matiz**: no
significa que el hardware no importe, sino que **su variación entre regiones del chip es
pequeña comparada con la variación entre circuitos**.

## 4. Qué NO modelamos, y hay que declararlo

**Crosstalk.** Cuando se opera sobre un qubit, sus vecinos se perturban. Nuestro modelo usa
los tres canales canónicos de Qiskit Aer, que son **puramente locales**.

Esto tiene una consecuencia comprobada: se propuso añadir el **grado de conectividad** del
qubit como feature, con la idea de que un qubit con más vecinos sufre más crosstalk. Se midió
y la correlación fue **+0,025 (p = 0,62)** — cero.

**Por qué:** sin crosstalk en el modelo de ruido, **no existe camino causal** entre el grado
del qubit y la etiqueta. Añadirlo habría sido meter una dimensión muerta.

> 📌 **Lección metodológica:** que una variable *varíe* y *no esté capturada* no la hace útil.
> Hay que comprobar que tenga un camino causal hacia la etiqueta **en el sistema que
> realmente se está simulando**.

## 5. Por qué mitigar y no corregir

La **corrección** de errores (QEC) es la solución definitiva, pero necesita muchos qubits
físicos por cada qubit lógico — muy por encima de lo que hay hoy.

La **mitigación** (QEM) es la alternativa realista: no impide el error, lo **estima y lo
descuenta** del resultado. No necesita qubits extra, pero tampoco escala indefinidamente.

Este TFM se sitúa en la mitigación, y en una variante concreta: **estimar la degradación antes
de ejecutar**, mirando solo el circuito y la calibración.
