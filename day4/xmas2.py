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

    for row in range(1, height - 1):
        for col in range(1, width - 1):
            if xmas_pattern[row][col] == "A":
                #M.S
                #.A.
                #M.S
                if xmas_pattern[row - 1][col - 1] == "M" and xmas_pattern[row - 1][col + 1] == "S" and xmas_pattern[row + 1][col + 1] == "S" and xmas_pattern[row + 1][col - 1] == "M":
                    num_xmas += 1
                #M.M
                #.A.
                #S.S
                if xmas_pattern[row - 1][col - 1] == "M" and xmas_pattern[row - 1][col + 1] == "M" and xmas_pattern[row + 1][col + 1] == "S" and xmas_pattern[row + 1][col - 1] == "S":
                    num_xmas += 1
                #S.M
                #.A.
                #S.M
                if xmas_pattern[row - 1][col - 1] == "S" and xmas_pattern[row - 1][col + 1] == "M" and xmas_pattern[row + 1][col + 1] == "M" and xmas_pattern[row + 1][col - 1] == "S":
                    num_xmas += 1
                #S.S
                #.A.
                #M.M
                if xmas_pattern[row - 1][col - 1] == "S" and xmas_pattern[row - 1][col + 1] == "S" and xmas_pattern[row + 1][col + 1] == "M" and xmas_pattern[row + 1][col - 1] == "M":
                    num_xmas += 1

    print(num_xmas)


if __name__ == "__main__":
    main()
