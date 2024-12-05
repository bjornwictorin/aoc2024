#!/usr/bin/env python3


def main():
    xmas_text = open("input.txt", "r")
    num_xmas = 0
    xmas_pattern = []
    for line in xmas_text:
        xmas_pattern.append(line.rstrip())
    xmas_text.close()
    height = len(xmas_pattern)
    width = len(xmas_pattern[0])

    for row in range(height):
        for col in range(width):
            if xmas_pattern[row][col] == "X":
                if col < width - 3 and xmas_pattern[row][col + 1] == "M" and xmas_pattern[row][col + 2] == "A" and xmas_pattern[row][col + 3] == "S":
                    num_xmas += 1
                if col < width - 3 and row < height - 3 and xmas_pattern[row + 1][col + 1] == "M" and xmas_pattern[row + 2][col + 2] == "A" and xmas_pattern[row + 3][col + 3] == "S":
                    num_xmas += 1
                if row < height - 3 and xmas_pattern[row + 1][col] == "M" and xmas_pattern[row + 2][col] == "A" and xmas_pattern[row + 3][col] == "S":
                    num_xmas += 1
                if row < height - 3 and col >= 3 and xmas_pattern[row + 1][col - 1] == "M" and xmas_pattern[row + 2][col - 2] == "A" and xmas_pattern[row + 3][col - 3] == "S":
                    num_xmas += 1
                if col >= 3 and xmas_pattern[row][col - 1] == "M" and xmas_pattern[row][col - 2] == "A" and xmas_pattern[row][col - 3] == "S":
                    num_xmas += 1
                if row >= 3 and col >= 3 and xmas_pattern[row - 1][col - 1] == "M" and xmas_pattern[row - 2][col - 2] == "A" and xmas_pattern[row - 3][col - 3] == "S":
                    num_xmas += 1
                if row >= 3 and xmas_pattern[row - 1][col] == "M" and xmas_pattern[row - 2][col] == "A" and xmas_pattern[row - 3][col] == "S":
                    num_xmas += 1
                if col < width - 3 and row >= 3 and xmas_pattern[row - 1][col + 1] == "M" and xmas_pattern[row - 2][col + 2] == "A" and xmas_pattern[row - 3][col + 3] == "S":
                    num_xmas += 1

    print(num_xmas)


if __name__ == "__main__":
    main()
