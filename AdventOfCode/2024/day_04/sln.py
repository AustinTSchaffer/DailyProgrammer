import re
import dataclasses
import time
from typing import Any

@dataclasses.dataclass
class Input:
    grid: list[str]
    width: int
    height: int

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        grid = [
            line.strip()
            for line in
            f.readlines()
            if line
        ]

    return Input(
        grid=grid,
        height=len(grid),
        width=len(grid[0])
    )

def word_at_position_and_direction(input: Input, i: int, j: int, vector: tuple[int, int], word='XMAS') -> bool:
    max_i = (vector[0] * (len(word) - 1)) + i
    if 0 > max_i or max_i >= input.height:
        return False

    max_j = (vector[1] * (len(word) - 1)) + j
    if 0 > max_j or max_j >= input.width:
        return False

    for letter_idx, letter in enumerate(word):
        if letter != input.grid[i+(vector[0]*letter_idx)][j+(vector[1]*letter_idx)]:
            return False

    return True

def word_count_at_position(input, i, j, word='XMAS') -> int:
    count = 0
    for i_dir in (-1, 0, +1):
        for j_dir in (-1, 0, +1):
            if (i_dir or j_dir) and word_at_position_and_direction(input, i, j, (i_dir, j_dir)):
                count += 1
    return count

def part_1(input: Input):
    return sum(
        word_count_at_position(input, i, j)
        for i in range(input.height)
        for j in range(input.width)
    )

def part_2(input: Input):
    count = 0
    for i in range(1, input.height - 1):
        for j in range(1, input.width - 1):
            if input.grid[i][j] != 'A':
                continue

            diag_tlbr = (input.grid[i-1][j-1], input.grid[i+1][j+1])
            if diag_tlbr != ('M', 'S') and diag_tlbr != ('S', 'M'):
                continue

            diag_bltr = (input.grid[i+1][j-1], input.grid[i-1][j+1])
            if diag_bltr != ('M', 'S') and diag_bltr != ('S', 'M'):
                continue

            count += 1

    return count


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
