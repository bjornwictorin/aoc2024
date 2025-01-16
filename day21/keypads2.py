#! /usr/bin/env python3

NUM_DIR_ROBOTS = 2


def parse_input(filename):
    data = open(filename, "r")
    codes = []
    for line in data:
        codes.append(line.rstrip())
    return codes


# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
def get_num_pad_pos(digit):
    if digit == "7":
        return (0, 0)
    elif digit == "8":
        return (0, 1)
    elif digit == "9":
        return (0, 2)
    elif digit == "4":
        return (1, 0)
    elif digit == "5":
        return (1, 1)
    elif digit == "6":
        return (1, 2)
    elif digit == "1":
        return (2, 0)
    elif digit == "2":
        return (2, 1)
    elif digit == "3":
        return (2, 2)
    elif digit == "0":
        return (3, 1)
    elif digit == "A":
        return (3, 2)
    else:
        assert False, f"invalid digit: {digit}"

def get_num_pad_symbol(row, col):
    if row == 0:
        if col == 0:
            return "7"
        elif col == 1:
            return "8"
        elif col == 2:
            return "9"
    elif row == 1:
        if col == 0:
            return "4"
        elif col == 1:
            return "5"
        elif col == 2:
            return "6"
    elif row == 2:
        if col == 0:
            return "1"
        elif col == 1:
            return "2"
        elif col == 2:
            return "3"
    elif row == 3:
        if col == 1:
            return "0"
        elif col == 2:
            return "A"
    assert False, f"invalid (row, col): ({row}, {col})"

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
def get_dir_pad_pos(button):
    if button == "^":
        return (0, 1)
    elif button == "A":
        return (0, 2)
    elif button == "<":
        return (1, 0)
    elif button == "v":
        return (1, 1)
    elif button == ">":
        return (1, 2)
    else:
        assert False, f"invalid button: {button}"

def get_dir_pad_symbol(row, col):
    if row == 0:
        if col == 1:
            return "^"
        elif col == 2:
            return "A"
    elif row == 1:
        if col == 0:
            return "<"
        elif col == 1:
            return "v"
        elif col == 2:
            return ">"
    assert False, f"invalid (row, col): ({row}, {col})"


def is_valid_num_robot(pos):
    y, x = pos
    if x < 0 or x > 2 or y < 0 or y > 3 or (x == 0 and y == 3):
        return False
    return True

def is_valid_dir_robot(pos):
    y, x = pos
    if x < 0 or x > 2 or y < 0 or y > 1 or (x == 0 and y == 0):
        return False
    return True


def calc_next_state(init_state, button):
    """Return state after pressing button. If state is invalid return None"""
    state = list(init_state)
    for ii in range(NUM_DIR_ROBOTS):
        # print(button)
        y, x = state[ii]
        if button == "A":
            # button = state.dir_robots[ii].symbol
            button = get_dir_pad_symbol(y, x)
        else:
            if button == ">":
                state[ii] = (y, x + 1)
            elif button == "v":
                state[ii] = (y + 1, x)
            elif button == "<":
                state[ii] = (y, x - 1)
            elif button == "^":
                state[ii] = (y - 1, x)
            else:
                assert False, f"invalid button: {button}"
            if is_valid_dir_robot(state[ii]):
                return tuple(state)
            else:
                # print(f"invalid dir robot: {state.dir_robots[ii]}")
                return None

    # update num_robot
    if button != "A":
        # to_y, to_x = get_num_pad_pos(to_digit)
        num_robot_y, num_robot_x = state[-1]
        if button == ">": # and num_robot_x < to_x:
            state[-1] = (num_robot_y, num_robot_x + 1)
        elif button == "v": # and num_robot_y < to_y:
            state[-1] = (num_robot_y + 1, num_robot_x)
        elif button == "<": # and num_robot_x > to_x:
            state[-1] = (num_robot_y, num_robot_x - 1)
        elif button == "^": # and num_robot_y > to_y:
            state[-1] = (num_robot_y - 1, num_robot_x)
        else:
            return None
            # assert False, f"invalid button: {button}"
    if is_valid_num_robot(state[-1]):
        return tuple(state)
    else:
        # print(f"invalid num robot: {state.num_robot}")
        return None


def calc_transition_len(from_digit, to_digit):
    """Use BFS to find shortest sequence which leads to pressing to_digit"""
    from_digit_y, from_digit_x = get_num_pad_pos(from_digit)
    initial_state = tuple(((0, 2) if ii < NUM_DIR_ROBOTS else (from_digit_y, from_digit_x)) for ii in range(NUM_DIR_ROBOTS + 1))
    current_states = [initial_state]
    visited_states = set()
    num_steps = 0
    while True:
        num_steps += 1
        next_states = []
        for state in current_states:
            if all(dir_robot == (0, 2) for dir_robot in state[:-1]) and state[-1] == get_num_pad_pos(to_digit):
                # print(num_steps)
                return num_steps
            # create new next states by pressing all buttons on remote control
            for button in "^A<v>":
                next_state = calc_next_state(state, button)
                if next_state and tuple(next_state) not in visited_states:
                    next_states.append(next_state)
                    visited_states.add(tuple(next_state))
        current_states = next_states


def calc_seq_len(code):
    seq_len = 0
    for ii in range(len(code)):
        from_digit = "A" if ii == 0 else code[ii - 1]
        to_digit = code[ii]
        seq_len += calc_transition_len(from_digit, to_digit)
        # print(".", end="", flush=True)
    return seq_len


def main():
    codes = parse_input("input.txt")
    values = [int(x[:-1]) for x in codes]
    seq_lengths = []

    for code in codes:
        print(code)
        seq_lengths.append(calc_seq_len(code))

    complexities = [value * length for value, length in zip(values, seq_lengths)]
    print(sum(complexities))


if __name__ == "__main__":
    main()
