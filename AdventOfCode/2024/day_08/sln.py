import re
import dataclasses
import time
from typing import Any
import itertools

@dataclasses.dataclass
class Input:
    antennas: dict[str, list[tuple[int, int]]]
    width: int
    height: int

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = [
            line.strip()
            for line in f.readlines()
            if line.strip()
        ]
    height = len(data)
    width = len(data[0])
    antennas: dict[str, list[tuple[int, int]]] = {}
    for i in range(height):
        for j in range(width):
            antenna_class = data[i][j]

            if antenna_class == '.':
                continue

            loc = (i, j)
            if (antenna_locs := antennas.get(antenna_class)):
                antenna_locs.append(loc)
            else:
                antennas[antenna_class] = [loc]
    return Input(
        antennas=antennas,
        width=width,
        height=height,
    )

def part_1(input: Input):
    distinct_inbounds_antinode_locs = set()
    def add(antinode: tuple[int, int]):
        if antinode[0] >= 0 and antinode[0] < input.height and antinode[1] >= 0 and antinode[1] < input.width:
            distinct_inbounds_antinode_locs.add(antinode)

    for antenna_class, locations in input.antennas.items():
        for loc_a, loc_b in itertools.combinations(locations, 2):
            add((loc_a[0] + (loc_a[0] - loc_b[0]), loc_a[1] + (loc_a[1] - loc_b[1])))
            add((loc_b[0] + (loc_b[0] - loc_a[0]), loc_b[1] + (loc_b[1] - loc_a[1])))

    return len(distinct_inbounds_antinode_locs)

def part_2(input: Input):
    distinct_inbounds_antinode_locs = set()
    def add(antinode: tuple[int, int]) -> bool:
        if antinode[0] >= 0 and antinode[0] < input.height and antinode[1] >= 0 and antinode[1] < input.width:
            distinct_inbounds_antinode_locs.add(antinode)
            return True
        return False

    for antenna_class, locations in input.antennas.items():
        for location in locations:
            add(location)

        for loc_a, loc_b in itertools.combinations(locations, 2):
            loc_a_i_offset = loc_a[0] - loc_b[0]
            loc_a_j_offset = loc_a[1] - loc_b[1]
            mult = 1
            while add((loc_a[0] + (mult * loc_a_i_offset), loc_a[1] + (mult * loc_a_j_offset))):
                mult += 1

            loc_b_i_offset = loc_b[0] - loc_a[0]
            loc_b_j_offset = loc_b[1] - loc_a[1]
            mult = 1
            while add((loc_b[0] + (mult * loc_b_i_offset), loc_b[1] + (mult * loc_b_j_offset))):
                mult += 1

    return len(distinct_inbounds_antinode_locs)

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
