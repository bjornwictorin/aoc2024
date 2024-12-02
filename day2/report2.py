#!/usr/bin/env python3

def check_levels(levels):
    level_diffs = [int(levels[ii+1]) - int(levels[ii]) for ii in range(len(levels) - 1)]
    return all(4 > diff > 0 for diff in level_diffs) or all(-4 < diff < 0 for diff in level_diffs)

def main():
    reports = open("input.txt", "r")
    safe_reports = 0
    for line in reports:
        levels = line.rstrip().split(" ")
        if check_levels(levels):
            safe_reports += 1
        else:
            for ii in range(len(levels)):
                if check_levels(levels[:ii] + levels[ii+1:]):
                    safe_reports += 1
                    break

    print(safe_reports)


if __name__ == "__main__":
    main()
