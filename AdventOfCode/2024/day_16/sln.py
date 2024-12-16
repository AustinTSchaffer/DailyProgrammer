import re
import dataclasses
import time
from typing import Any
import networkx

@dataclasses.dataclass
class Input:
    start: tuple[tuple[int, int], tuple[int, int]]
    exit: tuple[int, int]
    open_spaces: set[tuple[int, int]]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.readlines()

    open_spaces = []
    for i, row in enumerate(data):
        for j, char in enumerate(row):
            if char == '.':
                open_spaces.append((i, j))
            elif char in 'Ee':
                open_spaces.append((i, j))
                exit = (i, j)
            elif char in 'Ss':
                open_spaces.append((i, j))
                start = ((i, j), (0, 1))
    return Input(
        start=start,
        exit=exit,
        open_spaces=open_spaces,
    )

def part_1(input: Input):
    g = networkx.DiGraph()

    directions = [(-1, 0), (0, -1), (+1, 0), (0, +1)]
    for node in input.open_spaces:
        for dir_idx, dir in enumerate(directions):
            meta_node = (node, dir)

            g.add_edge(meta_node, (node, directions[(dir_idx + 1) % 4]), weight=1000)
            g.add_edge(meta_node, (node, directions[(dir_idx - 1) % 4]), weight=1000)

            if (adj := (node[0] + dir[0], node[1] + dir[1])) in input.open_spaces:
                g.add_edge(meta_node, (adj, dir), weight=1)

            for dir in directions:
                g.add_edge((input.exit, dir), input.exit, weight=0)

    spl = networkx.algorithms.shortest_path_length(
        g,
        source=input.start,
        target=input.exit,
        weight='weight'
    )

    return spl

def part_2(input: Input):
    g = networkx.DiGraph()

    directions = [(-1, 0), (0, -1), (+1, 0), (0, +1)]
    for node in input.open_spaces:
        for dir_idx, dir in enumerate(directions):
            meta_node = (node, dir)

            g.add_edge(meta_node, (node, directions[(dir_idx + 1) % 4]), weight=1000)
            g.add_edge(meta_node, (node, directions[(dir_idx - 1) % 4]), weight=1000)

            if (adj := (node[0] + dir[0], node[1] + dir[1])) in input.open_spaces:
                g.add_edge(meta_node, (adj, dir), weight=1)

            for dir in directions:
                g.add_edge((input.exit, dir), input.exit, weight=0)

    sps = networkx.algorithms.all_shortest_paths(
        g,
        source=input.start,
        target=input.exit,
        weight='weight'
    )

    included_in_one_sp = set()
    for sp in sps:
        for node in sp:
            if node != input.exit:
                included_in_one_sp.add(node[0])

    return len(included_in_one_sp)

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
