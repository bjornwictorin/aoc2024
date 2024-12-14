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


def calc_safety_factor(robots, map_width, map_height):
    quadrants = 4 * [0]
    for robot in robots:
        # print(f"robot: {robot}")
        if robot.x < map_width // 2 and robot.y < map_height // 2:
            quadrants[0] += 1
        elif robot.x > map_width // 2 and robot.y < map_height // 2:
            quadrants[1] += 1
        elif robot.x < map_width // 2 and robot.y > map_height // 2:
            quadrants[2] += 1
        elif robot.x > map_width // 2 and robot.y > map_height // 2:
            quadrants[3] += 1
    print(quadrants)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

def main():
    robots = parse_input("input.txt")
    map_width = 101
    map_height = 103

    for _ in range(100):
        for robot in robots:
            robot.x = (robot.x + robot.x_velocity) % map_width
            robot.y = (robot.y + robot.y_velocity) % map_height
    
    safety_factor = calc_safety_factor(robots, map_width, map_height)

    print(safety_factor)

if __name__ == "__main__":
    main()
