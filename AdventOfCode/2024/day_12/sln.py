import re
import dataclasses
import time
from typing import Any, Literal


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


@dataclasses.dataclass(frozen=True)
class PerimeterSegment:
    node_a: tuple[int, int]
    node_b: tuple[int, int]
    containment_dir: Literal['U', 'D', 'L', 'R']

@dataclasses.dataclass
class Region:
    classification: str
    locations: set[tuple[int, int]]
    area: int
    perimeter_segments: list[PerimeterSegment]


def in_bounds(position: tuple[int, int], farm: Farm) -> bool:
    return (
        position[0] >= 0 and position[0] < farm.height and
        position[1] >= 0 and position[1] < farm.width
    )


def determine_region(seed: tuple[int, int], farm: Farm) -> Region:
    region_class = farm.grid[seed[0]][seed[1]]
    perimeter_segments = []
    locations = set()
    frontier = [seed]

    def determine_perimeter_segment(node: tuple[int, int], dir: Literal['U', 'D', 'L', 'R']) -> PerimeterSegment:
        match dir:
            case 'U':
                return PerimeterSegment(
                    node_a=node,
                    node_b=(node[0], node[1] + 1),
                    containment_dir='D',
                )
            case 'D':
                return PerimeterSegment(
                    node_a=(node[0] + 1, node[1]),
                    node_b=(node[0] + 1, node[1] + 1),
                    containment_dir='U',
                )
            case 'L':
                return PerimeterSegment(
                    node_a=node,
                    node_b=(node[0] + 1, node[1]),
                    containment_dir='R',
                )
            case 'R':
                return PerimeterSegment(
                    node_a=(node[0], node[1] + 1),
                    node_b=(node[0] + 1, node[1] + 1),
                    containment_dir='L',
                )
            case _:
                raise ValueError(dir)

    while frontier:
        position = frontier.pop()
        locations.add(position)
        for dir, vec in [('U', (-1, 0)), ('D', (+1, 0)), ('L', (0, -1)), ('R', (0, +1))]:
            neighbor = (
                position[0] + vec[0],
                position[1] + vec[1],
            )

            if not in_bounds(neighbor, farm):
                perimeter_segments.append(determine_perimeter_segment(position, dir))
            elif (neighbor in locations) or (neighbor in frontier):
                ...
            elif farm.grid[neighbor[0]][neighbor[1]] == region_class:
                frontier.append(neighbor)
            else:
                perimeter_segments.append(determine_perimeter_segment(position, dir))

    return Region(
        classification=region_class,
        locations=locations,
        area=len(locations),
        perimeter_segments=perimeter_segments,
    )

def combine_perimeter_segments(region: Region) -> list[tuple[tuple[int, int], tuple[int, int], Literal['H', 'V']]]:
    combined_segments: dict[tuple[tuple[int, int], Literal['H', 'V'], Literal['U', 'D', 'L', 'R']], PerimeterSegment] = {}

    for segment in region.perimeter_segments:
        if (existing_combined_segment := combined_segments.get((segment.node_a, segment.containment_dir))):
            del combined_segments[(existing_combined_segment.node_a, segment.containment_dir)]
            del combined_segments[(existing_combined_segment.node_b, segment.containment_dir)]

            nodes = sorted([segment.node_a, segment.node_b, existing_combined_segment.node_a, existing_combined_segment.node_b])

            node_a = nodes[0]
            node_b = nodes[-1]

            segment = PerimeterSegment(
                node_a=node_a,
                node_b=node_b,
                containment_dir=segment.containment_dir,
            )

        if (existing_combined_segment := combined_segments.get((segment.node_b, segment.containment_dir))):
            del combined_segments[(existing_combined_segment.node_a, segment.containment_dir)]
            del combined_segments[(existing_combined_segment.node_b, segment.containment_dir)]

            nodes = sorted([segment.node_a, segment.node_b, existing_combined_segment.node_a, existing_combined_segment.node_b])

            node_a = nodes[0]
            node_b = nodes[-1]

            segment = PerimeterSegment(
                node_a=node_a,
                node_b=node_b,
                containment_dir=segment.containment_dir,
            )

        combined_segments[(segment.node_a, segment.containment_dir)] = segment
        combined_segments[(segment.node_b, segment.containment_dir)] = segment

    return list(set(combined_segments.values()))


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
            sum_ += region.area * len(region.perimeter_segments)
    return sum_

def part_2(farm: Farm):
    sum_ = 0
    nodes_considered = set()
    for i in range(farm.height):
        for j in range(farm.width):
            node = (i, j)
            if node in nodes_considered:
                continue
            region = determine_region(node, farm)
            nodes_considered = set.union(nodes_considered, region.locations)
            combined_perimeter_segments = combine_perimeter_segments(region)
            sum_ += region.area * len(combined_perimeter_segments)
    return sum_

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input_1 = parse_input('sample_input.txt')
    sample_input_2 = parse_input('sample_input.2.txt')

    before = time.time_ns()
    result = part_1(sample_input_1)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1 (sample):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_1(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1:', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(sample_input_1)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2 (sample 1 (1206)):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(sample_input_2)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2 (sample 2 (368)):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2:', result, f'({_time} ms)')
