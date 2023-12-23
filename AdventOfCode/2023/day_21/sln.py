import re
import dataclasses
import timeit
import collections
from typing import Iterable
import numpy as np

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
            width=j + 1,
            height=i + 1
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
    return next(iter_num_visitable_bfs(input, steps))


def iter_num_visitable_bfs(input: Input, starting_steps: int = None, ending_steps: int = None):
    steps = input.steps if starting_steps is None else starting_steps

    explored = {input.start: 0}

    node_queue = collections.deque([input.start])
    node_queue_next = collections.deque([])

    def sim(step: int):
        nonlocal node_queue, node_queue_next
        while len(node_queue) > 0:
            node = node_queue.popleft()
            for adj_node in adj_nodes(node, input):
                if adj_node not in explored:
                    explored[adj_node] = step
                    node_queue_next.append(adj_node)
        node_queue, node_queue_next = node_queue_next, node_queue

    for step in range(1, steps + 1):
        sim(step)

    step = steps
    while True:
        valid_rem = step % 2
        yield (
            sum(
                1 for v in explored.values()
                if v % 2 == valid_rem
            ),
            step,
            explored,
        )

        if step >= ending_steps:
            return

        step += 1
        sim(step)

def part_1(input: Input):
    return num_visitable_bfs(input)[0]


def part_2(input: Input, steps: int = None):
    # This cutoff could probably be a function of the number of steps and the input size.
    if steps <= 400:
        return num_visitable_bfs(input, steps)[0]

    print()
    print("Solving for", steps, "using... linear algebra.")
    print()

    modulus_bucket = steps % (input.width * 2)
    print(f"{steps} mod {input.width * 2} = {modulus_bucket} (modulus bucket)")
    lower_order_results = {}

    print(f"g(y) = f(262y + {modulus_bucket})")
    print()

    for i in range(3):
        n_steps = (i * input.width * 2) + modulus_bucket
        lower_order_results[n_steps] = (i, num_visitable_bfs(input, n_steps)[0])
        print(f"f({n_steps}) = g({i}) = {lower_order_results[n_steps][1]}")

    print()

    eqs = []
    ans = []
    for x, y in lower_order_results.values():
        eqs.append([x ** 2, x, 1])
        ans.append(y)
        if x == 0:
            print(f"c = {y}")
        elif x == 1:
            print(f"a + b + c = {y}")
        else:
            print(f"{x ** 2}a + {x}b + c = {y}")

    print()

    coeffs = np.linalg.solve(np.array(eqs), np.array(ans))
    coeffs = list(map(int, coeffs))
    print(f"g(x) = {int(coeffs[0])}x^2 + {int(coeffs[1])}x + {int(coeffs[2])}")

    print()

    rescaled = (steps - modulus_bucket) // (input.width * 2)
    answer = (coeffs[0] * (rescaled ** 2)) + (coeffs[1] * rescaled) + coeffs[2]
    print(f"f({steps}) = g({rescaled}) = {answer}")
    print()

    return int((coeffs[0] * (rescaled ** 2)) + (coeffs[1] * rescaled) + coeffs[2])

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt', steps=6)

    timeit_globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals=timeit_globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input, steps)',
        globals=timeit_globals
    )

    print('Part 1 (sample):', part_1(sample_input))
    time = part_1_timer.timeit(1)
    print('Part 1:', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    timeit_globals['steps'] = 26_501_365
    time = part_2_timer.timeit(1)
    print('Part 2:', timeit_globals['result'], f'({time:.3} seconds)')
