> ✅ **Este fichero NO está desactualizado** (nota añadida ago-2026): la física de los
> observables de Pauli no cambia. Cubre bien X, Y y Z sobre un qubit.
>
> ⚠️ **Pero está incompleto respecto al dataset actual**, que usa **ocho observables**
> agregados sobre todo el registro, no solo los de un qubit. La sección final los recoge.

---

# Observables en Computación Cuántica

En mecánica cuántica, un **observable** es cualquier magnitud física que puede medirse en un sistema cuántico. Matemáticamente, un observable se representa mediante una **matriz hermítica**.  
En computación cuántica, los observables más comunes son los **operadores de Pauli**.

---

## 🧮 Tipos de observables más comunes

### **1. Observable Pauli‑X**
Representa una inversión del estado del qubit (un “flip”).  
Su matriz es:

$$
X =
\begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix}
$$

Este observable distingue estados en la **base X**, es decir, los estados $|+\rangle$ y $|-\rangle$.

---

### **2. Observable Pauli‑Y**
Incluye una fase compleja y también rota el estado del qubit.

$$
Y =
\begin{pmatrix}
0 & -i \\
i & 0
\end{pmatrix}
$$

Se usa menos en computación cuántica básica, pero es fundamental en análisis de ruido y operaciones más avanzadas.

---

### **3. Observable Pauli‑Z (el importante aquí)**
Este es el observable más usado para medir qubits en computación cuántica.  
Su matriz es:

$$
Z =
\begin{pmatrix}
1 & 0 \\
0 & -1
\end{pmatrix}
$$

### ¿Qué mide exactamente el observable Z?

El operador **Z** distingue entre los estados computacionales:

- $|0\rangle$ → **eigenvalor +1**  
- $|1\rangle$ → **eigenvalor −1**

Es decir, cuando mides un qubit con el observable Z, estás preguntando:

> “¿Está el qubit más alineado con el estado $|0⟩$ o con el estado $|1⟩$?”

Por eso es el observable estándar en la mayoría de los sistemas cuánticos reales (IBM, Rigetti, IonQ, etc.), y también es clave en el análisis de **ruido**, porque muchos tipos de ruido afectan directamente a la probabilidad de obtener +1 o −1 en esta medición.

---

# 🧩 Qubits (visión breve)

Un **qubit** es la unidad básica de información cuántica.  
Puede estar en:

- $|0\rangle$
- $|1\rangle$
- o cualquier **superposición**:

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle
$$

con $|\alpha|^2 + |\beta|^2 = 1$.

Los qubits también pueden estar **entrelazados**, lo que permite correlaciones imposibles en sistemas clásicos.

---

# 🔀 La puerta X (NOT cuántico)

La puerta **X** es el equivalente cuántico del NOT clásico:  
- Convierte $|0\rangle$ en $|1\rangle$  
- Convierte $|1\rangle$ en $|0\rangle$

Su matriz es exactamente el observable Pauli‑X:

$$
X =
\begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix}
$$

### ¿Por qué aparece en análisis de ruido?

Porque muchas fuentes de ruido producen **bit‑flips**, que son errores que se modelan como la acción no deseada de la puerta X sobre el qubit.  
Ejemplo:

$$
|0\rangle \xrightarrow{\text{ruido}} |1\rangle
$$

Por eso, entender la puerta X y el observable Z es fundamental para estudiar **ruido de tipo bit‑flip** y **mediciones en la base computacional**.

---

## 🧠 Resumen rápido

- **Observables** → magnitudes medibles, representadas por matrices hermíticas.  
- **Pauli‑Z** → mide si el qubit está en $|0\rangle$ (+1) o $|1\rangle$ (−1).  
- **Pauli‑X** → flip del qubit; también es una puerta cuántica.  
- **Qubits** → estados en superposición y entrelazamiento.  
- **Puerta X** → NOT cuántico, matriz $\begin{pmatrix}0&1\\1&0\end{pmatrix}$.

---

Perfecto, Gregory.  
Aquí tienes **la ampliación sobre Pauli‑Z**, en **el mismo formato Markdown y estilo** que tus apuntes, para que puedas pegarlo directamente debajo de la sección correspondiente.

---

## 🔍 ¿Qué significan realmente los valores +1 y −1 en el observable Z?

Cuando hablamos del observable **Pauli‑Z**, decimos que sus *eigenvalores* son **+1** y **−1**.  
Esto no es un adorno matemático: es exactamente lo que devuelve una **medición física** del qubit en la base computacional.

### ✔️ ¿Qué es un eigenvalor en este contexto?

Un **eigenvalor** es el resultado que obtienes cuando mides un qubit que está en uno de los estados propios (eigenestados) del operador Z.

Los eigenestados del operador Z son:

- $|0\rangle$  
- $|1\rangle$

Y los eigenvalores asociados son:

- $Z|0\rangle = +1 \, |0\rangle$  
- $Z|1\rangle = -1 \, |1\rangle$

Esto significa:

- Si el qubit está en $|0\rangle$ y lo mides con Z → **obtienes +1**  
- Si el qubit está en $|1\rangle$ y lo mides con Z → **obtienes −1**

---

## 🎯 ¿Por qué +1 y −1? ¿Por qué no 0 y 1?

Porque en mecánica cuántica:

- Los observables se representan con **matrices hermíticas**  
- Sus resultados posibles son **eigenvalores reales**  
- En el caso de Pauli‑Z, esos valores son **+1 y −1**

Esto tiene una interpretación física:

- **+1** corresponde a “spin arriba” o alineado con el eje Z  
- **−1** corresponde a “spin abajo” o anti‑alineado con el eje Z  

En computación cuántica, esto se traduce directamente a:

- **+1 → estado $|0\rangle$**  
- **−1 → estado $|1\rangle$**

---

## 📌 ¿Qué pasa si el qubit está en superposición?

Si el estado es, por ejemplo:

$$
|\psi\rangle = \alpha |0\rangle + \beta |1\rangle
$$

Entonces la medición con Z **colapsa** el estado y devuelve:

- **+1** con probabilidad $|\alpha|^2$  
- **−1** con probabilidad $|\beta|^2$

Y después de medir:

- Si salió +1 → el qubit queda en $|0\rangle$  
- Si salió −1 → el qubit queda en $|1\rangle$

---

## 🧠 ¿Por qué es tan importante en análisis de ruido?

Porque muchos tipos de ruido afectan directamente a la probabilidad de obtener +1 o −1.

Ejemplos:

- **Bit‑flip noise**:  
  Cambia $|0\rangle$ ↔ $|1\rangle$, alterando la probabilidad de obtener +1 o −1.

- **Phase‑flip noise**:  
  Cambia el signo de la amplitud de $|1\rangle$, afectando cómo se comporta el qubit bajo Z.

- **Readout noise**:  
  El hardware puede reportar +1 cuando debería ser −1, o viceversa.

Por eso Pauli‑Z es el observable estándar para medir qubits en hardware real.

---

## 🧩 Resumen añadido para tus apuntes

- El observable Z tiene eigenvalores **+1** y **−1**.  
- Estos valores son los **resultados reales de la medición**.  
- $|0\rangle$ siempre da **+1**, $|1\rangle$ siempre da **−1**.  
- En superposición, la medición colapsa el estado y devuelve uno de esos dos valores con probabilidades $|\alpha|^2$ y $|\beta|^2$.  
- Es el observable más usado en hardware cuántico porque mide directamente el estado computacional del qubit.

---

---

# 🎯 Los ocho observables del dataset (añadido ago-2026)

Todo lo anterior describe observables sobre **un qubit**. El dataset del TFM no predice eso:
predice **ocho magnitudes agregadas sobre el registro entero**, que es lo que un usuario mide
de verdad al ejecutar un algoritmo.

| # | Observable | Qué mide | Por qué está |
|---|---|---|---|
| 1 | `mean_Z` | ⟨ΣZᵢ⟩/n — magnetización media | la magnitud global más usada; comparable entre tamaños |
| 2 | `mean_X` | ídem en la base X | captura errores de **fase**, invisibles en la base Z |
| 3 | `mean_Y` | ídem en la base Y | cierra las tres bases de Pauli |
| 4 | `std_Z` | dispersión de los ⟨Zᵢ⟩ | **heterogeneidad**: ¿sufren todos los qubits igual? |
| 5 | `std_X` | ídem en X | |
| 6 | `std_Y` | ídem en Y | |
| 7 | `paridad` | ⟨Z₀Z₁…Z_{n−1}⟩ | correlación global; **un solo fallo la rompe** |
| 8 | `corr_vecinos` | ⟨ΣZᵢZᵢ₊₁⟩/(n−1) | errores de dos qubits, que son los caros |

## Por qué ocho y no uno

Porque **un solo observable dejaría ciegos a varios tipos de circuito**. No es una cuestión de
preferencia: hay estados en los que un observable vale **cero por construcción física**.

* Un **GHZ** produce `|00…0⟩` y `|11…1⟩` al 50 %: la magnetización media **se cancela
  siempre**, valga lo que valga el ruido.
* Un **QFT** sobre `|0…0⟩` deja todos los ⟨Zᵢ⟩ a cero y **toda** su señal en `mean_X`.

Con un target escalar basado en Z, esos circuitos no tendrían nada que predecir. Sería una
elección arbitraria imposible de defender.

## Por qué hacen falta los valores por qubit

Una **desviación típica no se puede calcular a partir de una media**. Para obtener `std_Z`
hay que conocer los ⟨Zᵢ⟩ **individuales**, no su promedio.

Por eso el simulador evalúa **3n + 2** valores esperados —los ⟨Zᵢ⟩, ⟨Xᵢ⟩ y ⟨Yᵢ⟩ de cada
qubit, más la paridad y el correlador— y de ahí reduce a los ocho fijos. Cada muestra guarda
además `por_qubit [3, n]` con los valores individuales exactos.

**El tamaño fijo de la salida es innegociable:** si el objetivo creciera con el número de
qubits, no se podría entrenar una sola red para todos los tamaños.

## ⚠️ Un matiz medido que hay que declarar

Las tres dispersiones **no son independientes entre sí**:

```
std_X ↔ std_Y   +0,85       std_Z ↔ std_X   +0,77       std_Z ↔ std_Y   +0,80
```

Los cinco observables originales sí son casi ortogonales (|r| ≤ 0,19), pero el bloque `std_*`
mide en buena parte lo mismo en tres bases. **La justificación de los ocho es de simetría de
diseño —no dejar ninguna elección arbitraria sin explicar— no de independencia estadística.**
