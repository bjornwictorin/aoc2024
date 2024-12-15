#!/usr/bin/env python3


map_width = 0
map_height = 0


def parse_input(input_data):
    global map_width
    global map_height
    input_data = open(input_data, "r")
    warehouse_map = []
    robot_x = 0
    robot_y = 0
    moves = []
    above_space = True
    for line_number, line in enumerate(input_data):
        if line == "\n":
            above_space = False
        elif above_space:
            # read the map
            warehouse_map.append([symbol for symbol in line.rstrip()])
            robot_index = line.find("@")
            if robot_index != -1:
                robot_x = robot_index
                robot_y = line_number
        else:
            # read the moves
            for symbol in line.rstrip():
                assert symbol in (">", "v", "<", "^")
                moves.append(symbol)

    map_width = len(warehouse_map[0])
    map_height = len(warehouse_map)
    return warehouse_map, robot_x, robot_y, moves


def print_map(map):
    for line in map:
        print("".join(line))
    print()


def update_map(direction, robot_x, robot_y, map):
    symbol = map[robot_y][robot_x]
    # print(f"moving object at pos x: {robot_x}, y: {robot_y} in direction {direction} (a {symbol})")
    assert symbol in ("@", "O"), f"incorrect symbol to move: {map[robot_y][robot_x]}"
    could_move = False

    # Move right
    if direction == ">":
        symbol_ahead = map[robot_y][robot_x + 1]
        if symbol_ahead == ".":
            # free space ahead, just take a step
            map[robot_y][robot_x] = "."
            map[robot_y][robot_x + 1] = symbol
            could_move = True
        elif symbol_ahead == "O":
            # hit a box
            # first move all boxes to the right of this box
            # then move this box
            could_move = update_map(direction, robot_x + 1, robot_y, map)
            if could_move:
                assert map[robot_y][robot_x + 1] == ".", f"expected ., found {map[robot_y][robot_x + 1]}"
                map[robot_y][robot_x] = "."
                map[robot_y][robot_x + 1] = symbol
        else:
            # hit a wall, do nothing
            assert symbol_ahead == "#"
            could_move = False
        
    # Move down
    elif direction == "v":
        symbol_ahead = map[robot_y + 1][robot_x]
        if symbol_ahead == ".":
            # free space ahead, just take a step
            map[robot_y][robot_x] = "."
            map[robot_y + 1][robot_x] = symbol
            could_move = True
        elif symbol_ahead == "O":
            # hit a box
            # first move all boxes to the right of this box
            # then move this box
            could_move = update_map(direction, robot_x, robot_y + 1, map)
            if could_move:
                assert map[robot_y + 1][robot_x] == "."
                map[robot_y][robot_x] = "."
                map[robot_y + 1][robot_x] = symbol
        else:
            # hit a wall, do nothing
            assert symbol_ahead == "#"
            could_move = False

    # Move left
    elif direction == "<":
        symbol_ahead = map[robot_y][robot_x - 1]
        if symbol_ahead == ".":
            # free space ahead, just take a step
            map[robot_y][robot_x] = "."
            map[robot_y][robot_x - 1] = symbol
            could_move = True
        elif symbol_ahead == "O":
            # hit a box
            # first move all boxes to the right of this box
            # then move this box
            could_move = update_map(direction, robot_x - 1, robot_y, map)
            if could_move:
                assert map[robot_y][robot_x - 1] == "."
                map[robot_y][robot_x] = "."
                map[robot_y][robot_x - 1] = symbol
        else:
            # hit a wall, do nothing
            assert symbol_ahead == "#"
            could_move = False

    # Move up
    elif direction == "^":
        symbol_ahead = map[robot_y - 1][robot_x]
        if symbol_ahead == ".":
            # free space ahead, just take a step
            map[robot_y][robot_x] = "."
            map[robot_y - 1][robot_x] = symbol
            could_move = True
        elif symbol_ahead == "O":
            # hit a box
            # first move all boxes to the right of this box
            # then move this box
            could_move = update_map(direction, robot_x, robot_y - 1, map)
            if could_move:
                assert map[robot_y - 1][robot_x] == "."
                map[robot_y][robot_x] = "."
                map[robot_y - 1][robot_x] = symbol
        else:
            # hit a wall, do nothing
            assert symbol_ahead == "#"
            could_move = False

    return could_move


def calc_gps_scores(warehouse_map):
    scores = []
    for row_number, line in enumerate(warehouse_map):
        for col_number, symbol in enumerate(line):
            if symbol == "O":
                scores.append(row_number * 100 + col_number)
    return scores


def main():
    warehouse_map, robot_x, robot_y, moves = parse_input("input.txt")
    # print_map(warehouse_map)
    for direction in moves:
        could_move = update_map(direction, robot_x, robot_y, warehouse_map)
        # print_map(warehouse_map)
        if could_move:
            if direction == ">":
                robot_x += 1
            elif direction == "v":
                robot_y += 1
            elif direction == "<":
                robot_x -= 1
            else:
                assert direction == "^"
                robot_y -= 1

    
    gps_scores = calc_gps_scores(warehouse_map)
    print(sum(gps_scores))


if __name__ == "__main__":
    main()
