import re
import dataclasses
import timeit
from typing import Iterable, NamedTuple
import astar
import math

@dataclasses.dataclass
class Input:
    start: tuple[int, int]
    end: tuple[int, int]
    heatmap: list[list[int]]
    width: int
    height: int


def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        heatmap = []
        for i, row in enumerate(f):
            heatmap.append([])
            for j, val in enumerate(row.strip()):
                heatmap[-1].append(int(val))

        return Input(
            start=(0, 0),
            end=(i, j),
            heatmap=heatmap,
            width=j+1,
            height=i+1,
        )


def print_heatmap(input: Input, highlight: list[tuple[int, int]] = ()):
    result = []
    for i, row in enumerate(input.heatmap):
        for j, val in enumerate(row):
            if (i, j) in highlight:
                result.append(f'\033[1m{val}\033[0m')
            else:
                result.append(str(val))
        result.append('\n')
    print(''.join(result))


TNode = tuple[int, int, int, int]


class AStar_Day17(astar.AStar):
    def __init__(self, input: Input):
        self.input = input

    _diffs = ((0, -1), (0, +1), (-1, 0), (+1, 0))

    def neighbors(self, node: TNode) -> Iterable[TNode]:
        for diff in AStar_Day17._diffs:
            # Can't go out of bounds.
            if (i := node[0] + diff[0]) < 0 or i >= self.input.height:
                continue

            # Can't go out of bounds.
            if (j := node[1] + diff[1]) < 0 or j >= self.input.width:
                continue

            # Can't reverse direction.
            if (diff[0] and ((diff[0] * node[2]) < 0)) or (diff[1] and ((diff[1] * node[3]) < 0)):
                continue

            yield (
                i,
                j,
                (node[2] + diff[0]) if diff[0] else 0,
                (node[3] + diff[1]) if diff[1] else 0,
            )

    def distance_between(self, _, n2: TNode) -> float:
        return self.input.heatmap[n2[0]][n2[1]]

    def is_goal_reached(self, current: TNode, goal: tuple[int, int]) -> bool:
        return current[0] == goal[0] and current[1] == goal[1]
    
    def heuristic_cost_estimate(self, current: TNode, goal: tuple[int, int]) -> float:
        return abs(goal[0] - current[0]) + abs(goal[1] - current[1])


class HeatmapAstarPart1(AStar_Day17):
    def __init__(self, input: Input):
        super().__init__(input)

    def neighbors(self, node: TNode) -> Iterable[TNode]:
        for neighbor in super().neighbors(node):
            if abs(neighbor[2]) <= 3 and abs(neighbor[3]) <= 3:
                yield neighbor

class HeatmapAstarPart2(AStar_Day17):
    def __init__(self, input: Input):
        super().__init__(input)

    def neighbors(self, node: TNode) -> TNode:
        for neighbor in super().neighbors(node):
            # Invalidate early turns
            neighbor_requires_invalid_turn = (
                (node[2] and abs(node[2]) < 4 and not neighbor[2]) or
                (node[3] and abs(node[3]) < 4 and not neighbor[3])
            )

            if neighbor_requires_invalid_turn:
                continue

            # Invalidate long runs.
            if abs(neighbor[2]) > 10 or abs(neighbor[3]) > 10:
                continue

            yield neighbor
    
    def is_goal_reached(self, current: TNode, goal: tuple[int, int]) -> bool:
        return (
            super().is_goal_reached(current, goal) and (
                abs(current[2]) >= 4 or abs(current[3]) >= 4
            )
        )


def part_1(input: Input, print_route=True):
    result = HeatmapAstarPart1(input).astar((*input.start, 0, 0), input.end)
    result = list(result)

    if print_route:
        print_heatmap(input, {(n[0], n[1]) for n in result})

    return sum(
        input.heatmap[node[0]][node[1]]
        for node in result[1:]
    )


def part_2(input: Input, print_route=True):
    result = HeatmapAstarPart2(input).astar((*input.start, 0, 0), input.end)
    result = list(result)

    if print_route:
        print_heatmap(input, {(n[0], n[1]) for n in result})

    return sum(
        input.heatmap[node[0]][node[1]]
        for node in result[1:]
    )

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')
    sample_input_2 = parse_input('sample_input_2.txt')

    globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals = globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals = globals
    )

    print('Part 1 (sample):', part_1(sample_input))
    time = part_1_timer.timeit(1)
    print('Part 1:', globals['result'], f'({time:.3} seconds)')

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2 (sample 2):', part_2(sample_input_2))
    time = part_2_timer.timeit(1)
    print('Part 2:', globals['result'], f'({time:.3} seconds)')
