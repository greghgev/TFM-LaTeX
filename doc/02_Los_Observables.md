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