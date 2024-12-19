import re
import dataclasses
import time
from typing import Any
import networkx as nx

@dataclasses.dataclass
class Input:
    falling_bytes: list[tuple[int, int]]
    initial_bytes_fallen: int
    width: int
    height: int

def parse_input(filename: str, initial_bytes_fallen: int) -> Input:
    with open(filename, 'r') as f:
        data = f.readlines()

    falling_bytes = [
        tuple(reversed(list(map(int, line.strip().split(',')))))
        for line in data
        if line
    ]

    max_i = max(b[0] for b in falling_bytes)
    max_j = max(b[1] for b in falling_bytes)

    return Input(
        falling_bytes=falling_bytes,
        initial_bytes_fallen=initial_bytes_fallen,
        height=max_i+1,
        width=max_j+1,
    )

def part_1(input: Input):
    G = nx.grid_graph((input.height, input.width))
    for node in input.falling_bytes[:input.initial_bytes_fallen]:
        G.remove_node(node)
    pl = nx.astar_path_length(
        G,
        source=(0, 0),
        target=(input.height-1, input.width-1),
        heuristic=lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
    )
    return pl

def part_2(input: Input):
    G = nx.grid_graph((input.height, input.width))
    for node in input.falling_bytes[:input.initial_bytes_fallen]:
        G.remove_node(node)
    for node in input.falling_bytes[input.initial_bytes_fallen:]:
        G.remove_node(node)
        try:
            nx.astar_path_length(
                G,
                source=(0, 0),
                target=(input.height-1, input.width-1),
                heuristic=lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
            )

        except Exception:
            return f'{node[1]},{node[0]}'


if __name__ == '__main__':
    input = parse_input('input.txt', 1024)
    sample_input = parse_input('sample_input.txt', 12)

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
