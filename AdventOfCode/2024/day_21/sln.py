import re
import dataclasses
import time
from typing import Any, Literal, Iterable
import astar

Input = list[str]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        return [
            line.strip()
            for line in f
            if line
        ]

DPadButton = Literal['^', 'v', '<', '>', 'A']
CodePadButton = Literal['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A']

DPAD_BUTTONS: list[DPadButton] = '^A<v>'

D_PAD: list[list[None | DPadButton]] = [
    [None, '^', 'A'],
    ['<', 'v', '>'],
]

D_PAD_INDEX: dict[DPadButton, tuple[int, int]] = {
    button: (i, j)
    for i, row in enumerate(D_PAD)
    for j, button in enumerate(row)
    if button is not None
}

CODE_PAD = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A'],
]

CODE_PAD_INDEX: dict[CodePadButton, tuple[int, int]] = {
    button: (i, j)
    for i, row in enumerate(CODE_PAD)
    for j, button in enumerate(row)
    if button is not None
}

State = tuple[DPadButton | None, DPadButton, DPadButton, CodePadButton]

def get_dpad_button(location: tuple[int, int]) -> DPadButton | None:
    in_bounds = (
        location[0] >= 0 and
        location[0] < len(D_PAD) and
        location[1] >= 0 and
        location[1] < len(D_PAD[0])
    )

    if not in_bounds:
        return None

    return D_PAD[location[0]][location[1]]

def get_code_pad_button(location: tuple[int, int]) -> CodePadButton | None:
    in_bounds = (
        location[0] >= 0 and
        location[0] < len(CODE_PAD) and
        location[1] >= 0 and
        location[1] < len(CODE_PAD[0])
    )

    if not in_bounds:
        return None

    return CODE_PAD[location[0]][location[1]]

def simulate_button_press(*, button: DPadButton, button_pad_index: int = 1, state: State) -> State | None:
    is_last_button_pad = (button_pad_index == (len(state) - 1))

    pad_button_loc_curr = (
        CODE_PAD_INDEX[state[button_pad_index]]
        if is_last_button_pad else
        D_PAD_INDEX[state[button_pad_index]]
    )

    if button == '<':
        pad_button_loc_next = (pad_button_loc_curr[0], pad_button_loc_curr[1] - 1)
    elif button == '>':
        pad_button_loc_next = (pad_button_loc_curr[0], pad_button_loc_curr[1] + 1)
    elif button == 'v':
        pad_button_loc_next = (pad_button_loc_curr[0] + 1, pad_button_loc_curr[1])
    elif button == '^':
        pad_button_loc_next = (pad_button_loc_curr[0] - 1, pad_button_loc_curr[1])
    elif button == 'A' and not is_last_button_pad:
        return simulate_button_press(button=state[button_pad_index], button_pad_index=button_pad_index+1, state=state)
    elif button == 'A' and is_last_button_pad:
        return state

    if is_last_button_pad and (button := get_code_pad_button(pad_button_loc_next)) is not None:
        new_state = list(state)
        new_state[button_pad_index] = button
        return tuple(new_state)
    elif not is_last_button_pad and (button := get_dpad_button(pad_button_loc_next)) is not None:
        new_state = list(state)
        new_state[button_pad_index] = button
        return tuple(new_state)

    return None

def determine_neighbors(state: State) -> Iterable[State]:
    for option in DPAD_BUTTONS:
        result = simulate_button_press(button=option, state=tuple([option, *state[1:]]))
        if result is not None:
            yield result

def distance_to_goal(state: State, goal: State) -> int:
    dist = 0
    for s, g in zip(state[1:-1], goal[1:-1]):
        dist += (
            abs(D_PAD_INDEX[s][0] - D_PAD_INDEX[g][0]) +
            abs(D_PAD_INDEX[s][1] - D_PAD_INDEX[g][1])
        )

    dist += (
        abs(CODE_PAD_INDEX[state[-1]][0] - CODE_PAD_INDEX[goal[-1]][0]) +
        abs(CODE_PAD_INDEX[state[-1]][1] - CODE_PAD_INDEX[goal[-1]][1])
    )

    return dist

def find_efficient_path(code: str, num_robot_dpads: int = 2) -> Any:
    starts = [(None, *(['A'] * num_robot_dpads), 'A')]
    for char in code[:-1]:
        starts.append(('A', *(['A'] * num_robot_dpads), char))

    goals = [
        ('A', *(['A'] * num_robot_dpads), char)
        for char in code
    ]

    efficient_path = []
    for start, goal in zip(starts, goals):

        path = list(astar.find_path(
            start=start,
            goal=goal,
            neighbors_fnct=determine_neighbors,
            heuristic_cost_estimate_fnct=distance_to_goal,
        ))

        efficient_path.extend(path[1:])

    return efficient_path

def part_1(input: Input):
    result = 0
    for code in input:
        efficient_path = find_efficient_path(code)
        result += int(code[:-1]) * len(efficient_path)
    return result

def part_2(input: Input):
    result = 0
    for code in input:
        efficient_path = find_efficient_path(code, 25)
        result += int(code[:-1]) * len(efficient_path)
    return result

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    before = time.time_ns()
    result = part_1(sample_input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1 (sample):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_1(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1:', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(sample_input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2 (sample):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2:', result, f'({_time} ms)')
