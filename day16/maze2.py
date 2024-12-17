#!/usr/bin/env python3

def parse_input(input_data):
    input_data = open(input_data, "r")
    maze = []
    for line_number, line in enumerate(input_data):
        maze.append(line.rstrip())
        S_index = line.find("S")
        if S_index != -1:
            start_x = S_index
            start_y = line_number
        E_index = line.find("E")
        if E_index != -1:
            end_x = E_index
            end_y = line_number
    width = len(maze[0])
    height = len(maze)
    return maze, start_x, start_y, end_x, end_y, width, height


def print_map(map):
    for line in map:
        print(line)


def check_east(x, y, score, path, maze, visited_pos):
    adj_positions = []
    if maze[y][x + 1] != "#":
        if visited_pos[y][x + 1][0] == -1 or score + 1 <= visited_pos[y][x + 1][0]:
            adj_positions.append((x + 1, y, ">", score + 1, path + [(x + 1, y)]))
            visited_pos[y][x + 1][0] = score + 1
    if maze[y - 1][x] != "#":
        if visited_pos[y - 1][x][0] == -1 or score + 1001 <= visited_pos[y - 1][x][0]:
            adj_positions.append((x, y - 1, "^", score + 1001, path + [(x, y - 1)]))
            visited_pos[y - 1][x][0] = score + 1001
    if maze[y + 1][x] != "#":
        if visited_pos[y + 1][x][0] == -1 or score + 1001 <= visited_pos[y + 1][x][0]:
            adj_positions.append((x, y + 1, "v", score + 1001, path + [(x, y + 1)]))
            visited_pos[y + 1][x][0] = score + 1001
    
    return adj_positions

def check_south(x, y, score, path, maze, visited_pos):
    adj_positions = []
    if maze[y + 1][x] != "#":
        if visited_pos[y + 1][x][1] == -1 or score + 1 <= visited_pos[y + 1][x][1]:
            adj_positions.append((x, y + 1, "v", score + 1, path + [(x, y + 1)]))
            visited_pos[y + 1][x][1] = score + 1
    if maze[y][x + 1] != "#":
        if visited_pos[y][x + 1][1] == -1 or score + 1001 <= visited_pos[y][x + 1][1]:
            adj_positions.append((x + 1, y, ">", score + 1001, path + [(x + 1, y)]))
            visited_pos[y][x + 1][1] = score + 1001
    if maze[y][x - 1] != "#":
        if visited_pos[y][x - 1][1] == -1 or score + 1001 <= visited_pos[y][x - 1][1]:
            adj_positions.append((x - 1, y, "<", score + 1001, path + [(x - 1, y)]))
            visited_pos[y][x - 1][1] = score + 1001
        
    return adj_positions

def check_west(x, y, score, path, maze, visited_pos):
    adj_positions = []
    if maze[y][x - 1] != "#":
        if visited_pos[y][x - 1][2] == -1 or score + 1 <= visited_pos[y][x - 1][2]:
            adj_positions.append((x - 1, y, "<", score + 1, path + [(x - 1, y)]))
            visited_pos[y][x - 1][2] = score + 1
    if maze[y + 1][x] != "#":
        if visited_pos[y + 1][x][2] == -1 or score + 1001 <= visited_pos[y + 1][x][2]:
            adj_positions.append((x, y + 1, "v", score + 1001, path + [(x, y + 1)]))
            visited_pos[y + 1][x][2] = score + 1001
    if maze[y - 1][x] != "#":
        if visited_pos[y - 1][x][2] == -1 or score + 1001 <= visited_pos[y - 1][x][2]:
            adj_positions.append((x, y - 1, "^", score + 1001, path + [(x, y - 1)]))
            visited_pos[y - 1][x][2] = score + 1001
    
    return adj_positions

def check_north(x, y, score, path, maze, visited_pos):
    adj_positions = []
    if maze[y - 1][x] != "#":
        if visited_pos[y - 1][x][3] == -1 or score + 1 <= visited_pos[y - 1][x][3]:
            adj_positions.append((x, y - 1, "^", score + 1, path + [(x, y - 1)]))
            visited_pos[y - 1][x][3] = score + 1
    if maze[y][x + 1] != "#":
        if visited_pos[y][x + 1][3] == -1 or score + 1001 <= visited_pos[y][x + 1][3]:
            adj_positions.append((x + 1, y, ">", score + 1001, path + [(x + 1, y)]))
            visited_pos[y][x + 1][3] = score + 1001
    if maze[y][x - 1] != "#":
        if visited_pos[y][x - 1][3] == -1 or score + 1001 <= visited_pos[y][x - 1][3]:
            adj_positions.append((x - 1, y, "<", score + 1001, path + [(x - 1, y)]))
            visited_pos[y][x - 1][3] = score + 1001
        
    return adj_positions


def calc_next_positions(x, y, direction, score, path, maze, visited_pos):
    if direction == ">":
        adj_positions = check_east(x, y, score, path, maze, visited_pos)
    elif direction == "v":
        adj_positions = check_south(x, y, score, path, maze, visited_pos)
    elif direction == "<":
        adj_positions = check_west(x, y, score, path, maze, visited_pos)
    else:
        assert direction == "^"
        adj_positions = check_north(x, y, score, path, maze, visited_pos)

    return adj_positions


def unique_positions(paths, scores):
    uniq_pos = set()
    for path, score in zip(paths, scores):
        if score == min(scores):
            for position in path:
                uniq_pos.add(position)
    return len(uniq_pos)

def print_path(path, width, height):
    for row_number in range(height):
        row = ""
        for col_number in range(width):
            if (col_number, row_number) in path:
                row += "X"
            else:
                row += "."
        print(row)
    print()

def main():
    maze, start_x, start_y, end_x, end_y, width, height = parse_input("input.txt")
    # print_map(maze)
    # print(f"start_x: {start_x}, start_y: {start_y}")

    visited_pos = [[[-1 for _ in range(4)] for _ in range(width)] for _ in range(height)]
    current_positions = [(start_x, start_y, ">", 0, [(start_x, start_y)])]
    next_positions = []
    successful_paths = []
    path_scores = []

    while True:
        next_positions = []
        if len(current_positions) == 0:
            break
        for x, y, direction, score, path in current_positions:
            # print(f"x: {x}, y: {y}")
            adj_positions = calc_next_positions(x, y, direction, score, path, maze, visited_pos)
            for x, y, _, score, path in adj_positions:
                if x == end_x and y == end_y:
                    successful_paths.append(path)
                    path_scores.append(score)
            next_positions.extend(adj_positions)

        current_positions = next_positions

    # for path, score in zip(successful_paths, path_scores):
    #     if score == min(path_scores):
    #         print_path(path, width, height)
    print(unique_positions(successful_paths, path_scores))

if __name__ == "__main__":
    main()
