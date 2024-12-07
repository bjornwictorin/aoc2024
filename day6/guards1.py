#!/usr/bin/env python3

def main():
    input_data = open("input.txt", "r")
    map = []
    row = 0
    col = 0
    for row_ii, line in enumerate(input_data):
        map.append([])
        for col_ii, letter in enumerate(line.rstrip()):
            map[-1].append(letter)
            if letter == "^":
                row = row_ii
                col = col_ii
    map_width = len(map[0])
    map_height = len(map)
    # print(map)
    # print(pos)


    while True:
        # print(map)
        if map[row][col] == "^":
            if row == 0:
                break
            elif map[row - 1][col] == "#":
                # turn right
                map[row][col] = ">"
            else:
                # step up
                map[row][col] = "X"
                map[row - 1][col] = "^"
                row -= 1
        elif map[row][col] == ">":
            if col == map_width - 1:
                break
            elif map[row][col + 1] == "#":
                # turn down
                map[row][col] = "v"
            else:
                # step right
                map[row][col] = "X"
                map[row][col + 1] = ">"
                col += 1
        elif map[row][col] == "v":
            if row == map_height - 1:
                break
            elif map[row + 1][col] == "#":
                # turn left
                map[row][col] = "<"
            else:
                # step down
                map[row][col] = "X"
                map[row + 1][col] = "v"
                row += 1
        elif map[row][col] == "<":
            if col == 0:
                break
            elif map[row][col - 1] == "#":
                # turn up
                map[row][col] = "^"
            else:
                # step left
                map[row][col] = "X"
                map[row][col - 1] = "<"
                col -= 1
    
    # mark the last pos
    map[row][col] = "X"
    num_visited_pos = sum(ii.count("X") for ii in map)
    print(num_visited_pos)


if __name__ == "__main__":
    main()
