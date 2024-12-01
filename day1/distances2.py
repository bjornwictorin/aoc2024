#!/usr/bin/env python3

def main():
    locations_file = open("input.txt", "r")
    locations = [[], []]
    for line in locations_file:
        loc0, loc1 = line.split("   ")
        locations[0].append(int(loc0))
        locations[1].append(int(loc1))
    total_dist = 0
    for ii, loc in enumerate(locations[0]):
        total_dist += loc * locations[1].count(loc)
    print(total_dist)


if __name__ == "__main__":
    main()
