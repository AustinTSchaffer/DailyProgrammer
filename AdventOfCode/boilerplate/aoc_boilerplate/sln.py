import re
import dataclasses
import time
from typing import Any

# @dataclasses.dataclass
# class Input:
#     ...

# Input = list

Input = Any

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        ...

def part_1(input: Input):
    ...

def part_2(input: Input):
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    before = time.time_ns()
    result = part_1(sample_input)
    time_ms = (time.time_ns() - before) / 1000

    print('Part 1 (sample):', result, f'({time_ms} ms)')

    before = time.time_ns()
    result = part_1(input)
    time_ms = (time.time_ns() - before) / 1000

    print('Part 1:', result, f'({time_ms} ms)')

    before = time.time_ns()
    result = part_2(sample_input)
    time_ms = (time.time_ns() - before) / 1000

    print('Part 2 (sample):', result, f'({time_ms} ms)')

    before = time.time_ns()
    result = part_2(input)
    time_ms = (time.time_ns() - before) / 1000

    print('Part 2:', result, f'({time_ms} ms)')
