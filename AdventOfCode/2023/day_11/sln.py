import re
import dataclasses
import itertools

@dataclasses.dataclass
class Input:
    height: int
    empty_rows: list[int]
    width: int
    empty_cols: list[int]
    raw_galaxy_locations: list[tuple[int, int]]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        space_map = [
            line.strip()
            for line in f.read().strip().split('\n')
        ]

    height = len(space_map)
    width = len(space_map[0])

    occupied_rows = [False] * height
    occupied_cols = [False] * width

    galaxies_raw = []
    for i, row in enumerate(space_map):
        for j, val in enumerate(row):
            if val == '#':
                occupied_rows[i] = True
                occupied_cols[j] = True
                galaxies_raw.append((i, j))

    return Input(
        height=height,
        empty_rows=[
            i for i in range(height) if not occupied_rows[i]
        ],
        width=width,
        empty_cols=[
            j for j in range(width) if not occupied_cols[j]
        ],
        raw_galaxy_locations=galaxies_raw,
    )


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(b[1] - a[1]) + abs(b[0] - a[0])


def part_1(input: Input):
    actual_galaxy_locations = []
    for x, y in input.raw_galaxy_locations:
        x += sum(1 for row in input.empty_rows if row < x)
        y += sum(1 for col in input.empty_cols if col < y)
        actual_galaxy_locations.append((x, y))

    sum_ = 0
    pairs = 0
    for g1, g2 in itertools.combinations(actual_galaxy_locations, 2):
        sum_ += manhattan(g1, g2)
        pairs += 1
    return sum_

def part_2(input: Input, factor_increase=1000000):
    actual_galaxy_locations = []
    for x, y in input.raw_galaxy_locations:
        x += sum(factor_increase-1 for row in input.empty_rows if row < x)
        y += sum(factor_increase-1 for col in input.empty_cols if col < y)
        actual_galaxy_locations.append((x, y))

    sum_ = 0
    pairs = 0
    for g1, g2 in itertools.combinations(actual_galaxy_locations, 2):
        sum_ += manhattan(g1, g2)
        pairs += 1
    return sum_


if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample, *10):', part_2(sample_input, 10))
    print('Part 2 (sample, *100):', part_2(sample_input, 100))
    print('Part 2:', part_2(input))
