#! /usr/bin/env python3


def parse_input(file_name):
    data = open(file_name, "r")
    connections = []
    for line in data:
        a, b = line.rstrip().split("-")
        connections.append((a, b))
    return connections


def find_tripples(connections):
    tripples = set()
    for pair in connections:
        lhs, rhs = pair
        # find all other connections that contain the lhs
        other_pairs_containing_lhs = [p for p in connections if p != pair and lhs in p]
        # for each of the other pairs, check if there exists a pair with lhs and the other computer in the other pair
        # if so, then that is a tripple
        for other_pair in other_pairs_containing_lhs:
            # print(other_pair)
            other_lhs, other_rhs = other_pair
            other_computer = other_lhs if other_rhs == lhs else other_rhs
            # print(f"other_computer: {other_computer}")
            if (rhs, other_computer) in connections or (other_computer, rhs) in connections:
                tripples.add(tuple(sorted((lhs, rhs, other_computer))))
        
        # find all other connections that contain the rhs
        other_pairs_containing_rhs = [p for p in connections if p != pair and rhs in p]
        # for each of the other pairs, check if there exists a pair with rhs and the other computer in the other pair
        # if so, then that is a tripple
        for other_pair in other_pairs_containing_rhs:
            other_lhs, other_rhs = other_pair
            other_computer = other_lhs if other_rhs == rhs else other_rhs
            if (lhs, other_computer) in connections or (other_computer, lhs) in connections:
                tripples.add(tuple(sorted((lhs, rhs, other_computer))))

    return tripples


def main():
    connections = parse_input("input.txt")
    # print(connections)
    tripples = find_tripples(connections)
    num_candidates = 0
    for tripple in tripples:
        if any(computer.startswith("t") for computer in tripple):
            num_candidates += 1
    
    # print(tripples)
    # print(len(tripples))
    print(num_candidates)


if __name__ == "__main__":
    main()
