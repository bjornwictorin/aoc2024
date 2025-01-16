#! /usr/bin/env python3

from copy import deepcopy
from typing import Optional, List

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


class KeypadRobot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"""
robot_pos: ({self.y}, {self.x})"""
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class DirRobot(KeypadRobot):
    def __init__(self, x=2, y=0):
        super().__init__(x, y)

    def is_valid(self):
        if self.x < 0 or self.x > 2 or \
           self.y < 0 or self.y > 1 or \
           (self.x == 0 and self.y == 0):
            return False
        return True
    
    @property
    def symbol(self):
        return get_dir_pad_symbol(self.y, self.x)

class NumRobot(KeypadRobot):
    def __init__(self, x=2, y=3):
        super().__init__(x, y)

    def is_valid(self):
        if self.x < 0 or self.x > 2 or \
           self.y < 0 or self.y > 3 or \
           (self.x == 0 and self.y == 3):
            return False
        return True
    
    @property
    def symbol(self):
        return get_num_pad_symbol(self.y, self.x)


class RobotState:
    def __init__(self, num_robot_x=2, num_robot_y=3):
        self.dir_robots: List[DirRobot] = []
        for _ in range(NUM_DIR_ROBOTS):
            self.dir_robots.append(DirRobot())
        self.num_robot = NumRobot(x=num_robot_x, y=num_robot_y)
        self.done = False
    
    def all_dir_robots_on_a(self):
        return all(robot.symbol == "A" for robot in self.dir_robots)
    
    def __repr__(self):
        return str(self.dir_robots[0]) + str(self.dir_robots[1]) + str(self.num_robot) + "\n" + self.num_robot.symbol
    
    def __eq__(self, other):
        return self.num_robot == other.num_robot and \
            all(x == y for x, y in zip(self.dir_robots, other.dir_robots))


def calc_next_state(initial_state: RobotState, button) -> Optional[RobotState]:
    """Return state after pressing button. If state is invalid return None"""
    # print("---")
    state: RobotState = deepcopy(initial_state)
    for ii in range(NUM_DIR_ROBOTS):
        # print(button)
        if button == "A":
            button = state.dir_robots[ii].symbol
        else:
            if button == ">":
                state.dir_robots[ii].x += 1
            elif button == "v":
                state.dir_robots[ii].y += 1
            elif button == "<":
                state.dir_robots[ii].x -= 1
            elif button == "^":
                state.dir_robots[ii].y -= 1
            else:
                assert False, f"invalid button: {button}"
            if state.dir_robots[ii].is_valid():
                return state
            else:
                # print(f"invalid dir robot: {state.dir_robots[ii]}")
                return None

    # update num_robot
    if button == "A":
        # if we get here all dir_robots pointed on A
        assert initial_state.all_dir_robots_on_a(), f"{initial_state}"
        state.done = True
    else:
        if button == ">":
            state.num_robot.x += 1
        elif button == "v":
            state.num_robot.y += 1
        elif button == "<":
            state.num_robot.x -= 1
        elif button == "^":
            state.num_robot.y -= 1
        else:
            assert False, f"invalid button: {button}"
    if state.num_robot.is_valid():
        return state
    else:
        # print(f"invalid num robot: {state.num_robot}")
        return None


def calc_transition_len(from_digit, to_digit):
    """Use BFS to find shortest sequence which leads to pressing to_digit"""
    from_digit_pos = get_num_pad_pos(from_digit)
    initial_state = RobotState(num_robot_x=from_digit_pos[1], num_robot_y=from_digit_pos[0])
    current_states = [initial_state]
    visited_states = []
    num_steps = 0
    while True:
        num_steps += 1
        next_states = []
        for state in current_states:
            if state.all_dir_robots_on_a() and state.num_robot.symbol == to_digit:
                return num_steps
            # create new next states by pressing all buttons on remote control
            for button in "^A<v>":
                next_state = calc_next_state(state, button)
                if next_state and next_state not in visited_states:
                    next_states.append(next_state)
                    visited_states.append(next_state)
        current_states = next_states


def calc_seq_len(code):
    seq_len = 0
    for ii in range(len(code)):
        from_digit = "A" if ii == 0 else code[ii - 1]
        to_digit = code[ii]
        seq_len += calc_transition_len(from_digit, to_digit)
        print(".", end="", flush=True)
    return seq_len


def main():
    codes = parse_input("input.txt")
    values = [int(x[:-1]) for x in codes]
    seq_lengths = []

    for code in codes:
        print(code, end="", flush=True)
        seq_lengths.append(calc_seq_len(code))
        print()

    complexities = [value * length for value, length in zip(values, seq_lengths)]
    print(sum(complexities))


if __name__ == "__main__":
    main()
