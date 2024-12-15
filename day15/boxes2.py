#!/usr/bin/env python3


def parse_input(input_data):
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
            # warehouse_map.append([symbol for symbol in line.rstrip()])
            warehouse_map.append([])
            for symbol in line.rstrip():
                if symbol == ".":
                    warehouse_map[-1].append(".")
                    warehouse_map[-1].append(".")
                elif symbol == "#":
                    warehouse_map[-1].append("#")
                    warehouse_map[-1].append("#")
                elif symbol == "O":
                    warehouse_map[-1].append("[")
                    warehouse_map[-1].append("]")
                else:
                    assert symbol == "@", f"unexpected symbol: {symbol}"
                    warehouse_map[-1].append("@")
                    warehouse_map[-1].append(".")
            robot_index = line.find("@")
            if robot_index != -1:
                robot_x = 2 * robot_index
                robot_y = line_number
        else:
            # read the moves
            for symbol in line.rstrip():
                assert symbol in (">", "v", "<", "^")
                moves.append(symbol)

    return warehouse_map, robot_x, robot_y, moves


def print_map(map):
    for line in map:
        print("".join(line))
    print()


def move_right(robot_x, robot_y, map):
    symbol = map[robot_y][robot_x]
    # print(f"moving object at pos x: {robot_x}, y: {robot_y} right (a {symbol})")
    assert symbol in ("@", "[", "]"), f"incorrect symbol to move: {map[robot_y][robot_x]}"
    could_move = False
    symbol_ahead = map[robot_y][robot_x + 1]
    if symbol_ahead == ".":
        # free space ahead, just take a step
        map[robot_y][robot_x] = "."
        map[robot_y][robot_x + 1] = symbol
        could_move = True
    elif symbol_ahead == "[" or symbol_ahead == "]":
        # hit a box
        # first move all boxes to the right of this box
        # then move this box
        could_move = move_right(robot_x + 1, robot_y, map)
        if could_move:
            assert map[robot_y][robot_x + 1] == ".", f"expected ., found {map[robot_y][robot_x + 1]}"
            map[robot_y][robot_x] = "."
            map[robot_y][robot_x + 1] = symbol
    else:
        # hit a wall, do nothing
        assert symbol_ahead == "#"
        could_move = False
    return could_move


def move_left(robot_x, robot_y, map):
    symbol = map[robot_y][robot_x]
    # print(f"moving object at pos x: {robot_x}, y: {robot_y} left (a {symbol})")
    assert symbol in ("@", "[", "]"), f"incorrect symbol to move: {map[robot_y][robot_x]}"
    could_move = False
    symbol_ahead = map[robot_y][robot_x - 1]
    if symbol_ahead == ".":
        # free space ahead, just take a step
        map[robot_y][robot_x] = "."
        map[robot_y][robot_x - 1] = symbol
        could_move = True
    elif symbol_ahead == "[" or symbol_ahead == "]":
        # hit a box
        # first move all boxes to the right of this box
        # then move this box
        could_move = move_left(robot_x - 1, robot_y, map)
        if could_move:
            assert map[robot_y][robot_x - 1] == ".", f"expected ., found {map[robot_y][robot_x - 1]}"
            map[robot_y][robot_x] = "."
            map[robot_y][robot_x - 1] = symbol
    else:
        # hit a wall, do nothing
        assert symbol_ahead == "#"
        could_move = False
    return could_move


def can_move_down(x, y, map):
    if map[y + 1][x] == "]":
        can_move = can_move_down(x - 1, y + 1, map) and can_move_down(x, y + 1, map)
    elif map[y + 1][x] == "[":
        can_move = can_move_down(x, y + 1, map) and can_move_down(x + 1, y + 1, map)
    elif map[y + 1][x] == ".":
        can_move = True
    else:
        assert map[y + 1][x] == "#"
        can_move = False
    return can_move

def move_down(x, y, map):
    if map[y][x] == "@":
        move_down(x, y + 1, map)
        map[y + 1][x] = "@"
        map[y][x] = "."
    elif map[y][x] == "[":
        move_down(x, y + 1, map)
        move_down(x + 1, y + 1, map)
        map[y + 1][x] = "["
        map[y + 1][x + 1] = "]"
        map[y][x] = "."
        map[y][x + 1] = "."
    elif map[y][x] == "]":
        move_down(x - 1, y + 1, map)
        move_down(x, y + 1, map)
        map[y + 1][x - 1] = "["
        map[y + 1][x] = "]"
        map[y][x - 1] = "."
        map[y][x] = "."


def check_and_move_down(x, y, map):
    symbol = map[y][x]
    # print(f"moving object at pos x: {x}, y: {y} down (a {symbol})")
    assert symbol in ("@", "[", "]"), f"incorrect symbol to move: {map[y][x]}"
    # check if all boxes in front of this box/robot can move
    # if all boxes in front can move then move them and
    # then move this box/robot
    if symbol == "@":
        can_move = can_move_down(x, y, map)
    elif symbol == "[":
        can_move = can_move_down(x, y, map) and can_move_down(x + 1, y, map)
    else:
        assert symbol == "]"
        can_move = can_move_down(x - 1, y, map) and can_move_down(x, y, map)
    if can_move:
        move_down(x, y, map)
    return can_move


def can_move_up(x, y, map):
    if map[y - 1][x] == "]":
        can_move = can_move_up(x - 1, y - 1, map) and can_move_up(x, y - 1, map)
    elif map[y - 1][x] == "[":
        can_move = can_move_up(x, y - 1, map) and can_move_up(x + 1, y - 1, map)
    elif map[y - 1][x] == ".":
        can_move = True
    else:
        assert map[y - 1][x] == "#"
        can_move = False
    return can_move

def move_up(x, y, map):
    if map[y][x] == "@":
        move_up(x, y - 1, map)
        map[y - 1][x] = "@"
        map[y][x] = "."
    elif map[y][x] == "[":
        move_up(x, y - 1, map)
        move_up(x + 1, y - 1, map)
        map[y - 1][x] = "["
        map[y - 1][x + 1] = "]"
        map[y][x] = "."
        map[y][x + 1] = "."
    elif map[y][x] == "]":
        move_up(x - 1, y - 1, map)
        move_up(x, y - 1, map)
        map[y - 1][x - 1] = "["
        map[y - 1][x] = "]"
        map[y][x - 1] = "."
        map[y][x] = "."


def check_and_move_up(x, y, map):
    symbol = map[y][x]
    # print(f"moving object at pos x: {x}, y: {y} up (a {symbol})")
    assert symbol in ("@", "[", "]"), f"incorrect symbol to move: {map[y][x]}"
    # check if all boxes in front of this box/robot can move
    # if all boxes in front can move then move them and
    # then move this box/robot
    if symbol == "@":
        can_move = can_move_up(x, y, map)
    elif symbol == "[":
        can_move = can_move_up(x, y, map) and can_move_up(x + 1, y, map)
    else:
        assert symbol == "]"
        can_move = can_move_up(x - 1, y, map) and can_move_up(x, y, map)
    if can_move:
        move_up(x, y, map)
    return can_move


def calc_gps_scores(warehouse_map):
    scores = []
    for row_number, line in enumerate(warehouse_map):
        for col_number, symbol in enumerate(line):
            if symbol == "[":
                scores.append(row_number * 100 + col_number)
    return scores


def main():
    warehouse_map, robot_x, robot_y, moves = parse_input("input.txt")
    # print_map(warehouse_map)
    for direction in moves:
        if direction == ">":
            could_move = move_right(robot_x, robot_y, warehouse_map)
            if could_move:
                robot_x += 1
        elif direction == "v":
            could_move = check_and_move_down(robot_x, robot_y, warehouse_map)
            if could_move:
                robot_y += 1
        elif direction == "<":
            could_move = move_left(robot_x, robot_y, warehouse_map)
            if could_move:
                robot_x -= 1
        else:
            assert direction == "^"
            could_move = check_and_move_up(robot_x, robot_y, warehouse_map)
            if could_move:
                robot_y -= 1
        # print_map(warehouse_map)

    
    gps_scores = calc_gps_scores(warehouse_map)
    print(sum(gps_scores))


if __name__ == "__main__":
    main()
