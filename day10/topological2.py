#!/usr/bin/env python3

def parse_input(input_data):
    input_data = open(input_data, "r")
    map = []
    for line in input_data:
        map.append([int(ii) for ii in line.rstrip()])
    return map


def print_map(map):
    for line in map:
        print(line)


def find_summits(row, col, map):
    map_width = len(map[0])
    map_height = len(map)
    assert 0 <= row < map_height, "illegal row"
    assert 0 <= col < map_width, "illegal col"
    height = map[row][col]
    if height == 9:
        return [(row, col)]
    reachable_summits = []
    # check above
    if row > 0 and map[row - 1][col] == height + 1:
        reachable_summits.extend(find_summits(row - 1, col, map))
    # check to the right
    if col < map_width - 1 and map[row][col + 1] == height + 1:
        reachable_summits.extend(find_summits(row, col + 1, map))
    # check below
    if row < map_height - 1 and map[row + 1][col] == height + 1:
        reachable_summits.extend(find_summits(row + 1, col, map))
    # check to the left
    if col > 0 and map[row][col - 1] == height + 1:
        reachable_summits.extend(find_summits(row, col - 1, map))
    return reachable_summits


def main():
    map = parse_input("input.txt")
    print_map(map)
    trailhead_scores = []
    for row, line in enumerate(map):
        for col, height in enumerate(line):
            if height == 0:
                reachable_summits = find_summits(row, col, map)
                num_paths = len(reachable_summits)
                trailhead_scores.append(num_paths)

    print(trailhead_scores)
    print(sum(trailhead_scores))

if __name__ == "__main__":
    main()
