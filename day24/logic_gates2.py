#! /usr/bin/env python3


from abc import get_cache_token
from typing import Set
from copy import copy


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


def calc_logic(wire_values_init, gates):
    wire_values = copy(wire_values_init)
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
    
    z_bits = []
    for wire, value in wire_values.items():
        if wire.startswith("z"):
            z_bits.append((wire, value))
    z_bits.sort(reverse=True)
    z_value = 0
    for _, z_bit in z_bits:
        z_value = 2 * z_value + z_bit
    
    return z_value


BIT_WIDTH = 45 # add two 45 bit numbers


def sweep_values(gates):
    print("sweeping test values")
    # create test vectors
    # start with zero
    wire_values_zero = {}
    for bit_index in range(BIT_WIDTH):
        wire_values_zero[f"x{bit_index:02}"] = 0
        wire_values_zero[f"y{bit_index:02}"] = 0
    
    result_zero_plus_zero = calc_logic(wire_values_zero, gates)
    print(f"0+0: {result_zero_plus_zero}")

    for bit_index in range(BIT_WIDTH):
        wire_values_test = copy(wire_values_zero)
        wire_values_test[f"x{bit_index:02}"] = 1
        res10 = calc_logic(wire_values_test, gates)
        wire_values_test[f"y{bit_index:02}"] = 1
        res11 = calc_logic(wire_values_test, gates)
        wire_values_test[f"x{bit_index:02}"] = 0
        res01 = calc_logic(wire_values_test, gates)
        print(f"bit_index: {bit_index}")
        print(f"res10 = {res10}")
        print(f"res01 = {res01}")
        print(f"res11 = {res11}")
        one_shifted = 1 << bit_index
        if res10 != one_shifted or res01 != one_shifted or res11 != one_shifted + one_shifted:
            break


def switch_gate_outputs(gates: Set[LogicGate], output_a, output_b):
    print(f"switching {output_a} <-> {output_b}")
    gate_a = None
    gate_b = None
    for gate in gates:
        if gate.output == output_a:
            gate_a = gate
        if gate.output == output_b:
            gate_b = gate
    assert gate_a != None
    assert gate_b != None
    print(gate_a)
    print(gate_b)
    gate_a.output = output_b
    gate_b.output = output_a


def main():
    _, gates = parse_input("input.txt")
    sweep_values(gates)


# Full adders

# First fail at bit index 8
# mjm XOR gvw -> z08
# x08 XOR y08 -> qjb // should be written to gvw

# carry from bit index 7
# x07 XOR y07 -> stm
# stm AND gdp -> qgv
# qgv OR dsf -> mjm // carry out from index 7
# y07 AND x07 -> dsf

# swith gvw and qjb
    switch_gate_outputs(gates, "gvw", "qjb")
    sweep_values(gates)

# Next fail at bit index 14
# tpv XOR drk -> z14
# y14 XOR x14 -> drk

# carry from index 13
# x13 AND y13 -> rsq
# rsq OR cfk -> tpv // carry out from index 13
# hcg AND mnv -> cfk
# y13 XOR x13 -> mnv

# y15 AND x15 -> z15
# y15 XOR x15 -> rgt
# fbv XOR rgt -> jgc

# switch z15 and jgc:
    switch_gate_outputs(gates, "z15", "jgc")
    sweep_values(gates)

# Next fail at index 21
# hwm AND tdc -> z22
# y22 XOR x22 -> tdc
# x22 AND y22 -> snh
# tdc XOR hwm -> drg

# switch z22 and drg
    switch_gate_outputs(gates, "z22", "drg")
    sweep_values(gates)

# Next fail at index 34
# qrg OR ppf -> z35
# y35 AND x35 -> ppf
# y35 XOR x35 -> vcs
# vcs XOR dtj -> jbp

# switch z35 and jbp
    switch_gate_outputs(gates, "z35", "jbp")
    sweep_values(gates)

    # swapped gates:
    swapped_gates = ["gvw", "qjb", "z15", "jgc", "z22", "drg", "z35", "jbp"]
    swapped_gates.sort()
    print(",".join(swapped_gates))

if __name__ == "__main__":
    main()
