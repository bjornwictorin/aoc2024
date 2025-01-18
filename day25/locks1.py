#! /usr/bin/env python3

def parse_input(filename):
    data = open(filename, "r")
    locks = []
    keys = []
    is_key = False
    columns = [0, 0, 0, 0, 0]
    for ii, line in enumerate(data):
        for jj, char in enumerate(line.rstrip()):
            if char == "#":
                columns[jj] += 1
        if ii % 8 == 0:
            if line.rstrip() == ".....":
                is_key = True
            else:
                is_key = False
        if ii % 8 == 7:
            if is_key:
                keys.append(tuple(columns))
            else:
                locks.append(tuple(columns))
            columns = [0, 0, 0, 0, 0]
    # add the last lock/key
    if is_key:
        keys.append(tuple(columns))
    else:
        locks.append(tuple(columns))
    return locks, keys


def key_fits_lock(key, lock):
    for ii in range(5):
        if key[ii] + lock[ii] > 7:
            return False
    return True


def main():
    locks, keys = parse_input("input.txt")
    key_lock_combinations = 0
    for lock in locks:
        for key in keys:
            if key_fits_lock(key, lock):
                key_lock_combinations += 1
    
    print(key_lock_combinations)


if __name__ == "__main__":
    main()
