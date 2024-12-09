#!/usr/bin/env python3


class DiskNode:
    def __init__(self, id, size, is_file, prev_node, next_node, tried_to_move):
        self.id: int = id
        self.size: int = size
        self.is_file: bool = is_file
        self.prev_node: DiskNode = prev_node
        self.next_node: DiskNode = next_node
        self.tried_to_move: bool = tried_to_move
    
    def __repr__(self):
        return f"{self.id}, {self.size}, {self.is_file}"


def create_nodes(input_file):
    input = open(input_file, "r")
    first_node: DiskNode = None
    last_node: DiskNode = None
    latest_node = None
    for line in input:
        for ii, number in enumerate(line.rstrip()):
            assert number.isnumeric()
            # print(number)
            is_file = ii % 2 == 0
            node = DiskNode(ii // 2, int(number), is_file, None, None, False)
            if ii == 0:
                first_node = node
            else:
                node.prev_node = latest_node
                latest_node.next_node = node
            latest_node = node
            if ii == len(line) - 2:
                last_node = node
    return first_node, last_node


def calc_checksum(first_node: DiskNode):
    checksum = 0
    node = first_node
    block_pos = 0
    while node != None:
        block_end = block_pos + node.size
        while block_pos < block_end:
            if node.is_file:
                checksum += block_pos * node.id
            block_pos += 1
        node = node.next_node
    return checksum


def find_file_to_move(start_node: DiskNode):
    file_to_move = start_node
    while (file_to_move.tried_to_move or not file_to_move.is_file) and file_to_move.prev_node != None:
        file_to_move = file_to_move.prev_node
    return file_to_move


def find_gap_to_fill(first_node: DiskNode, file_to_move: DiskNode):
    gap_to_fill = first_node
    while gap_to_fill != None and (gap_to_fill.is_file or gap_to_fill.size < file_to_move.size):
        gap_to_fill = gap_to_fill.next_node
    return gap_to_fill
    

def main():
    first_node, last_node = create_nodes("input.txt")
    # first node can't be moved
    first_node.tried_to_move = True
    file_to_move = last_node
    assert file_to_move.is_file, "Last entry must be file!"
    gap_to_fill = first_node.next_node
    assert not gap_to_fill.is_file, "Gap to fill must not be a file!"
    while True:
        file_to_move = find_file_to_move(file_to_move)
        print(f"Trying to move file {file_to_move.id}")
        if file_to_move == first_node:
            break
        gap_to_fill = find_gap_to_fill(first_node, file_to_move)
        if gap_to_fill != None and gap_to_fill.id < file_to_move.id:
            file_before_gap = gap_to_fill.prev_node
            if file_to_move.size < gap_to_fill.size:
                print(f"Moving all file {file_to_move.id} to gap of size {gap_to_fill.size}")
                new_node = DiskNode(file_to_move.id, file_to_move.size, True, file_before_gap, gap_to_fill, True)
                file_before_gap.next_node = new_node
                gap_to_fill.prev_node = new_node
                gap_to_fill.size -= file_to_move.size
                assert gap_to_fill.size > 0, "incorrect size"
                # Convert file_to_move into empty space
                file_to_move.is_file = False
            elif file_to_move.size == gap_to_fill.size:
                print(f"Moving all file {file_to_move.id} to gap of size {gap_to_fill.size}")
                new_node = DiskNode(file_to_move.id, file_to_move.size, True, file_before_gap, gap_to_fill.next_node, True)
                file_before_gap.next_node = new_node
                gap_to_fill.next_node.prev_node = new_node
                # Change file_to_move and drop the node and the gap before it
                file_to_move.is_file = False

        else:
            file_to_move.tried_to_move = True


    checksum = calc_checksum(first_node)
    print(checksum)

if __name__ == "__main__":
    main()
