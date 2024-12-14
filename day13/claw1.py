#!/usr/bin/env python3

import re

def parse_input(input_data):
    input_data = open(input_data, "r")
    machines = []
    for line_number, line in enumerate(input_data):
        if line_number % 4 == 0:
            a_numbers = re.findall(r"Button A: X\+(\d+), Y\+(\d+)", line)
        elif line_number % 4 == 1:
            b_numbers = re.findall(r"Button B: X\+(\d+), Y\+(\d+)", line)
        elif line_number % 4 == 2:
            prize_numbers = re.findall(r"Prize: X=(\d+), Y=(\d+)", line)
        elif line_number % 4 == 3:
            assert line == "\n"
            machine = a_numbers[0] + b_numbers[0] + prize_numbers[0]
            machine = tuple(int(ii) for ii in machine)
            machines.append(machine)
    # add the last machine
    machine = a_numbers[0] + b_numbers[0] + prize_numbers[0]
    machine = tuple(int(ii) for ii in machine)
    machines.append(machine)
    return machines


def calc_min_tokens(machine):
    """Return smallest number of tokens required to reach prize.
    Return zero if prize is not reachable."""
    a_cost = 3 # button a costs 3 tokens
    b_cost = 1 # button b costs 1 token
    a_x, a_y, b_x, b_y, prize_x, prize_y = machine
    used_tokens_at_prize = []

    for num_a in range(101):
        for num_b in range(101):
            if num_a * a_x + num_b * b_x == prize_x and num_a * a_y + num_b * b_y == prize_y:
                used_tokens = a_cost * num_a + b_cost * num_b
                used_tokens_at_prize.append(used_tokens)

    assert len(used_tokens_at_prize) <= 1

    return min(used_tokens_at_prize) if used_tokens_at_prize else 0


def main():
    machines = parse_input("input.txt")
    tokens = []

    for machine in machines:
        # print(machine)
        machine_tokens = calc_min_tokens(machine)
        tokens.append(machine_tokens)

    print(sum(tokens))

if __name__ == "__main__":
    main()
