#!/usr/bin/env python3

from copy import deepcopy


def print_map(map):
    for line in map:
        print("".join(line))
    print()


def update_map(map, row, col):
    map_width = len(map[0])
    map_height = len(map)
    done = False
    if map[row][col] == "^":
        if row == 0:
            done = True
        elif map[row - 1][col] in ("#", "O"):
            # turn right
            map[row][col] = ">"
        else:
            # step up
            map[row - 1][col] = "^"
            row -= 1
    elif map[row][col] == ">":
        if col == map_width - 1:
            done = True
        elif map[row][col + 1] in ("#", "O"):
            # turn down
            map[row][col] = "v"
        else:
            # step right
            map[row][col + 1] = ">"
            col += 1
    elif map[row][col] == "v":
        if row == map_height - 1:
            done = True
        elif map[row + 1][col] in ("#", "O"):
            # turn left
            map[row][col] = "<"
        else:
            # step down
            map[row + 1][col] = "v"
            row += 1
    elif map[row][col] == "<":
        if col == 0:
            done = True
        elif map[row][col - 1] in ("#", "O"):
            # turn up
            map[row][col] = "^"
        else:
            # step left
            map[row][col - 1] = "<"
            col -= 1
    direction = map[row][col]

    return row, col, direction, done


def main():
    input_data = open("input.txt", "r")
    start_map = []
    start_row = 0
    start_col = 0
    start_direction = "^"
    for row_ii, line in enumerate(input_data):
        start_map.append([])
        for col_ii, letter in enumerate(line.rstrip()):
            start_map[-1].append(letter)
            if letter == start_direction:
                start_row = row_ii
                start_col = col_ii
    map_width = len(start_map[0])
    map_height = len(start_map)
    num_loop_pos = 0

    for row_ii in range(map_height):
        for col_ii in range(map_width):
            if start_map[row_ii][col_ii] == ".":
                map = deepcopy(start_map)
                # Create an empty position log for each map config
                position_log = [[[] for _ in range(map_width)] for _ in range(map_height)]
                # reset row and col
                row = start_row
                col = start_col
                direction = start_direction
                # place new obstacle
                map[row_ii][col_ii] = "O"
                # print_map(map)
                done = False
                is_loop = False
                while not done and not is_loop:
                    # store position
                    position_log[row][col].append(direction)
                    # update map
                    row, col, direction, done = update_map(map, row, col)
                    if direction not in ("^", ">", "v", "<", "."):
                        print_map(map)
                        print(f"row_ii: {row_ii}")
                        print(f"col_ii: {col_ii}")
                    assert direction in ("^", ">", "v", "<", "."), f"invalid direction: {direction} (at {row}, {col})"
                    # check if same position (direction and coordinate) was already visited
                    if direction in position_log[row][col]:
                        is_loop = not done
                if is_loop:
                    num_loop_pos += 1

    print(num_loop_pos)


if __name__ == "__main__":
    main()
