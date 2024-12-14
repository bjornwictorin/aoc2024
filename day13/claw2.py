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
    offset = 10000000000000
    prize_x += offset
    prize_y += offset

    # quotient = dividend / divisor
    num_a_dividend = (b_y * prize_x - b_x * prize_y)
    num_a_divisor = (a_x * b_y - a_y * b_x)

    num_b_dividend = (a_y * prize_x - a_x * prize_y)
    num_b_divisor = (b_x * a_y - b_y * a_x)

    if num_a_dividend % num_a_divisor == 0 and num_b_dividend % num_b_divisor == 0:
        num_a = num_a_dividend // num_a_divisor
        num_b = num_b_dividend // num_b_divisor
        return num_a * a_cost + num_b * b_cost
    return 0


def main():
    machines = parse_input("input.txt")
    tokens = []

    for machine in machines:
        # print(machine)
        machine_tokens = calc_min_tokens(machine)
        tokens.append(machine_tokens)

    # print(tokens)
    print(sum(tokens))

if __name__ == "__main__":
    main()
