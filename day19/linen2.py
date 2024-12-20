#! /usr/bin/env python3

from functools import cache


def parse_input(input_file):
    input_data = open(input_file, "r")
    avail_patterns = []
    wanted_patterns = []
    for line_number, line in enumerate(input_data):
        if line_number == 0:
            avail_patterns = line.rstrip().split(", ")
        elif line_number >= 2:
            wanted_patterns.append(line.rstrip())
    return avail_patterns, wanted_patterns


@cache
def calc_num_possible_pattern_dfs(wanted_pattern: str, start_index: int, avail_patterns: tuple[str]):
    num_combinations = 0
    for avail_pattern in avail_patterns:
        if wanted_pattern[start_index:] == avail_pattern:
            num_combinations += 1
        elif wanted_pattern[start_index:].startswith(avail_pattern):
            new_start_index = start_index + len(avail_pattern)
            num_combinations += calc_num_possible_pattern_dfs(wanted_pattern, new_start_index, avail_patterns)
    return num_combinations


def main():
    avail_patterns, wanted_patterns = parse_input("input.txt")
    num_comb_list = []
    for wanted_pattern in wanted_patterns:
        print(wanted_pattern)
        useful_patterns = tuple([x for x in avail_patterns if x in wanted_pattern])
        num_comb = calc_num_possible_pattern_dfs(wanted_pattern, 0, useful_patterns)
        num_comb_list.append(num_comb)
    print(sum(num_comb_list))


if __name__ == "__main__":
    main()
