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


def check_east(x, y, score, maze, visited_pos):
    adj_positions = []
    if maze[y][x + 1] != "#":
        if visited_pos[y][x + 1] == -1 or score + 1 < visited_pos[y][x + 1]:
            adj_positions.append((x + 1, y, ">", score + 1))
            visited_pos[y][x + 1] = score + 1
    if maze[y - 1][x] != "#":
        if visited_pos[y - 1][x] == -1 or score + 1001 < visited_pos[y - 1][x]:
            adj_positions.append((x, y - 1, "^", score + 1001))
            visited_pos[y - 1][x] = score + 1001
    if maze[y + 1][x] != "#":
        if visited_pos[y + 1][x] == -1 or score + 1001 < visited_pos[y + 1][x]:
            adj_positions.append((x, y + 1, "v", score + 1001))
            visited_pos[y + 1][x] = score + 1001
    
    return adj_positions

def check_south(x, y, score, maze, visited_pos):
    adj_positions = []
    if maze[y + 1][x] != "#":
        if visited_pos[y + 1][x] == -1 or score + 1 < visited_pos[y + 1][x]:
            adj_positions.append((x, y + 1, "v", score + 1))
            visited_pos[y + 1][x] = score + 1
    if maze[y][x + 1] != "#":
        if visited_pos[y][x + 1] == -1 or score + 1001 < visited_pos[y][x + 1]:
            adj_positions.append((x + 1, y, ">", score + 1001))
            visited_pos[y][x + 1] = score + 1001
    if maze[y][x - 1] != "#":
        if visited_pos[y][x - 1] == -1 or score + 1001 < visited_pos[y][x - 1]:
            adj_positions.append((x - 1, y, "<", score + 1001))
            visited_pos[y][x - 1] = score + 1001
        
    return adj_positions

def check_west(x, y, score, maze, visited_pos):
    adj_positions = []
    if maze[y][x - 1] != "#":
        if visited_pos[y][x - 1] == -1 or score + 1 < visited_pos[y][x - 1]:
            adj_positions.append((x - 1, y, "<", score + 1))
            visited_pos[y][x - 1] = score + 1
    if maze[y + 1][x] != "#":
        if visited_pos[y + 1][x] == -1 or score + 1001 < visited_pos[y + 1][x]:
            adj_positions.append((x, y + 1, "v", score + 1001))
            visited_pos[y + 1][x] = score + 1001
    if maze[y - 1][x] != "#":
        if visited_pos[y - 1][x] == -1 or score + 1001 < visited_pos[y - 1][x]:
            adj_positions.append((x, y - 1, "^", score + 1001))
            visited_pos[y - 1][x] = score + 1001
    
    return adj_positions

def check_north(x, y, score, maze, visited_pos):
    adj_positions = []
    if maze[y - 1][x] != "#":
        if visited_pos[y - 1][x] == -1 or score + 1 < visited_pos[y - 1][x]:
            adj_positions.append((x, y - 1, "^", score + 1))
            visited_pos[y - 1][x] = score + 1
    if maze[y][x + 1] != "#":
        if visited_pos[y][x + 1] == -1 or score + 1001 < visited_pos[y][x + 1]:
            adj_positions.append((x + 1, y, ">", score + 1001))
            visited_pos[y][x + 1] = score + 1001
    if maze[y][x - 1] != "#":
        if visited_pos[y][x - 1] == -1 or score + 1001 < visited_pos[y][x - 1]:
            adj_positions.append((x - 1, y, "<", score + 1001))
            visited_pos[y][x - 1] = score + 1001
        
    return adj_positions


def calc_next_positions(x, y, direction, score, maze, visited_pos):
    if direction == ">":
        adj_positions = check_east(x, y, score, maze, visited_pos)
    elif direction == "v":
        adj_positions = check_south(x, y, score, maze, visited_pos)
    elif direction == "<":
        adj_positions = check_west(x, y, score, maze, visited_pos)
    else:
        assert direction == "^"
        adj_positions = check_north(x, y, score, maze, visited_pos)

    return adj_positions


def main():
    maze, start_x, start_y, end_x, end_y, width, height = parse_input("input.txt")
    # print_map(maze)
    # print(f"start_x: {start_x}, start_y: {start_y}")
    
    lowest_score = 1000000 # big number
    visited_pos = [[-1 for _ in range(width)] for _ in range(height)]
    current_positions = [(start_x, start_y, ">", 0)]
    next_positions = []

    while True:
        next_positions = []
        if len(current_positions) == 0:
            break
        for x, y, direction, score in current_positions:
            # print(f"x: {x}, y: {y}")
            adj_positions = calc_next_positions(x, y, direction, score, maze, visited_pos)
            for x, y, _, score in adj_positions:
                if x == end_x and y == end_y and score < lowest_score:
                    lowest_score = score
            next_positions.extend(adj_positions)

        current_positions = next_positions

    print(lowest_score)

if __name__ == "__main__":
    main()
