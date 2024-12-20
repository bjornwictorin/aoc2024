#! /usr/bin/env python3


def parse_input(input_file):
    input_data = open(input_file, "r")
    map = []
    for line_number, line in enumerate(input_data):
        map.append(line.rstrip())
        s_index = line.find("S")
        if s_index != -1:
            start_pos = (s_index, line_number)
        e_index = line.find("E")
        if e_index != -1:
            end_pos = (e_index, line_number)
    width = len(map[0])
    height = len(map)
    return map, start_pos, end_pos, width, height


def print_map(map):
    for line in map:
        print(line)
    print()


def find_next_pos(pos, map, visited_pos):
    x, y = pos
    if map[y][x + 1] != "#" and (x + 1, y) not in visited_pos:
        return (x + 1, y)
    elif map[y + 1][x] != "#" and (x, y + 1) not in visited_pos:
        return (x, y + 1)
    elif map[y][x - 1] != "#" and (x - 1, y) not in visited_pos:
        return (x - 1, y)
    elif map[y - 1][x] != "#" and (x, y - 1) not in visited_pos:
        return (x, y - 1)
    else:
        assert False, "Error: should have found next pos"


def find_shortcut_ends(pos, map, width, height, visited_pos):
    x, y = pos
    shortcut_end_list = []
    if x < width - 3 and map[y][x + 1] == "#" and map[y][x + 2] != "#" and (x + 2, y) not in visited_pos:
        shortcut_end_list.append((x + 2, y))
    if y < height - 3 and map[y + 1][x] == "#" and map[y + 2][x] != "#" and (x, y + 2) not in visited_pos:
        shortcut_end_list.append((x, y + 2))
    if x >= 3 and map[y][x - 1] == "#" and map[y][x - 2] != "#" and (x - 2, y) not in visited_pos:
        shortcut_end_list.append((x - 2, y))
    if y >= 3 and map[y - 1][x] == "#" and map[y - 2][x] != "#" and (x, y - 2) not in visited_pos:
        shortcut_end_list.append((x, y - 2))
    return shortcut_end_list


def calc_shortcut_saving(pos, shortcut_end, map, visited_pos):
    x, y = pos
    steps = 0
    while pos != shortcut_end:
        visited_pos.append(pos)
        pos = find_next_pos(pos, map, visited_pos)
        steps += 1
    assert steps >= 4  # shortest possible shortcut walks from one side of # to the other
    return steps - 2


def main():
    map, start_pos, end_pos, width, height = parse_input("input.txt")
    print_map(map)
    shortcut_savings = {}
    visited_pos = []
    pos = start_pos
    while pos != end_pos:
        shortcut_end_list = find_shortcut_ends(pos, map, width, height, visited_pos)
        for shortcut_end in shortcut_end_list:
            saving = calc_shortcut_saving(pos, shortcut_end, map, visited_pos.copy())
            if saving in shortcut_savings:
                shortcut_savings[saving] += 1
            else:
                shortcut_savings[saving] = 1
        visited_pos.append(pos)
        pos = find_next_pos(pos, map, visited_pos)

    num_useful_shortcuts = 0
    for saving, num_occurences in shortcut_savings.items():
        if saving >= 100:
            num_useful_shortcuts += num_occurences

    print(num_useful_shortcuts)


if __name__ == "__main__":
    main()
