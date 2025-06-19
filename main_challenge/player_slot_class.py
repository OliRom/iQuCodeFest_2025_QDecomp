from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import parameters as para
import matplotlib.pyplot as plt


class PlayerSlot:
    """
    Represents one player card slot in the QDutch game.
    """
    def __init__(self):
        """
        Initializes the PlayerSlot with a quantum circuit.
        """
        self.qc = QuantumCircuit(para.num_qubits, para.num_qubits)
    
    def apply_operator(self, operator: list[str]) -> None:
        """
        Applies a quantum operator to the player slot.

        Args:
            operator (list[str]): The quantum operator to apply.
        """
        # CNOT gate
        if "C" in operator:
            target = operator.index("X")
            control = operator.index("C")
            self.qc.cx(control, target)
            return
        
        # SWAP gate
        if "SWAP" in operator:
            qubit1 = operator.index("SWAP")
            qubit2 = operator[qubit1+1:].index("SWAP") + qubit1 + 1
            self.qc.cx(qubit1, qubit2)
            self.qc.cx(qubit2, qubit1)
            self.qc.cx(qubit1, qubit2)
            return
        
        # Single qubit gates
        for i, gate_name in enumerate(operator):
            if gate_name == "I":
                continue

            else:
                method = getattr(self.qc, gate_name.lower())
                method(i)

    def measure(self, nb) -> int:
        """
        Measures the state of one qubit of the player slot.
        
        Returns:
            int: The measured state of the player slot.
        """
        self.qc.measure(nb, nb)
        # To be able to retrieve the state and continue the game after the measurement
        self.qc.save_statevector()

        self.plot_circuit()

        simulator = AerSimulator(method="statevector")
        new_circuit = transpile(self.qc, simulator)
        job = simulator.run(new_circuit, shots=1)
        result = job.result()

        # Get the statevector and the partial measurement
        statevector = result.get_statevector(new_circuit)
        measured_bit = list(result.get_counts().keys())[0][-nb-1]

        print(statevector)

        # Reinitialize the circuit with the statevector AFTER the partial measurement to continue the game
        self.qc = QuantumCircuit(para.num_qubits, para.num_qubits)
        self.qc.initialize(statevector, range(para.num_qubits))

        return int(measured_bit)


    def measure_all(self) -> int:
        """
        Measures the state of the player slot (3 qubits).
        
        Returns:
            int: The measured state of the player slot.
        """
        self.qc.measure_all()
        
        # Simulate the circuit to get the measurement result
        simulator = AerSimulator()
        new_circuit = transpile(self.qc, simulator)
        job = simulator.run(new_circuit, shots=1)
        result = job.result()
        counts = result.get_counts()

        value = int(list(counts.keys())[0][:para.num_qubits], 2)

        # Reinitialize the circuit after the measurement to continue the game
        self.qc = QuantumCircuit(para.num_qubits, para.num_qubits)
        self.set_state(value)

        return value

    def set_state(self, state: int) -> None:
        """
        Sets the state of the player slot.
        
        Args:
            state (int): The new state of the player slot.
        """
        initial_state = [0] * 2**para.num_qubits
        initial_state[state] = 1

        self.qc.initialize(initial_state, range(para.num_qubits))

    def plot_circuit(self) -> None:
        """
        Plots the quantum circuit of the player slot.
        """
        self.qc.draw(output='mpl')
        plt.show()
