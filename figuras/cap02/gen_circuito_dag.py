"""Genera las dos figuras del apartado 2.1.5: un circuito y su DAG.

Salida:
    figuras/cap02/dag_circuito.pdf   el circuito, dibujado con Qiskit
    figuras/cap02/dag_grafo.pdf      el mismo circuito como grafo acíclico dirigido

El grafo lo dibuja `qiskit.visualization.dag_drawer`, que usa graphviz y colorea
por sí solo los tres tipos de nodo: verde las entradas, azul las operaciones y
rojo las salidas. Es el mismo aspecto que tiene la representación interna de
Qiskit, así que la figura no es una ilustración inventada sino lo que el
transpilador manipula de verdad.

Ejecutar desde la raíz del repositorio LaTeX:
    python figuras/cap02/gen_circuito_dag.py
"""

from pathlib import Path

from qiskit import QuantumCircuit, transpile
from qiskit.converters import circuit_to_dag
from qiskit.visualization import dag_drawer

SALIDA = Path(__file__).parent
BASE_NATIVA = ["cz", "id", "rz", "sx", "x"]  # IBM Heron, igual que en src/config.py


def construye_circuito() -> QuantumCircuit:
    """Un circuito ANCHO y POCO PROFUNDO, elegido por la forma del grafo.

    La primera versión usaba 3 qubits y 4 puertas en cascada: correcto, pero el DAG
    salía como una columna altísima y estrecha, imposible de maquetar junto al
    circuito. Con varios qubits en paralelo y una sola puerta de dos qubits, el grafo
    queda apaisado —una rama por qubit— y además se ve de un vistazo lo que importa:
    las ramas son independientes hasta que la `cz` las une.
    """
    qc = QuantumCircuit(5)
    for q in range(5):
        qc.rz(0.4 + 0.1 * q, q)
        qc.sx(q)
    qc.cz(0, 3)
    return qc


def main() -> None:
    qc = construye_circuito()

    # El circuito ya se escribe en la base nativa {rz, sx, cz}. Se transpila igualmente
    # para dejar constancia de que es lo que el chip ejecuta, pero sin que el paso añada
    # puertas: con una H, el transpilador la descompone en rz-sx-rz y el grafo se
    # alarga tanto que deja de caber al lado del circuito.
    qc_nativo = transpile(qc, basis_gates=BASE_NATIVA, optimization_level=1, seed_transpiler=42)

    qc_nativo.draw(
        output="mpl",
        filename=str(SALIDA / "dag_circuito.pdf"),
        fold=-1,          # sin partir el circuito en varias filas
        idle_wires=False,
    )

    dag_drawer(circuit_to_dag(qc_nativo), filename=str(SALIDA / "dag_grafo.pdf"))

    print(f"{qc_nativo.num_qubits} qubits · {len(qc_nativo.data)} puertas · "
          f"profundidad {qc_nativo.depth()}")


if __name__ == "__main__":
    main()
