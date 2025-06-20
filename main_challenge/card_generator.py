import numpy as np
import random
from qiskit import QuantumCircuit
import parameters as param
import math
from typing import NamedTuple, Any


class Card(NamedTuple):
    type: str
    data: Any

def generate_card():
    card_type = random.choices(
        ["State", "Operator", "Measurement"], 
        [param.state_prob, param.operation_prob, param.measurement_prob]
    )[0]
    if card_type == "State":
        data = generate_state()

    elif card_type == "Measurement":
        data = generate_measurement()

    else:
        data = generate_operator()

    return Card(type=card_type, data=data)
        


def generate_operator():
    card = ["I" for _ in range(param.num_qubits)]

    operator_type = random.choices(
        ['one_single_qubit', "two_single_qubit", "two_qubit"], [param.one_single_qubit_prob, param.two_single_qubit_prob, param.two_qubit_prob])[0]
    
    if operator_type == "one_single_qubit":
        index = random.sample(range(param.num_qubits), 1)[0]
        operation = random.choices(list(param.gate_prob["single_qubit"].keys()),
                                  list(param.gate_prob["single_qubit"].values()))[0]
        card[index] = operation

    elif operator_type == "two_single_qubit":
        index = random.sample(range(param.num_qubits), 2)
        operation = random.choices(list(param.gate_prob["single_qubit"].keys()),
                                  list(param.gate_prob["single_qubit"].values()), k = 2)

        for i, op in zip(index, operation):
            card[i] = op

    else:
        index = random.sample(range(param.num_qubits), 2)
        operation = random.choices(list(param.gate_prob["two_qubit"].keys()),
                                  list(param.gate_prob["two_qubit"].values()))[0]
        if operation == "CNOT":
            card[index[0]] = "C"
            card[index[1]] = "X"
        
        elif operation == "SWAP":
            card[index[0]] = "SWAP"
            card[index[1]] = "SWAP"

    return card

def generate_state() -> int:
    return random.randint(0, 2**param.num_qubits - 1)

def generate_measurement():
    return random.randint(0, param.num_qubits - 1)
