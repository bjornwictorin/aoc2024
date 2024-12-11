#!/usr/bin/env python3

from math import log10

def parse_input(input_data):
    input_data = open(input_data, "r")
    stones = []
    for line in input_data:
        stones.extend(line.rstrip().split())
    stones = [int(x) for x in stones]
    return stones


def calc_num_stones(value, iterations_left):
    if iterations_left == 0:
        return 1
    if value == 0:
        return calc_num_stones(1, iterations_left - 1)
    elif int(log10(value)) % 2 == 1:
        # even number of digits
        divider = (10**int((log10(value) + 1)//2))
        left_half = value // divider
        right_half = value % divider
        return calc_num_stones(left_half, iterations_left - 1) + calc_num_stones(right_half, iterations_left - 1)
    else:
        return calc_num_stones(value * 2024, iterations_left - 1)


def main():
    stones = parse_input("input.txt")
    print(stones)
    num_stones = 0
    for stone_value in stones:
        num_stones += calc_num_stones(stone_value, 25)

    print(num_stones)

if __name__ == "__main__":
    main()
