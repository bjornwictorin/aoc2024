#! /usr/bin/env python3

from functools import cache
from typing import List

NUM_DIRPADS = 4


def parse_input(filename):
    data = open(filename, "r")
    codes = []
    for line in data:
        codes.append(line.rstrip())
    return codes


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
def get_num_pad_pos(digit):
    if digit == "7":
        return (0, 0)
    elif digit == "8":
        return (0, 1)
    elif digit == "9":
        return (0, 2)
    elif digit == "4":
        return (1, 0)
    elif digit == "5":
        return (1, 1)
    elif digit == "6":
        return (1, 2)
    elif digit == "1":
        return (2, 0)
    elif digit == "2":
        return (2, 1)
    elif digit == "3":
        return (2, 2)
    elif digit == "0":
        return (3, 1)
    elif digit == "A":
        return (3, 2)
    else:
        assert False, f"invalid digit: {digit}"

def get_num_pad_symbol(row, col):
    if row == 0:
        if col == 0:
            return "7"
        elif col == 1:
            return "8"
        elif col == 2:
            return "9"
    elif row == 1:
        if col == 0:
            return "4"
        elif col == 1:
            return "5"
        elif col == 2:
            return "6"
    elif row == 2:
        if col == 0:
            return "1"
        elif col == 1:
            return "2"
        elif col == 2:
            return "3"
    elif row == 3:
        if col == 1:
            return "0"
        elif col == 2:
            return "A"
    assert False, f"invalid (row, col): ({row}, {col})"

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
def get_dir_pad_pos(button):
    if button == "^":
        return (0, 1)
    elif button == "A":
        return (0, 2)
    elif button == "<":
        return (1, 0)
    elif button == "v":
        return (1, 1)
    elif button == ">":
        return (1, 2)
    else:
        assert False, f"invalid button: {button}"

def get_dir_pad_symbol(row, col):
    if row == 0:
        if col == 1:
            return "^"
        elif col == 2:
            return "A"
    elif row == 1:
        if col == 0:
            return "<"
        elif col == 1:
            return "v"
        elif col == 2:
            return ">"
    assert False, f"invalid (row, col): ({row}, {col})"


def is_valid_num_robot(pos):
    y, x = pos
    if x < 0 or x > 2 or y < 0 or y > 3 or (x == 0 and y == 3):
        return False
    return True

def is_valid_dir_robot(pos):
    y, x = pos
    if x < 0 or x > 2 or y < 0 or y > 1 or (x == 0 and y == 0):
        return False
    return True


def calc_pad_path_len(from_pos, to_pos):
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    return abs(to_row - from_row) + abs(to_col - from_col)


def find_pad_shortest_paths(pos, target_pos, steps, direction, path: List[str], max_steps, numpad_shortest_paths: List[str], is_numpad=True):
    # print(f"pos: {pos}")
    row, col = pos
    if steps > max_steps:
        return
    if is_numpad and not is_valid_num_robot(pos):
        return
    if not is_numpad and not is_valid_dir_robot(pos):
        return
    if steps > 0:
        path.append(direction)
    if pos == target_pos:
        path.append("A")
        numpad_shortest_paths.append("".join(path))
        path.pop()
    else:
        find_pad_shortest_paths((row, col + 1), target_pos, steps + 1, ">", path, max_steps, numpad_shortest_paths)
        find_pad_shortest_paths((row + 1, col), target_pos, steps + 1, "v", path, max_steps, numpad_shortest_paths)
        find_pad_shortest_paths((row, col - 1), target_pos, steps + 1, "<", path, max_steps, numpad_shortest_paths)
        find_pad_shortest_paths((row - 1, col), target_pos, steps + 1, "^", path, max_steps, numpad_shortest_paths)
    # Remove last entry before returning
    if steps > 0:
        path.pop()

def calc_pad_shortest_paths(from_digit, to_digit, is_numpad=True):
    # print(f"{from_digit} to {to_digit}")
    # Find length of shortest paths in num keypad
    if is_numpad:
        pad_path_len = calc_pad_path_len(get_num_pad_pos(from_digit), get_num_pad_pos(to_digit))
    else:
        pad_path_len = calc_pad_path_len(get_dir_pad_pos(from_digit), get_dir_pad_pos(to_digit))
    # print(f"numpad_path_len: {numpad_path_len}")
    # Use DFS recursion to find all
    pad_shortest_paths = []
    from_pos = get_num_pad_pos(from_digit) if is_numpad else get_dir_pad_pos(from_digit)
    target_pos = get_num_pad_pos(to_digit) if is_numpad else get_dir_pad_pos(to_digit)
    path = []
    find_pad_shortest_paths(from_pos, target_pos, 0, "*", path, pad_path_len, pad_shortest_paths)
    assert len(pad_shortest_paths) >= 1, f"Error: no paths of length {pad_path_len} found"
    assert all(len(path) == pad_path_len + 1 for path in pad_shortest_paths) # +1 for pressing A
    return pad_shortest_paths


@cache
def calc_path_len(from_digit, to_digit, level):
    # Find all shortest paths in num keypad
    if level == NUM_DIRPADS:
        return 1
    numpad_shortest_paths = calc_pad_shortest_paths(from_digit, to_digit, is_numpad=level == 0)
    print(f"level: {level}, numpad_shortest_paths {numpad_shortest_paths}")
    path_lengths = []
    for numpad_path in numpad_shortest_paths:
        path_len = 0
        for ii in range(len(numpad_path)):
            from_symbol = "A" if ii == 0 else numpad_path[ii - 1]
            to_symbol = numpad_path[ii]
            path_len += calc_path_len(from_symbol, to_symbol, level + 1)
        path_lengths.append(path_len)
    
    print(len(path_lengths))
    assert min(path_lengths) > 0
    return min(path_lengths)


def calc_seq_len(code):
    seq_len = 0
    for ii in range(len(code)):
        from_digit = "A" if ii == 0 else code[ii - 1]
        to_digit = code[ii]
        partial_len = calc_path_len(from_digit, to_digit, 0)
        seq_len += partial_len
        print(f"from: {from_digit}, to: {to_digit}, partial_len: {partial_len}")
    return seq_len


def main():
    codes = parse_input("test_input.txt")
    values = [int(x[:-1]) for x in codes]
    codes = ["1"]
    values = [1]
    seq_lengths = []

    for code in codes:
        print(code)
        seq_lengths.append(calc_seq_len(code))
    
    print(f"NUM_DIRPADS: {NUM_DIRPADS}, seq_lengths: {seq_lengths}")

    complexities = [value * length for value, length in zip(values, seq_lengths)]
    print(sum(complexities))


if __name__ == "__main__":
    main()
