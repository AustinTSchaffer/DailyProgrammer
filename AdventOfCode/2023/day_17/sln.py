import re
import dataclasses
import timeit
from typing import Iterable
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
            start=(0,0),
            end=(i,j),
            heatmap=heatmap,
            width=j+1,
            height=i+1,
        )

class AStar_Day17(astar.AStar):
    def __init__(self, input: Input):
        self.input = input

    _diffs = ((0, -1), (0, +1), (-1, 0), (+1, 0))

    def gen_neighbors(self, node: tuple[tuple[int, int], ...]) -> tuple[int, int]:
        for diff in AStar_Day17._diffs:
            # Can't go out of bounds.
            if (i := node[-1][0] + diff[0]) < 0 or i >= self.input.height:
                continue

            # Can't go out of bounds.
            if (j := node[-1][1] + diff[1]) < 0 or j >= self.input.width:
                continue

            tup = (i, j)

            # Can't reverse direction.
            if len(node) > 1 and tup == node[-2]:
                continue

            yield tup

    def distance_between(self, _, n2: tuple[tuple[int, int], ...]) -> float:
        i, j = n2[-1]
        return self.input.heatmap[i][j]

    def is_goal_reached(self, current: tuple[tuple[int, int], ...], goal: tuple[int, int]) -> bool:
        return current[-1] == goal
    
    def heuristic_cost_estimate(self, current: tuple[tuple[int, int], ...], goal: tuple[int, int]) -> float:
        return abs(goal[0] - current[-1][0]) + abs(goal[1] - current[-1][1])


class HeatmapAstarPart1(AStar_Day17):
    def __init__(self, input: Input):
        super().__init__(input)

    def neighbors(self, node: tuple[tuple[int, int], ...]) -> Iterable:
        for neighbor in self.gen_neighbors(node):
            i, j = neighbor

            history = len(node)
            if history <= 3:
                yield (*node, neighbor)
            else:
                if all(i==n[0] for n in node):
                    continue
                if all(j==n[1] for n in node):
                    continue
                yield (*node[1:], (i, j))


def part_1(input: Input):
    result = HeatmapAstarPart1(input).astar(((input.start,)), input.end)
    result = list(result)
    return sum(
        input.heatmap[node[-1][0]][node[-1][1]]
        for node in result[1:]
    )

class HeatmapAstarPart2(AStar_Day17):
    def __init__(self, input: Input):
        super().__init__(input)

    def neighbors(self, node: tuple[tuple[int, int], ...]) -> Iterable:
        valid_neighbors = []
        for neighbor in self.gen_neighbors(node):
            i, j = neighbor

            # Invalidate early turns
            relevant_nodes = node[-5:]
            neighbor_requires_invalid_turn = (len(node) > 1 and i != node[-2][0] and j != node[-2][1]) and (
                (
                    len(relevant_nodes) < 5 and not (
                        all(i == n[0] for n in relevant_nodes) or
                        all(j == n[1] for n in relevant_nodes)
                    )
                ) or (
                    len(relevant_nodes) == 5 and not (
                        all(relevant_nodes[0][0] == n[0] for n in relevant_nodes) or
                        all(relevant_nodes[0][1] == n[1] for n in relevant_nodes)
                    )
                )
            )

            if neighbor_requires_invalid_turn:
                continue

            # Invalidate long runs.
            relevant_nodes = node[-11:]
            neighbor_in_a_run_of_11 = (
                len(relevant_nodes) == 11 and (
                    all(i == n[0] for n in relevant_nodes) or
                    all(j == n[1] for n in relevant_nodes)
                )
            )

            if neighbor_in_a_run_of_11:
                continue

            valid_neighbors.append((*node[-10:], neighbor))
        return valid_neighbors
    
    def is_goal_reached(self, current: tuple[tuple[int, int], ...], goal: tuple[int, int]) -> bool:
        last_5 = current[-5:]
        return (
            super().is_goal_reached(current, goal) and (
                all(last_5[0][0] == n[0] for n in last_5) or
                all(last_5[0][1] == n[1] for n in last_5)
            )
        )

def print_heatmap(input: Input, highlight: list[tuple[int, int]] = ()):
    result = []
    for i, row in enumerate(input.heatmap):
        for j, val in enumerate(row):
            if (i,j) in highlight:
                result.append(f'\033[1m{val}\033[0m')
            else:
                result.append(str(val))
        result.append('\n')
    print(''.join(result))

def part_2(input: Input, print_route=False):
    result = HeatmapAstarPart2(input).astar(((input.start,)), input.end)
    result = list(result)

    if print_route:
        print_heatmap(input, [n[-1] for n in result])

    return sum(
        input.heatmap[node[-1][0]][node[-1][1]]
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
