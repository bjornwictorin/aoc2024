#! /usr/bin/env python3

from typing import Set, Tuple


CONNECTIONS = set()
COMPUTERS = set()


def parse_input(file_name):
    global CONNECTIONS
    global COMPUTERS
    data = open(file_name, "r")
    for line in data:
        a, b = line.rstrip().split("-")
        CONNECTIONS.add((a, b))
        COMPUTERS.add(a)
        COMPUTERS.add(b)


def connected(computer_a, computer_b):
    return (computer_a, computer_b) in CONNECTIONS or (computer_b, computer_a) in CONNECTIONS


def find_groups(initial_groups: Set[Tuple], group_size):
    new_groups = set()
    for group in initial_groups:
        for other_computer in COMPUTERS:
            if other_computer not in group:
                # check if there is a connection from computer to all computers in group
                if all(connected(other_computer, comp) for comp in group):
                    new_group = list(group)
                    new_group.append(other_computer)
                    new_group.sort()
                    new_groups.add(tuple(new_group))
    for new_group in new_groups:
        assert len(new_group) == group_size
    return new_groups


def main():
    parse_input("input.txt")
    groups_of_x = []
    groups_of_x.append(CONNECTIONS)
    group_size = 3
    while(groups_of_x[-1]):
        groups_of_x.append(find_groups(groups_of_x[-1], group_size))
        group_size += 1
        # print(len(groups_of_x[-1]))
    
    assert len(groups_of_x[-1]) == 0
    assert len(groups_of_x[-2]) == 1
    biggest_group = groups_of_x[-2].pop()
    print(",".join(biggest_group))



if __name__ == "__main__":
    main()
