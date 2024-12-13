import re
import dataclasses
import time
from typing import Any

Input = list[int]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        return list(map(int, f.read().split(' ')))

# def part_1(input: Input):
#     stones = input
#     stones_next = []
#     for _ in range(25):
#         for stone in stones:
#             if stone == 0:
#                 stones_next.append(1)
#                 continue
#             stone_str = str(stone)
#             len_stone_str = len(stone_str)
#             if len_stone_str % 2 == 0:
#                 stones_next.append(int(stone_str[:(len_stone_str//2)]))
#                 stones_next.append(int(stone_str[(len_stone_str//2):]))
#                 continue
#             stones_next.append(stone * 2024)
#         stones = stones_next
#         stones_next = []
#     return len(stones)

_num_stones_created_cache: dict[tuple[int, int], int] = {}
def num_stones_created(stone: int, iterations_remaining: int):
    if iterations_remaining <= 0:
        return 1

    if existing_result := _num_stones_created_cache.get((stone, iterations_remaining)):
        return existing_result

    if stone == 0:
        result = num_stones_created(1, iterations_remaining - 1)
        _num_stones_created_cache[(stone, iterations_remaining)] = result
        return result

    stone_str = str(stone)
    len_stone_str = len(stone_str)
    if len_stone_str % 2 == 0:
        result = (
            num_stones_created(int(stone_str[:(len_stone_str//2)]), iterations_remaining - 1) + 
            num_stones_created(int(stone_str[(len_stone_str//2):]), iterations_remaining - 1)
        )
        _num_stones_created_cache[(stone, iterations_remaining)] = result
        return result

    result = num_stones_created(stone * 2024, iterations_remaining - 1)
    _num_stones_created_cache[(stone, iterations_remaining)] = result
    return result


def part_1(input: Input):
    result = 0
    for stone in input:
        result += num_stones_created(stone, 25)
    return result


def part_2(input: Input):
    result = 0
    for stone in input:
        result += num_stones_created(stone, 75)
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
