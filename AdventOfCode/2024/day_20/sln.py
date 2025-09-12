import re
import dataclasses
import time
from typing import Any
import networkx

@dataclasses.dataclass
class Input:
    grid: list[list[str]]
    graph: networkx.Graph
    width: int
    height: int
    start: tuple[int, int]
    end: tuple[int, int]


def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.read()

    grid = [
        line.strip()
        for line in data.splitlines()
        if line
    ]

    nodes = set()

    start = None
    end = None

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char in 'Ss':
                start = (i, j)
                nodes.add(start)
            elif char in 'Ee':
                end = (i, j)
                nodes.add(end)
            elif char == '.':
                nodes.add((i, j))

    if start is None or end is None:
        raise ValueError("missing start or end")

    graph = networkx.Graph()
    for node in nodes:
        for adj_move in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
            adj_node = (node[0] + adj_move[0], node[1] + adj_move[1])
            if adj_node in nodes:
                graph.add_edge(node, adj_node)

    return Input(
        graph=graph,
        end=end,
        start=start,
        height=len(grid),
        width=len(grid[0]),
        grid=grid,
    )

def part_1(input: Input):
    shortest_path = networkx.shortest_path(input.graph, input.start, input.end)

    path_node_times = {
        node: i
        for i, node in enumerate(shortest_path)
    }

    cheating_options = [
        (+2, 0),
        (+1, +1),
        (0, +2),
        (-2, 0),
        (-1, -1),
        (0, -2),
        (-1, +1),
        (+1, -1),
    ]

    cheats_and_time_saved = {}

    for node_time, node in enumerate(shortest_path):
        for cheat_option in cheating_options:
            adj_node = (node[0] + cheat_option[0], node[1] + cheat_option[1])
            if (adj_node_time := path_node_times.get(adj_node)) is not None:
                cheats_and_time_saved[(node, adj_node)] = adj_node_time - (node_time + 2)

    output = 0
    for time_saved in cheats_and_time_saved.values():
        if time_saved >= 100:
            output += 1
    return output

def part_2(input: Input):
    shortest_path = networkx.shortest_path(input.graph, input.start, input.end)

    path_node_times = {
        node: i
        for i, node in enumerate(shortest_path)
    }

    cheating_options: list[tuple[int, int]] = []

    for i in range(-20, 21):
        for j in range(-20, 21):
            if abs(i) + abs(j) <= 20:
                cheating_options.append((i, j))

    cheats_and_time_saved = {}

    for node_time, node in enumerate(shortest_path):
        for cheat_option in cheating_options:
            adj_node = (node[0] + cheat_option[0], node[1] + cheat_option[1])
            if (adj_node_time := path_node_times.get(adj_node)) is not None:
                cheat_id = (node, adj_node)
                time_saved = adj_node_time - (node_time + abs(cheat_option[0]) + abs(cheat_option[1]))

                if (prior_time_saved := cheats_and_time_saved.get(cheat_id)):
                    cheats_and_time_saved[cheat_id] = max(prior_time_saved, time_saved)
                else:
                    cheats_and_time_saved[cheat_id] = time_saved

    output = 0
    for time_saved in cheats_and_time_saved.values():
        if time_saved >= 100:
            output += 1
    return output

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
