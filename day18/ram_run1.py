#!/usr/bin/env python3

width = 71
height = 71

def parse_input(input_data, num_fallen_bytes):
    input_data = open(input_data, "r")
    map = [["." for _ in range(width)] for _ in range(height)]
    for line_number, line in enumerate(input_data):
        if line_number == num_fallen_bytes:
            break
        x, y = line.rstrip().split(",")
        map[int(y)][int(x)] = "#"
    return map

 
def print_map(map):
    for line in map:
        print("".join(line))


def main():
    map = parse_input("input.txt", 1024)
    print_map(map)
    num_steps = 0
    current_positions = [(0, 0)]
    visited_positions = {(0, 0)}
    goal = (width - 1, height - 1) # lower right corner
    goal_reached = False

    while not goal_reached:
        next_positions = []
        num_steps += 1
        for x, y in current_positions:
            if goal_reached:
                break
            for next_x, next_y in ((x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)):
                if 0 <= next_x < width and 0 <= next_y < height and \
                map[next_y][next_x] == "." and (next_x, next_y) not in visited_positions:
                    if (next_x, next_y) == goal:
                        goal_reached = True
                        break
                    visited_positions.add((next_x, next_y))
                    next_positions.append((next_x, next_y))
        current_positions = next_positions
        #print(current_positions)

    print(num_steps)

if __name__ == "__main__":
    main()
