#! /usr/bin/env python3


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


def is_possible_pattern_bfs(wanted_pattern: str, avail_patterns: list[str]):
    current_match_lengths = [0]
    prev_matched_lengths = {0}
    while current_match_lengths:
        next_match_lengths = []
        for match_len in current_match_lengths:
            for avail_pattern in avail_patterns:
                if wanted_pattern[match_len:match_len + len(avail_pattern)] == avail_pattern:
                    new_match_len = match_len + len(avail_pattern)
                    if new_match_len == len(wanted_pattern):
                        return True
                    if new_match_len not in prev_matched_lengths:
                        next_match_lengths.append(new_match_len)
                        prev_matched_lengths.add(new_match_len)
        current_match_lengths = next_match_lengths

    return False


def main():
    avail_patterns, wanted_patterns = parse_input("input.txt")
    avail_patterns.sort(key=len)
    possible_patterns = []
    for wanted_pattern in wanted_patterns:
        # print(wanted_pattern)
        if is_possible_pattern_bfs(wanted_pattern, avail_patterns):
            possible_patterns.append(wanted_pattern)
            # print("possible")
    print(len(possible_patterns))


if __name__ == "__main__":
    main()
