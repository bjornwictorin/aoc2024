#!/usr/bin/env python3

def parse_input():
    input_data = open("input.txt", "r")
    equations = []
    for line in input_data:
        lhs, rhs = line.split(":")
        lhs = int(lhs)
        rhs = rhs.strip().split(" ")
        rhs = [int(ii) for ii in rhs]
        equations.append([lhs, rhs])

    return equations


def merge_nodes(values):
    assert len(values) >= 2
    if len(values) == 2:
        return [values[0] + values[1], values[0] * values[1]]
    return merge_nodes([values[0] + values[1]] + values[2:]) + merge_nodes([values[0] * values[1]] + values[2:])

def main():
    equations = parse_input()
    # lhs = left hand side
    true_lhs = []
    for lhs, rhs in equations:
        potential_solutions = merge_nodes(rhs)
        # print(potential_solutions)
        if lhs in potential_solutions:
            true_lhs.append(lhs)

    
    print(sum(true_lhs))

if __name__ == "__main__":
    main()
