import re
import dataclasses
import time
from typing import Any


@dataclasses.dataclass
class Farm:
    grid: list[list[str]]
    height: int
    width: int


def parse_input(filename: str) -> Farm:
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            grid_row = []
            grid.append(grid_row)
            for char in line:
                grid_row.append(char)
    return Farm(
        grid=grid,
        height=len(grid),
        width=len(grid[0]),
    )


@dataclasses.dataclass
class Region:
    classification: str
    locations: set[tuple[int, int]]
    area: int
    perimeter_segments: list[tuple[tuple[int, int], tuple[int, int]]]
    perimeter: int


def in_bounds(position: tuple[int, int], farm: Farm) -> bool:
    return (
        position[0] >= 0 and position[0] < farm.height and
        position[1] >= 0 and position[1] < farm.width
    )


def determine_region(seed: tuple[int, int], farm: Farm) -> Region:
    region_class = farm.grid[seed[0]][seed[1]]
    perimeter_segments = []
    perimeter = 0
    locations = set()
    frontier = [seed]
    while frontier:
        position = frontier.pop()
        locations.add(position)
        for dir, vec in [('U', (-1, 0)), ('D', (+1, 0)), ('L', (0, -1)), ('R', (0, +1))]:
            neighbor = (
                position[0] + vec[0],
                position[1] + vec[1],
            )

            if not in_bounds(neighbor, farm):
                perimeter += 1
                perimeter_segments.append((
                    (),
                    (),
                ))
            elif (neighbor in locations) or (neighbor in frontier):
                ...
            elif farm.grid[neighbor[0]][neighbor[1]] == region_class:
                frontier.append(neighbor)
            else:
                perimeter += 1
                perimeter_segments.append(None)


    return Region(
        classification=region_class,
        locations=locations,
        area=len(locations),
        perimeter=perimeter,
    )


def part_1(farm: Farm):
    sum_ = 0
    nodes_considered = set()
    for i in range(farm.height):
        for j in range(farm.width):
            node = (i, j)
            if node in nodes_considered:
                continue
            region = determine_region(node, farm)
            nodes_considered = set.union(nodes_considered, region.locations)
            sum_ += region.area * region.perimeter
    return sum_

def part_2(input: Farm):
    ...

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
