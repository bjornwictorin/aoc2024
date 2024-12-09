#!/usr/bin/env python3


class DiskNode:
    def __init__(self, id, size, is_file, prev_node, next_node):
        self.id: int = id
        self.size: int = size
        self.is_file: bool = is_file
        self.prev_node: DiskNode = prev_node
        self.next_node: DiskNode = next_node
    
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
            node = DiskNode(ii // 2, int(number), is_file, None, None)
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
            checksum += block_pos * node.id
            block_pos += 1
        node = node.next_node
    return checksum


def main():
    first_node, last_node = create_nodes("input.txt")
    file_to_move = last_node
    assert file_to_move.is_file, "Last entry must be file!"
    gap_to_fill = first_node.next_node
    assert not gap_to_fill.is_file, "Gap to fill must not be a file!"
    while gap_to_fill != None:
        file_before_gap = gap_to_fill.prev_node
        if file_to_move.size < gap_to_fill.size:
            print(f"Moving all file {file_to_move.id} to gap of size {gap_to_fill.size}")
            new_node = DiskNode(file_to_move.id, file_to_move.size, True, file_before_gap, gap_to_fill)
            file_before_gap.next_node = new_node
            gap_to_fill.prev_node = new_node
            gap_to_fill.size -= file_to_move.size
            assert gap_to_fill.size > 0, "incorrect size"
            # Change file to move
            file_to_move = file_to_move.prev_node.prev_node
            assert file_to_move.is_file
            # Drop the node and the gap before it
            file_to_move.prev_node.prev_node.next_node = None
        elif file_to_move.size == gap_to_fill.size:
            print(f"Moving all file {file_to_move.id} to gap of size {gap_to_fill.size}")
            new_node = DiskNode(file_to_move.id, file_to_move.size, True, file_before_gap, gap_to_fill.next_node)
            file_before_gap.next_node = new_node
            gap_to_fill.next_node.prev_node = new_node
            # Change file_to_move and drop the node and the gap before it
            file_to_move = file_to_move.prev_node.prev_node
            file_to_move.next_node = None
            # Move to next gap to fill
            gap_to_fill = gap_to_fill.next_node.next_node
            assert not gap_to_fill.is_file
        elif file_to_move.size > gap_to_fill.size:
            print(f"Moving part of file {file_to_move.id} (size {file_to_move.size}) to gap of size {gap_to_fill.size}")
            new_node = DiskNode(file_to_move.id, gap_to_fill.size, True, file_before_gap, gap_to_fill.next_node)
            file_before_gap.next_node = new_node
            gap_to_fill.next_node.prev_node = new_node
            file_to_move.size -= gap_to_fill.size
            # Move to next gap to fill
            gap_to_fill = gap_to_fill.next_node.next_node
        else:
            assert False, "Code should never get here!"

    checksum = calc_checksum(first_node)
    print(checksum)

if __name__ == "__main__":
    main()
