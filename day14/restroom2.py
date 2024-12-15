#!/usr/bin/env python3

import re


class Robot:
    def __init__(self, x, y, x_velocity, y_velocity):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
    
    def __repr__(self):
        return f"(x: {self.x}, y: {self.y})"


def parse_input(input_data):
    input_data = open(input_data, "r")
    robots = []
    for line in input_data:
        numbers = re.findall(r"p=(\d+),(\d+) v=([-]*\d+),([-]*\d+)", line)[0]
        assert len(numbers) == 4
        robots.append(Robot(int(numbers[0]), int(numbers[1]), int(numbers[2]), int(numbers[3])))
    return robots


def print_robots(robots, map_width, map_height):
    drawing = [[" " for _ in range(map_width)] for _ in range(map_height)]
    for robot in robots:
        drawing[robot.y][robot.x] = "*"
    for line in drawing:
        print("".join(line))
    print()

def main():
    robots = parse_input("input.txt")
    map_width = 101
    map_height = 103

    ii = 0
    """The x position for all robots will repeat itself every 101th (=map_width) step.
    The y position for all robots will repeat itself every 103rd (=map_height) step.
    After step 30 there is a distinct horizonrtal pattern. After step 81 there is a
    distinct vertical pattern. (Found by manually looking through patterns.)
    Find first step that is a multiple of 101 after 81 and a multiple of 103
    after 30."""
    while True:
        for robot in robots:
            robot.x = (robot.x + robot.x_velocity) % map_width
            robot.y = (robot.y + robot.y_velocity) % map_height
        ii += 1
        if ii % map_width == 81 and ii % map_height == 30:
            print_robots(robots, map_width, map_height)
            print(ii)
            break


if __name__ == "__main__":
    main()
