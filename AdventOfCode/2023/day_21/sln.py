import re
import dataclasses
import timeit
import collections
from typing import Iterable

@dataclasses.dataclass
class Input:
    steps: int
    rocks: set[tuple[int, int]]
    start: tuple[int, int]
    width: int
    height: int


def parse_input(filename: str, steps: int = 64) -> Input:
    with open(filename, 'r') as f:
        rocks = set()
        for i, row in enumerate(f):
            for j, val in enumerate(row.strip()):
                if val == '#':
                    rocks.add((i, j))
                if val == 'S':
                    start = (i, j)
        return Input(
            steps=steps,
            rocks=rocks,
            start=start,
            width=j+1,
            height=i+1
        )

_diffs = ((-1, 0), (+1, 0), (0, -1), (0, +1))
def adj_nodes(node: tuple[int, int], input: Input) -> Iterable[tuple[int, int]]:
    for diff in _diffs:
        i = node[0] + diff[0]
        j = node[1] + diff[1]

        if (i % input.height, j % input.width) in input.rocks:
            continue

        yield (i, j)

def num_visitable_bfs(input: Input, steps: int = None):
    steps = input.steps if steps is None else steps
    explored = {input.start: 0}

    node_queue = collections.deque([input.start])
    node_queue_next = collections.deque([])

    for step in range(1, steps+1):
        while len(node_queue) > 0:
            node = node_queue.popleft()
            for adj_node in adj_nodes(node, input):
                if adj_node not in explored:
                    explored[adj_node] = step
                    node_queue_next.append(adj_node)
        node_queue, node_queue_next = node_queue_next, node_queue

    valid_rem = steps % 2
    return sum(
        1 for v in explored.values()
        if v % 2 == valid_rem
    ), explored

def part_1(input: Input):
    return num_visitable_bfs(input)[0]

def part_2(input: Input, steps: int = None):
    # This cutoff could probably be a function of the number of steps and the input size.
    if steps <= 400:
        return num_visitable_bfs(input, steps)[0]

    """
    """

    raise NotImplementedError()

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt', steps=6)

    timeit_globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals = timeit_globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input, steps)',
        globals = timeit_globals
    )

    print('Part 1 (sample):', part_1(sample_input))
    time = part_1_timer.timeit(1)
    print('Part 1:', timeit_globals['result'], f'({time:.3} seconds)')

    # TODO: Figure out how quickly the results grow using
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
    # for both (a) the number of visitable nodes and (b)
    # the time it takes to search that space. This should
    # help determine the time it'll take to brute-force the
    # actual input, as well as what the approximate answer
    # will be (precise to ~ +- 1 OoM).
    for steps in [6, 10, 50, 100, 500, 1000, 5000]:
        timeit_globals['input'] = sample_input
        timeit_globals['steps'] = steps
        time = part_2_timer.timeit(1)
        print(f'Part 2 (sample, {steps} steps):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    timeit_globals['steps'] = 26501365
    time = part_2_timer.timeit(1)
    print('Part 2:', timeit_globals['result'], f'({time:.3} seconds)')
