#!/usr/bin/env python3

width = 71
height = 71
input_length = 3450
min_num_bytes = 1024

def parse_input():
    input_data = open("input.txt", "r")
    falling_bytes = []
    for line in input_data:
        x, y = line.rstrip().split(",")
        falling_bytes.append((int(x), int(y)))
    return falling_bytes

def generate_map(falling_bytes, n):
    map = [["." for _ in range(width)] for _ in range(height)]
    for byte_x, byte_y in falling_bytes[:n]:
        map[byte_y][byte_x] = "#"
    return map

 
def print_map(map):
    for line in map:
        print("".join(line))


def calc_num_steps(map):
    num_steps = 0
    current_positions = [(0, 0)]
    visited_positions = {(0, 0)}
    goal = (width - 1, height - 1) # lower right corner
    goal_reached = False

    while not goal_reached and len(current_positions) > 0:
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
    return num_steps if goal_reached else -1


def main():
    falling_bytes = parse_input()
    for num_fallen_bytes in range(min_num_bytes, input_length):
        map = generate_map(falling_bytes, num_fallen_bytes)
        num_steps = calc_num_steps(map)    
        if num_steps == -1:
            first_blocking_byte = falling_bytes[num_fallen_bytes - 1]
            break

    print(f"{first_blocking_byte[0]},{first_blocking_byte[1]}")

if __name__ == "__main__":
    main()
