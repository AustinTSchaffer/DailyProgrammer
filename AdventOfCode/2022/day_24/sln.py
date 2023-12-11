import re
import dataclasses
import math
import collections
from typing import Literal
import enum
import heapq
import astar

BLIZZARD_GLYPHS = 'v>^<'

class BlizzardDir(enum.Enum):
    Down  = 0b0001
    Right = 0b0010
    Up    = 0b0100
    Left  = 0b1000

@dataclasses.dataclass(frozen=True)
class Input:
    blizzard: dict[tuple[int, int], BlizzardDir]
    """
    Initial configuration of the blizzard.
    """

    start: tuple[int, int]
    """
    Starting location of the agent.
    """

    end: tuple[int, int]
    """
    Starting location of the agent.
    """

    width: int
    """
    Width of the area which contains the blizzard.
    """

    height: int
    """
    Height of the area which contains the blizzard.
    """

@dataclasses.dataclass
class BlizzardSimulation:
    input_ref: Input
    num_states: int
    states: list[list[list[int]]]

_simulation_cache: dict[int, BlizzardSimulation] = {}
def simulate(input: Input, t: int) -> list[list[int]]:
    cache_key = id(input)
    if (cache_entry := _simulation_cache.get(cache_key)) is not None:
        return cache_entry.states[t % cache_entry.num_states]

    num_states = math.lcm(input.width, input.height)
    cache_entry = BlizzardSimulation(input, num_states, [None for _ in range(num_states)])

    current_state = [
        [0 for _ in range(input.width)]
        for _ in range(input.height)
    ]

    for location, glyph in input.blizzard.items():
        current_state[location[0]][location[1]] = glyph.value

    cache_entry.states[0] = current_state

    for state_idx in range(1, num_states):
        next_state = [
            [0 for _ in range(input.width)]
            for _ in range(input.height)
        ]

        for i, row in enumerate(current_state):
            for j, value in enumerate(row):
                if value & BlizzardDir.Up.value:
                    next_state[(i-1) % input.height][j] |= BlizzardDir.Up.value
                if value & BlizzardDir.Down.value:
                    next_state[(i+1) % input.height][j] |= BlizzardDir.Down.value
                if value & BlizzardDir.Left.value:
                    next_state[i][(j-1) % input.width] |= BlizzardDir.Left.value
                if value & BlizzardDir.Right.value:
                    next_state[i][(j+1) % input.width] |= BlizzardDir.Right.value

        cache_entry.states[state_idx] = next_state
        current_state = next_state

    _simulation_cache[cache_key] = cache_entry
    return cache_entry.states[t % cache_entry.num_states]

def possible_moves(input: Input, t: int, curr_loc: tuple[int, int]) -> dict[tuple[tuple[int, int], tuple[int, int]]]:
    return {
        move: (row, col)
        for move in ((0, 0), (-1, 0), (1, 0), (0, 1), (0, -1))
        if (
            ((
                row := curr_loc[0] + move[0],
                col := curr_loc[1] + move[1]
            ) in [input.end, input.start]) or
            (move == (0, 0) and curr_loc in [input.start, input.end]) or
            (
                row in range(0, input.height) and
                col in range(0, input.width) and
                simulate(input, t+1)[row][col] == 0
            )
        )
    }

def parse_input(filename: str) -> Input:
    blizzard_glyphs = {}
    start = None
    end = None

    with open(filename, 'r') as f:
        for row_idx, row in enumerate(f):
            for col_idx, value in enumerate(row):
                location = (row_idx-1, col_idx-1)

                if value == '.':
                    if start is None:
                        start = location
                    else:
                        end = location

                if value in BLIZZARD_GLYPHS:
                    blizzard_glyphs[location] = BlizzardDir(1 << BLIZZARD_GLYPHS.index(value))

    height = end[0] - start[0] - 1
    width = end[1] - start[1] + 1

    return Input(
        blizzard=blizzard_glyphs,
        start=start,
        end=end,
        width=width,
        height=height,
    )


def part_1(input: Input):
    def neighbors_fnct(t_n: tuple[int, tuple[int, int]]):
        t, node = t_n
        for neighbor in possible_moves(input, t, node).values():
            yield (t+1, neighbor)

    def cost_est_func(n1, n2):
        return (
            abs(n1[1][1] - n2[1][1]) +
            abs(n1[1][0] - n2[1][0])
        )

    def is_goal_reached_fnct(node_a, node_b):
        # We don't care about t when checking to see
        # if we're at the goal.
        return node_a[1] == node_b[1]

    path = astar.find_path(
        (0, input.start),
        (-1, input.end),
        neighbors_fnct=neighbors_fnct,
        heuristic_cost_estimate_fnct=cost_est_func,
        is_goal_reached_fnct=is_goal_reached_fnct,
    )

    return len(list(path)) - 1

def part_2(input: Input):
    def neighbors(t_n: tuple[int, tuple[int, int]]):
        t, node = t_n
        for neighbor in possible_moves(input, t, node).values():
            yield (t+1, neighbor)

    def manhattan(n1, n2):
        return (
            abs(n1[1][1] - n2[1][1]) +
            abs(n1[1][0] - n2[1][0])
        )

    def is_goal_reached(node_a, node_b):
        # We don't care about t when checking to see
        # if we're at the goal.
        return node_a[1] == node_b[1]

    path = astar.find_path(
        (0, input.start),
        (-1, input.end),
        neighbors_fnct=neighbors,
        heuristic_cost_estimate_fnct=manhattan,
        is_goal_reached_fnct=is_goal_reached,
    )

    output = list(path)

    path = astar.find_path(
        output[-1],
        (-1, input.start),
        neighbors_fnct=neighbors,
        heuristic_cost_estimate_fnct=manhattan,
        is_goal_reached_fnct=is_goal_reached,
    )

    output.extend(list(path))

    path = astar.find_path(
        output[-1],
        (-1, input.end),
        neighbors_fnct=neighbors,
        heuristic_cost_estimate_fnct=manhattan,
        is_goal_reached_fnct=is_goal_reached,
    )

    output.extend(list(path))

    return len(output) - 3

if __name__ == '__main__':
    input_ = parse_input('input.txt')
    sample_input_1 = parse_input('sample_input_1.txt')
    sample_input_2 = parse_input('sample_input_2.txt')

    print('Part 1 (sample 1):', part_1(sample_input_1))
    print('Part 1 (sample 2):', part_1(sample_input_2))
    # print('Part 1:', part_1(input_))

    print('Part 2 (sample 1):', part_2(sample_input_1))
    print('Part 2 (sample 2):', part_2(sample_input_2))
    print('Part 2:', part_2(input_))
