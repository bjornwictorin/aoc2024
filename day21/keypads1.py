#! /usr/bin/env python3


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

class robot_state:    
    def __init__(self, dir_robot0_x=2, dir_robot0_y=0, dir_robot1_x=2, dir_robot1_y=0, num_robot_x=2, num_robot_y=3):
        self.dir_robot0_x = dir_robot0_x
        self.dir_robot0_y = dir_robot0_y
        self.dir_robot1_x = dir_robot1_x
        self.dir_robot1_y = dir_robot1_y
        self.num_robot_x = num_robot_x
        self.num_robot_y = num_robot_y

    def is_valid(self):
        if self.dir_robot0_x < 0 or self.dir_robot0_x > 2 or  self.dir_robot0_y < 0 or self.dir_robot0_y > 1 or \
            self.dir_robot1_x < 0 or self.dir_robot1_x > 2 or  self.dir_robot1_y < 0 or self.dir_robot1_y > 1 or \
            self.num_robot_x < 0 or self.num_robot_x > 2 or  self.num_robot_y < 0 or self.num_robot_y > 3:
            return False
        # handle the special invalid cases (0, 0) for dir and (3, 0) for num
        if self.dir_robot0_x == 0 and self.dir_robot0_y == 0 or \
            self.dir_robot1_x == 0 and self.dir_robot1_y == 0 or \
            self.num_robot_x == 0 and self.num_robot_y == 3:
            return False
        return True
    
    @property
    def dir_robot0_symbol(self):
        return get_dir_pad_symbol(self.dir_robot0_y, self.dir_robot0_x)
    
    @property
    def dir_robot1_symbol(self):
        return get_dir_pad_symbol(self.dir_robot1_y, self.dir_robot1_x)
    
    @property
    def num_robot_symbol(self):
        return get_num_pad_symbol(self.num_robot_y, self.num_robot_x)

    def __repr__(self):
        return f"""
        dir_robot0_pos: ({self.dir_robot0_y}, {self.dir_robot0_x}), symbol: {self.dir_robot0_symbol}
        dir_robot1_pos: ({self.dir_robot1_y}, {self.dir_robot1_x}), symbol: {self.dir_robot1_symbol}
        num_robot_pos: ({self.num_robot_y}, {self.num_robot_x}), symbol: {self.num_robot_symbol}"""

    def __eq__(self, other):
        return self.dir_robot0_x == other.dir_robot0_x and self.dir_robot0_y == other.dir_robot0_y and \
            self.dir_robot1_x == other.dir_robot1_x and self.dir_robot1_y == other.dir_robot1_y and \
            self.num_robot_x == other.num_robot_x and self.num_robot_y == other.num_robot_y

def calc_next_state(state: robot_state, button):
    if button == ">":
        return robot_state(state.dir_robot0_x + 1, state.dir_robot0_y,
                           state.dir_robot1_x, state.dir_robot1_y,
                           state.num_robot_x, state.num_robot_y)
    elif button == "v":
        return robot_state(state.dir_robot0_x, state.dir_robot0_y + 1,
                           state.dir_robot1_x, state.dir_robot1_y,
                           state.num_robot_x, state.num_robot_y)
    elif button == "<":
        return robot_state(state.dir_robot0_x - 1, state.dir_robot0_y,
                           state.dir_robot1_x, state.dir_robot1_y,
                           state.num_robot_x, state.num_robot_y)
    elif button == "^":
        return robot_state(state.dir_robot0_x, state.dir_robot0_y - 1,
                           state.dir_robot1_x, state.dir_robot1_y,
                           state.num_robot_x, state.num_robot_y)
    elif button == "A":
        if state.dir_robot0_symbol == ">":
            return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                               state.dir_robot1_x + 1, state.dir_robot1_y,
                               state.num_robot_x, state.num_robot_y)
        elif state.dir_robot0_symbol == "v":
            return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                               state.dir_robot1_x, state.dir_robot1_y + 1,
                               state.num_robot_x, state.num_robot_y)
        elif state.dir_robot0_symbol == "<":
            return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                               state.dir_robot1_x - 1, state.dir_robot1_y,
                               state.num_robot_x, state.num_robot_y)
        elif state.dir_robot0_symbol == "^":
            return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                               state.dir_robot1_x, state.dir_robot1_y - 1,
                               state.num_robot_x, state.num_robot_y)
        elif state.dir_robot0_symbol == "A":
            if state.dir_robot1_symbol == ">":
                return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                                   state.dir_robot1_x, state.dir_robot1_y,
                                   state.num_robot_x + 1, state.num_robot_y)
            elif state.dir_robot1_symbol == "v":
                return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                                   state.dir_robot1_x, state.dir_robot1_y,
                                   state.num_robot_x, state.num_robot_y + 1)
            elif state.dir_robot1_symbol == "<":
                return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                                   state.dir_robot1_x, state.dir_robot1_y,
                                   state.num_robot_x - 1, state.num_robot_y)
            elif state.dir_robot1_symbol == "^":
                return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                                   state.dir_robot1_x, state.dir_robot1_y,
                                   state.num_robot_x, state.num_robot_y - 1)
            elif state.dir_robot1_symbol == "A":
                # no update
                return robot_state(state.dir_robot0_x, state.dir_robot0_y,
                                   state.dir_robot1_x, state.dir_robot1_y,
                                   state.num_robot_x, state.num_robot_y)

    assert False, f"invalid button: {button} (state: {state})"


def calc_transition_len(from_digit, to_digit):
    """Use BFS to find shortest sequence which leads to pressing to_digit"""
    # print(f"from: {from_digit}, to: {to_digit}")
    # initially robot0 points at A and robot1 points at from_digit
    from_digit_pos = get_num_pad_pos(from_digit)
    initial_state = robot_state(num_robot_x=from_digit_pos[1], num_robot_y=from_digit_pos[0])
    current_states = [initial_state]
    visited_states = []
    # print(current_states)
    num_steps = 0
    while True:
        num_steps += 1
        next_states = []
        for state in current_states:
            if state.dir_robot0_symbol == "A" and state.dir_robot1_symbol == "A" and state.num_robot_symbol == to_digit:
                return num_steps
            # create new next states by pressing all buttons on remote control
            for button in "^A<v>":
                next_state = calc_next_state(state, button)
                if next_state.is_valid() and next_state not in visited_states:
                    next_states.append(next_state)
                    visited_states.append(next_state)
        current_states = next_states
            

def calc_seq_len(code):
    seq_len = 0
    for ii in range(len(code)):
        from_digit = "A" if ii == 0 else code[ii - 1]
        to_digit = code[ii]
        seq_len += calc_transition_len(from_digit, to_digit)
    return seq_len


def main():
    codes = parse_input("input.txt")
    values = [int(x[:-1]) for x in codes]
    seq_lengths = []

    for code in codes:
        seq_lengths.append(calc_seq_len(code))

    complexities = [value * length for value, length in zip(values, seq_lengths)]
    print(sum(complexities))


if __name__ == "__main__":
    main()
