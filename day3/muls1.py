#!/usr/bin/env python3

import re

def main():
    memory = open("input.txt", "r")
    product_sum = 0
    for line in memory:
        mul_pattern = r"mul\((\d+),(\d+)\)"
        regexp_matches = re.findall(mul_pattern, line)
        product_sum += sum(int(a) * int(b) for a, b in regexp_matches)
    print(product_sum)


if __name__ == "__main__":
    main()
