#!/usr/bin/env python3

def parse_input():
    input_data = open("input.txt", "r")
    antennas = {}
    map_height = 0
    map_width = 0
    for row_idx, line in enumerate(input_data):
        map_height += 1
        map_width = len(line.rstrip())
        for col_idx, letter in enumerate(line):
            if letter.isalnum():
                pos = (row_idx, col_idx)
                if letter not in antennas:
                    antennas[letter] = [pos]
                else:
                    antennas[letter].append(pos)
    return antennas, map_height, map_width


def calc_antinode(coord0, coord1):
    print(f"{coord0}, {coord1}")
    # vertical (y) direction
    row = coord0[0] + coord0[0] - coord1[0]
    col = coord0[1] + coord0[1] - coord1[1]
    # print(f"x: {x}")
    # print(f"y: {y}")
    return col, row
    # return 0 <= y < map_height and 0 <= x < map_width



def main():
    antennas, map_height, map_width = parse_input()
    antinodes = set()
    for antenna_name, coordinates in antennas.items():
        print(antenna_name)
        print(coordinates)
        for coord_index, coord in enumerate(coordinates[:-1]):
            for other_coord in coordinates[coord_index + 1:]:
                x, y = calc_antinode(coord, other_coord)
                if 0 <= y < map_height and 0 <= x < map_width:
                    antinodes.add((x, y))
                x, y = calc_antinode(other_coord, coord)
                if 0 <= y < map_height and 0 <= x < map_width:
                    antinodes.add((x, y))

    print(len(antinodes))

if __name__ == "__main__":
    main()
