import re
import dataclasses
import time
from typing import Any
import itertools

# @dataclasses.dataclass
# class Input:
#     ...

# Input = list

Input = list[list[int]]

def parse_input(filename: str) -> Input:
    output = []
    with open(filename, 'r') as f:
        for line in f:
            output.append([int(v) for v in line.strip().split()])
    return output

def is_safe_report(report: list[int]) -> bool:
    increasing = report[1] > report[0]

    for a, b in itertools.pairwise(report):
        diff = b - a

        if diff == 0:
            return False

        if diff > 3 or diff < -3:
            return False

        if (diff > 0 and not increasing) or (diff < 0 and increasing):
            return False

    return True

def is_safe_report_2(report: list[int]) -> bool:
    if is_safe_report(report):
        return True

    for idx in range(len(report)):
        report_cpy = report.copy()
        del report_cpy[idx]
        if is_safe_report(report_cpy):
            return True

    return False


def part_1(input: Input):
    safe_reports = 0
    for line in input:
        if is_safe_report(line):
            safe_reports += 1
    return safe_reports

def part_2(input: Input):
    safe_reports = 0
    for line in input:
        if is_safe_report_2(line):
            safe_reports += 1
    return safe_reports

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    before = time.time_ns()
    result = part_1(sample_input)
    _time = (time.time_ns() - before) / 1000

    print('Part 1 (sample):', result, f'({_time:.3} ms)')

    before = time.time_ns()
    result = part_1(input)
    _time = (time.time_ns() - before) / 1000

    print('Part 1:', result, f'({_time:.3} ms)')

    before = time.time_ns()
    result = part_2(sample_input)
    _time = (time.time_ns() - before) / 1000

    print('Part 2 (sample):', result, f'({_time:.3} ms)')

    before = time.time_ns()
    result = part_2(input)
    _time = (time.time_ns() - before) / 1000

    print('Part 2:', result, f'({_time:.3} ms)')
