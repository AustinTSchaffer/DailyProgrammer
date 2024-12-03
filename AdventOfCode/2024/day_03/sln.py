import re
import dataclasses
import time
from typing import Any

# @dataclasses.dataclass
# class Input:
#     ...

# Input = list

Input = str

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        return f.read()

def part_1(input: Input):
    matches = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', input)
    sum_ = 0
    for match in matches:
        assert len(match) == 2
        sum_ += int(match[0]) * int(match[1])
    return sum_

def part_2(input: Input):
    matches = re.findall(r'(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))', input)

    enabled = True
    sum_ = 0
    for match in matches:
        assert len(match) == 3
        if match[0] == 'do()':
            enabled = True
        elif match[0] == 'don\'t()':
            enabled = False
        elif enabled:
            sum_ += int(match[1]) * int(match[2])
    return sum_

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
