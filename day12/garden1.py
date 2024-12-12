#!/usr/bin/env python3

def parse_input(input_data):
    input_data = open(input_data, "r")
    garden = []
    for line in input_data:
        garden.append(line.rstrip())
    width = len(garden[0])
    height = len(garden)
    return garden, width, height


def print_map(map):
    for line in map:
        print(line)


def meassure_region(symbol, row, col, height, width, garden_map, visited_pos):
    # include current positions area
    area = 1
    perimeter = 0
    visited_pos[row][col] = True
    # look right
    if col < width - 1 and not visited_pos[row][col + 1] and garden_map[row][col + 1] == symbol:
        # region continues on right side
        area_part, perimeter_part = meassure_region(symbol, row, col + 1, height, width, garden_map, visited_pos)
        area += area_part
        perimeter += perimeter_part
    elif col == width - 1 or garden_map[row][col + 1] != symbol:
        # region boundary on right side
        perimeter += 1
    # look below
    if row < height - 1 and not visited_pos[row + 1][col] and garden_map[row + 1][col] == symbol:
        # region continues below
        area_part, perimeter_part = meassure_region(symbol, row + 1, col, height, width, garden_map, visited_pos)
        area += area_part
        perimeter += perimeter_part
    elif row == height - 1 or garden_map[row + 1][col] != symbol:
        # region boundary on right side
        perimeter += 1
    # look left
    if col > 0 and not visited_pos[row][col - 1] and garden_map[row][col - 1] == symbol:
        # region continues on left side
        area_part, perimeter_part = meassure_region(symbol, row, col - 1, height, width, garden_map, visited_pos)
        area += area_part
        perimeter += perimeter_part
    elif col == 0 or garden_map[row][col - 1] != symbol:
        # region boundary on right side
        perimeter += 1
    # look above
    if row > 0 and not visited_pos[row - 1][col] and garden_map[row - 1][col] == symbol:
        # region continues above
        area_part, perimeter_part = meassure_region(symbol, row - 1, col, height, width, garden_map, visited_pos)
        area += area_part
        perimeter += perimeter_part
    elif row == 0 or garden_map[row - 1][col] != symbol:
        # region boundary on right side
        perimeter += 1

    return area, perimeter


def main():
    garden_map, width, height = parse_input("input.txt")
    
    visited_pos = [[False for _ in range(width)] for _ in range(height)]
    regions = []


    for row, line in enumerate(garden_map):
        for col, symbol in enumerate(line):
            if not visited_pos[row][col]:
                area, perimeter = meassure_region(symbol, row, col,  width, height, garden_map, visited_pos)
                regions.append((symbol, area, perimeter))

    scores = [x[1] * x[2] for x in regions]
    # print(regions)
    # print(scores)
    print(sum(scores))

if __name__ == "__main__":
    main()
