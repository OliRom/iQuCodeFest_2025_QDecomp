num_qubits = 3  # Number of qubits in the quantum circuit

num_qubits = 3

state_prob = 0.35  # Probability to have the qubit in the state |0>

measurement_prob = 0.1  # Probability to have a measurement operation

operation_prob = 1 - state_prob - measurement_prob  # Probability to have an operation


single_qubit_prob = 0.75

two_qubit_prob = 1 - single_qubit_prob



one_single_qubit_prob = single_qubit_prob * 0.70

two_single_qubit_prob = single_qubit_prob * 0.30

gate_prob = {
    "single_qubit": {
        "H": 0.3,
        "X": 0.3,
        "Z": 0.2,
        "S": 0.2
    },
    "two_qubit": {
        "CNOT": 0.5,
        "SWAP": 0.5
    }
}



