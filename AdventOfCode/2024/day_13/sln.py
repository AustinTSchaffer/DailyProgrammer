import re
import dataclasses
import time
from typing import Any
import itertools
import z3

@dataclasses.dataclass
class ClawMachine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

ClawMachines = list[ClawMachine]

def parse_input(filename: str) -> ClawMachines:
    with open(filename, 'r') as f:
        data = f.read().strip()

    claw_machine_re = re.compile(r'Button A: X\+(?P<button_a_x>\d+), Y\+(?P<button_a_y>\d+)\nButton B: X\+(?P<button_b_x>\d+), Y\+(?P<button_b_y>\d+)\nPrize: X=(?P<prize_x>\d+), Y=(?P<prize_y>\d+)')

    output = []
    for match in claw_machine_re.finditer(data):
        output.append(ClawMachine(
            button_a=(
                int(match['button_a_x']),
                int(match['button_a_y']),
            ),
            button_b=(
                int(match['button_b_x']),
                int(match['button_b_y']),
            ),
            prize=(
                int(match['prize_x']),
                int(match['prize_y']),
            ),
        ))

    return output


def get_cost_to_goal(claw_machine: ClawMachine, button_a_cost = 3, button_b_cost = 1, prize_offset = 0) -> int | None:
    o = z3.Optimize()
    A_n = z3.Int('A_n')
    B_n = z3.Int('B_n')
    Cost = z3.Int('Cost')

    o.add(z3.And(
        (A_n * claw_machine.button_a[0]) + (B_n * claw_machine.button_b[0]) == (claw_machine.prize[0] + prize_offset),
        (A_n * claw_machine.button_a[1]) + (B_n * claw_machine.button_b[1]) == (claw_machine.prize[1] + prize_offset),
        0 <= A_n,
        0 <= B_n,
        (button_a_cost * A_n) + (button_b_cost * B_n) == Cost
    ))

    o.minimize(Cost)
    if o.check() != z3.sat:
        return None

    return o.model()[Cost].as_long()


def part_1(cms: ClawMachines):
    total_cost = 0
    for cm in cms:
        if (cost := get_cost_to_goal(cm)) is not None:
            total_cost += cost
    return total_cost

def part_2(cms: ClawMachines):
    total_cost = 0
    for cm in cms:
        if (cost := get_cost_to_goal(cm, prize_offset=10000000000000)) is not None:
            total_cost += cost
    return total_cost

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
