#! /usr/bin/env python3

map = []
width = 0
height = 0

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
    return tuple(map), start_pos, end_pos, width, height


def find_next_pos(pos, visited_pos):
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


def get_path(start_pos, end_pos, map):
    path = [start_pos]
    pos = start_pos
    while pos != end_pos:
        pos = find_next_pos(pos, path)
        path.append(pos)

    return tuple(path)


def calc_useful_cheats(pos, pos_index, cheat_steps, path):
    num_useful_cheats = 0
    pos_x, pos_y = pos
    for x_offset in range(-cheat_steps, cheat_steps + 1):
        for y_offset in range(-(cheat_steps - abs(x_offset)), (cheat_steps - abs(x_offset)) + 1):
            x = pos_x + x_offset
            y = pos_y + y_offset
            if (0 < x < width - 1) and (0 < y < height - 1):
                if (x, y) in path[pos_index + 100 + abs(x_offset) + abs(y_offset):]:
                    num_useful_cheats += 1

    return num_useful_cheats




def main():
    global map
    global width
    global height
    map, start_pos, end_pos, width, height = parse_input("input.txt")
    
    path = get_path(start_pos, end_pos, map)
    num_useful_cheats = 0

    cheat_steps = 20
    for pos_index, pos in enumerate(path):
        num_useful_cheats += calc_useful_cheats(pos, pos_index, cheat_steps, path)
        print(".", end="", flush=True)
    print()

    print(num_useful_cheats)


if __name__ == "__main__":
    main()
