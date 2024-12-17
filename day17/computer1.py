#!/usr/bin/env python3

def parse_input(input_data):
    input_data = open(input_data, "r")
    for line in input_data:
        if line.startswith("Register A:"):
            reg_a = int(line.split(": ")[1])
        elif line.startswith("Register B:"):
            reg_b = int(line.split(": ")[1])
        elif line.startswith("Register C:"):
            reg_c = int(line.split(": ")[1])
        elif line.startswith("Program"):
            program_str = line.rstrip().split(": ")[1]
            program = [int(instr) for instr in program_str.split(",")]

    return reg_a, reg_b, reg_c, program


def get_combo(operand, reg_a, reg_b, reg_c):
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return reg_a
    elif operand == 5:
        return reg_b
    elif operand == 6:
        return reg_c
    else:
        assert False, f"invalid combo operand: {operand}"



def exec_instr(instr, operand, reg_a, reg_b, reg_c, pc, output):
    if instr == 0: # adv
        combo_op = get_combo(operand, reg_a, reg_b, reg_c)
        reg_a = reg_a // (2**combo_op)
        pc += 2
    elif instr == 1: # bxl
        reg_b = reg_b ^ operand
        pc += 2
    elif instr == 2: # bst
        reg_b = get_combo(operand, reg_a, reg_b, reg_c) & 7
        pc += 2
    elif instr == 3: # jnz
        pc = pc + 2 if reg_a == 0 else operand
    elif instr == 4: # bxc
        reg_b = reg_b ^ reg_c
        pc += 2
    elif instr == 5: # out
        output.append(str(get_combo(operand, reg_a, reg_b, reg_c) & 7))
        pc += 2
    elif instr == 6: # bdv
        combo_op = get_combo(operand, reg_a, reg_b, reg_c)
        reg_b = reg_a // (2**combo_op)
        pc += 2
    elif instr == 7: # cdv
        combo_op = get_combo(operand, reg_a, reg_b, reg_c)
        reg_c = reg_a // (2**combo_op)
        pc += 2
    else:
        assert False, f"invalid instruction: {instr}"

    return reg_a, reg_b, reg_c, pc


def main():
    reg_a, reg_b, reg_c, program = parse_input("input.txt")
    # print(reg_a)
    # print(reg_b)
    # print(reg_c)
    # print(program)
    output = []
    pc = 0 # instruction pointer

    while pc < len(program):
        assert pc % 2 == 0
        instr = program[pc]
        operand = program[pc + 1]
        reg_a, reg_b, reg_c, pc = exec_instr(instr, operand, reg_a, reg_b, reg_c, pc, output)

    print(",".join(output))

if __name__ == "__main__":
    main()
