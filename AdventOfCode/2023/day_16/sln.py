import re
import dataclasses
from typing import Literal
import collections
import timeit

T_Dir = Literal['v', '<', '^', '>']
T_Dir_Loc = tuple[T_Dir, int, int]
T_Mirror = Literal['|', '-', '/', '\\']

@dataclasses.dataclass
class Input:
    mirrors: dict[tuple[int, int], T_Mirror]
    width: int
    height: int

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.read().split('\n')
        mirrors = {}
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val in '\\|-/':
                    mirrors[(i, j)] = val
        return Input(
            mirrors=mirrors,
            width=j+1,
            height=i+1,
        )

def simulate(input: Input, initial_cond: T_Dir_Loc = ('>', 0, 0)) -> set[tuple[int, int]]:
    """
    TODO: Is there a way to cache information between simulations?
    The idea being that if a subsequent simulation results in a T_Dir_Loc
    that was seen in a previous iteration, we should be able to save the set
    of nodes that were generated from that node. Subsequent simulations could
    reference that cache using `queue_item` as a key, and could reuse prior
    work by unioning the set stored in the cache.

    To avoid absurdly high space complexity, not all `queue_item` instances
    need to have a key in the cache. The only `queue_items` that would be
    interesting would be ones that start at a mirror.
    """

    queue: collections.deque[T_Dir_Loc] = collections.deque([initial_cond])
    visited_nodes: set[tuple[int, int]] = set()
    visited_nodes_with_directions: set[T_Dir_Loc] = set()

    while len(queue) > 0:
        dir, i, j = queue_item = queue.popleft()

        # We don't need to count nodes that are out of bounds.
        if (i < 0 or i >= input.height) or (j < 0 or j >= input.height):
            continue

        visited_nodes.add((i, j))

        # This indicates a loop. No need to process it.
        if queue_item in visited_nodes_with_directions:
            continue

        visited_nodes_with_directions.add(queue_item)
        mirror = input.mirrors.get((i, j))
        match (dir, mirror):
            # Cases involving the vertical splitter.
            case ('>', '|') | ('<', '|'):
                queue.append(('^', i - 1, j))
                queue.append(('v', i + 1, j))

            # Cases involving the horizontal splitter.
            case ('v', '-') | ('^', '-'):
                queue.append(('<', i, j - 1))
                queue.append(('>', i, j + 1))

            # The 4 horsemen of going right.
            case ('v', '\\') | ('^', '/') | ('>', '-') | ('>', None):
                queue.append(('>', i, j + 1))

            # The 4 horsemen of going left.
            case ('^', '\\') | ('v', '/') | ('<', '-') | ('<', None):
                queue.append(('<', i, j - 1))

            # The 4 horsemen of going up.
            case ('>', '/') | ('<', '\\') | ('^', '|') | ('^', None):
                queue.append(('^', i - 1, j))

            # Downward dogs.
            case ('>', '\\') | ('<', '/') | ('v', '|') | ('v', None):
                queue.append(('v', i + 1, j))

            # The "I'm bad at programming" safety net.
            case _:
                raise ValueError(dir, mirror)
    return visited_nodes

def part_1(input: Input):
    return len(simulate(input))

def part_2(input: Input):
    max_nodes_visited = 0

    for i in range(0, input.height):
        max_nodes_visited = max(
            max_nodes_visited,
            len(simulate(input, ('>', i, 0))),
            len(simulate(input, ('<', i, input.width - 1))),
        )

    for j in range(0, input.width):
        max_nodes_visited = max(
            max_nodes_visited,
            len(simulate(input, ('v', 0, j))),
            len(simulate(input, ('^', input.height - 1, j))),
        )

    return max_nodes_visited

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

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
    time = part_2_timer.timeit(1)
    print('Part 2:', globals['result'], f'({time:.3} seconds)')
