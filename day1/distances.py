#!/usr/bin/env python3

def main():
    locations_file = open("input.txt", "r")
    locations = [[], []]
    for line in locations_file:
        loc0, loc1 = line.split("   ")
        locations[0].append(int(loc0))
        locations[1].append(int(loc1))
    locations[0].sort()
    locations[1].sort()
    total_dist = 0
    for ii, loc in enumerate(locations[0]):
        total_dist += abs(loc - locations[1][ii])
    print(total_dist)


if __name__ == "__main__":
    main()
