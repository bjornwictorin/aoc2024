#!/usr/bin/env python3

width = 0
height = 0

def parse_input(input_data):
    global width
    global height

    input_data = open(input_data, "r")
    garden = []
    for line in input_data:
        garden.append(line.rstrip())
    
    width = len(garden[0])
    
    height = len(garden)
    return garden


def meassure_region(symbol, row, col, garden_map, visited_pos):
    # include current positions area
    area = 1
    num_corners = 0
    visited_pos[row][col] = True
    continues_right = False
    continues_below = False
    continues_left = False
    continues_above = False
    # look right
    if col < width - 1 and not visited_pos[row][col + 1] and garden_map[row][col + 1] == symbol:
        # region continues on right side
        area_part, num_corners_part = meassure_region(symbol, row, col + 1, garden_map, visited_pos)
        area += area_part
        num_corners += num_corners_part
    if col < width - 1 and garden_map[row][col + 1] == symbol:
        # same as condition above, but without the already visited check
        continues_right = True
    # look below
    if row < height - 1 and not visited_pos[row + 1][col] and garden_map[row + 1][col] == symbol:
        # region continues below
        area_part, num_corners_part = meassure_region(symbol, row + 1, col, garden_map, visited_pos)
        area += area_part
        num_corners += num_corners_part
    if row < height - 1 and garden_map[row + 1][col] == symbol:
        # same as condition above, but without the already visited check
        continues_below = True
    # look left
    if col > 0 and not visited_pos[row][col - 1] and garden_map[row][col - 1] == symbol:
        # region continues on left side
        area_part, num_corners_part = meassure_region(symbol, row, col - 1, garden_map, visited_pos)
        area += area_part
        num_corners += num_corners_part
    if col > 0 and garden_map[row][col - 1] == symbol:
        # same as condition above, but without the already visited check
        continues_left = True
    # look above
    if row > 0 and not visited_pos[row - 1][col] and garden_map[row - 1][col] == symbol:
        # region continues above
        area_part, num_corners_part = meassure_region(symbol, row - 1, col, garden_map, visited_pos)
        area += area_part
        num_corners += num_corners_part
    if row > 0 and garden_map[row - 1][col] == symbol:
        # same as condition above, but without the already visited check
        continues_above = True
    
    num_sharp_corners = 0
    # sharp corner detection
    if not continues_right and not continues_below:
        # sharp corner on lower right side
        num_sharp_corners += 1
    if not continues_below and not continues_left:
        # sharp corner on lower left side
        num_sharp_corners += 1
    if not continues_left and not continues_above:
        # sharp corner on upper left side
        num_sharp_corners += 1
    if not continues_above and not continues_right:
        # sharp corner on upper right side
        num_sharp_corners += 1
    
    num_non_sharp_corners = 0
    # non-sharp corner detection
    if continues_right and continues_below and garden_map[row + 1][col + 1] != symbol:
        # non-sharp corner on lower right side
        num_non_sharp_corners += 1
    if continues_below and continues_left and garden_map[row + 1][col - 1] != symbol:
        # non-sharp corner on lower left side
        num_non_sharp_corners += 1
    if continues_left and continues_above and garden_map[row - 1][col - 1] != symbol:
        # non-sharp corner on upper left side
        num_non_sharp_corners += 1
    if continues_above and continues_right and garden_map[row - 1][col + 1] != symbol:
        # non-sharp corner on upper right side
        num_non_sharp_corners += 1

    num_corners += num_sharp_corners
    num_corners += num_non_sharp_corners

    return area, num_corners


def main():
    garden_map = parse_input("input.txt")
    
    regions = []
    visited_pos = [[False for _ in range(width)] for _ in range(height)]

    for row, line in enumerate(garden_map):
        for col, symbol in enumerate(line):
            if not visited_pos[row][col]:
                area, num_corners = meassure_region(symbol, row, col, garden_map, visited_pos)
                regions.append((symbol, area, num_corners))

    # Note: num_sides == num_corners
    scores = [x[1] * x[2] for x in regions]
    print(sum(scores))

if __name__ == "__main__":
    main()
