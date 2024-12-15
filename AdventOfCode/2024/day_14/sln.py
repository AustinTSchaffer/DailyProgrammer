import re
import dataclasses
import time
from typing import Any

@dataclasses.dataclass
class Robots:
    filename: str
    initial_conditions: list[tuple[int, int, int, int]]
    width: int
    height: int

def parse_input(filename: str) -> Robots:
    with open(filename, 'r') as f:
        data = f.read().strip()

    matcher = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
    ics = []
    max_x = 0
    max_y = 0
    for match in matcher.finditer(data):
        ic = tuple(map(int, match.groups()))
        ics.append(ic)
        max_x = max(max_x, ic[0])
        max_y = max(max_y, ic[1])
    return Robots(
        filename=filename,
        initial_conditions=ics,
        width=max_x+1,
        height=max_y+1,
    )

def part_1(input: Robots):
    current_state = [
        (
            condition[0],
            condition[1],
        )
        for condition in
        input.initial_conditions
    ]
    for _ in range(100):
        next_state = []
        for robot_idx, location in enumerate(current_state):
            next_state.append((
                (location[0] + input.initial_conditions[robot_idx][2]) % input.width,
                (location[1] + input.initial_conditions[robot_idx][3]) % input.height,
            ))
        current_state = next_state

    q1, q2, q3, q4 = 0, 0, 0, 0
    for robot in current_state:
        if (robot[0] < (input.width // 2)) and (robot[1] < (input.height // 2)):
            q1 += 1
        elif (robot[0] < (input.width // 2)) and ((input.height // 2) < robot[1]):
            q3 += 1
        elif ((input.width // 2) < robot[0]) and (robot[1] < (input.height // 2)):
            q2 += 1
        elif ((input.width // 2) < robot[0]) and ((input.height // 2) < robot[1]):
            q4 += 1

    return q1 * q2 * q3 * q4

def print_robots(state: list[tuple[int, int]], width: int, height: int, f = None):
    for y in range(height):
        for x in range(width):
            if (x,y) in state:
                if f is None:
                    print('X', end='')
                else:
                    f.write('X')
            else:
                if f is None:
                    print('.', end='')
                else:
                    f.write('.')
        if f is None:
            print()
        else:
            f.write('\n')

def part_2(input_: Robots):
    repeat_catcher = {}

    current_state = [
        (
            condition[0],
            condition[1],
        )
        for condition in
        input_.initial_conditions
    ]
    generation = 0
    while True:
        cst = tuple(current_state)
        if cst in repeat_catcher:
            break
        else:
            repeat_catcher[tuple(current_state)] = generation
        generation += 1

        next_state = []
        for robot_idx, location in enumerate(current_state):
            next_state.append((
                (location[0] + input_.initial_conditions[robot_idx][2]) % input_.width,
                (location[1] + input_.initial_conditions[robot_idx][3]) % input_.height,
            ))
        current_state = next_state

    with open(f"{input_.filename}.sim", 'w') as f:
        for k, i in repeat_catcher.items():
            f.write(str(i))
            f.write('\n')
            print_robots(k, width=input_.width, height=input_.height, f=f)

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
