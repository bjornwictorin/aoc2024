#!/usr/bin/env python3

import re

def main():
    memory = open("input.txt", "r")
    product_sum = 0
    do = True
    for line in memory:
        mul_pattern = r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))"
        regexp_matches = re.findall(mul_pattern, line)
        # print(regexp_matches)
        for instr in regexp_matches:
            if instr[2] == "do()":
                do = True
            elif instr[3] == "don't()":
                do = False
            else:
                if do:
                    product_sum += int(instr[0]) * int(instr[1])

    print(product_sum)

if __name__ == "__main__":
    main()
