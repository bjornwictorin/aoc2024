#! /usr/bin/env python3


from typing import Set


class LogicGate:
    def __init__(self, gate_type, input0, input1, output):
        self.gate_type = gate_type
        self.input0 = input0
        self.input1 = input1
        self.output = output
    
    def __repr__(self):
        return f"({self.gate_type}, {self.input0}, {self.input1}, {self.output})"


def parse_input(file_name):
    data = open(file_name, "r")
    initial_wires = {}
    gates: Set[LogicGate] = set()

    parse_wires = True
    for line in data:
        if line == "\n":
            parse_wires = False
        elif parse_wires:
            name, value = line.rstrip().split(": ")
            initial_wires[name] = int(value)
        else:
            input0, gate_type, input1, _, output = line.rstrip().split(" ")
            gates.add(LogicGate(gate_type, input0, input1, output))

    return initial_wires, gates



def main():
    wire_values, gates = parse_input("input.txt")
    # print(wire_values)
    # print(gates)

    while gates:
        next_gates = set()
        for gate in gates:
            if gate.input0 in wire_values and gate.input1 in wire_values:
                if gate.gate_type == "AND":
                    wire_values[gate.output] = wire_values[gate.input0] & wire_values[gate.input1]
                elif gate.gate_type == "OR":
                    wire_values[gate.output] = wire_values[gate.input0] | wire_values[gate.input1]
                elif gate.gate_type == "XOR":
                    wire_values[gate.output] = wire_values[gate.input0] ^ wire_values[gate.input1]
                else:
                    assert False, f"invalid gate type: {gate.gate_type}"
            else:
                next_gates.add(gate)
        gates = next_gates
    
    # print(wire_values)
    
    z_bits = []
    for wire, value in wire_values.items():
        if wire.startswith("z"):
            z_bits.append((wire, value))
    z_bits.sort(reverse=True)
    # print(z_bits)
    z_value = 0
    for _, z_bit in z_bits:
        z_value = 2 * z_value + z_bit
    print(z_value)


if __name__ == "__main__":
    main()
