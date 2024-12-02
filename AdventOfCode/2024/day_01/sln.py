import re
import dataclasses
import time
from typing import Any

Input = list[tuple[int, int]]

def parse_input(filename: str) -> Input:
    output = []
    with open(filename, 'r') as f:
        for line in f:
            a, b = line.strip().split('   ')
            output.append((int(a), int(b)))
    return output

def part_1(input: Input):
    list_1 = sorted([r[0] for r in input])
    list_2 = sorted([r[1] for r in input])
    return sum(
        abs(a - b)
        for a, b in zip(list_1, list_2)
    )

def part_2(input: Input):
    counted = {}
    for _, v in input:
        count = counted.get(v, 0)
        counted[v] = count + 1

    return sum(
        counted.get(v, 0) * v
        for v, _ in input
    )

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
