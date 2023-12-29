import re
import dataclasses
import timeit
from typing import Iterable, Literal
import collections
import astar
import itertools


@dataclasses.dataclass
class Input:
    width: int
    height: int

    start: tuple[int, int]
    end: tuple[int, int]
    raw_graph: dict[tuple[int, int], list[tuple[int, int]]]
    """
    All nodes from the original input are represented.
    All edge weights are 1.

    `(x_1, y_1) -> [(x_2, y_2), ...]`
    """

    graph: dict[tuple[int, int], dict[tuple[int, int], int]]
    """
    Redundant nodes removed, squashed into single edges between
    nodes connected only by a single "hallway". This is not
    Floyd-Warshall's algorithm, just a crappy compression alg.

    `(x_1, y_1) -> {(x_2, y_2): cost, ...}`
    """


def parse_input(filename: str, obey_slopes: bool = True) -> Input:
    start = None
    end = None
    glyphs = {}

    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            for j, val in enumerate(line.strip()):
                coord = (i, j)
                if val == '.':
                    if start is None:
                        start = coord
                    end = coord
                if val != '#':
                    glyphs[coord] = val if obey_slopes else '.'

    raw_graph: dict[tuple[int, int], list[tuple[int, int]]] = {}
    num_adj_nodes: dict[tuple[int, int], int] = collections.defaultdict(int)
    for coord, glyph in glyphs.items():
        adj_nodes = raw_graph.setdefault(coord, [])
        if (adj := (coord[0], coord[1] + 1)) in glyphs:
            num_adj_nodes[coord] += 1
            if glyph in '.>' and glyphs[adj] != '<':
                adj_nodes.append(adj)
        if (adj := (coord[0], coord[1] - 1)) in glyphs:
            num_adj_nodes[coord] += 1
            if glyph in '.<' and glyphs[adj] != '>':
                adj_nodes.append(adj)
        if (adj := (coord[0] - 1, coord[1])) in glyphs:
            num_adj_nodes[coord] += 1
            if glyph in '.^' and glyphs[adj] != 'v':
                adj_nodes.append(adj)
        if (adj := (coord[0] + 1, coord[1])) in glyphs:
            num_adj_nodes[coord] += 1
            if glyph in '.v' and glyphs[adj] != '^':
                adj_nodes.append(adj)

    graph: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
    junctions = {start, end, *(
        node for node in raw_graph
        if num_adj_nodes[node] > 2
    )}

    for junction in junctions:
        graph[junction] = {adj_node: 1 for adj_node in raw_graph[junction]}
        q = collections.deque([(junction, adj_node) for adj_node in raw_graph[junction]])
        while len(q):
            prev_node, node = q.pop()
            adj_nodes = raw_graph[node]
            if node not in junctions:
                cost = graph[junction].pop(node)
                for adj_node in adj_nodes:
                    if adj_node != prev_node:
                        graph[junction][adj_node] = cost + 1
                        q.append((node, adj_node))

    # Sanity check, there should be an edge to the end from at least
    # one node (probably will be exactly one node).
    assert any(
        k == end
        for v in graph.values()
        for k in v.keys()
    )

    return Input(
        width=j + 1,
        height=i + 1,
        start=start,
        end=end,
        raw_graph=raw_graph,
        graph=graph,
    )


def get_longest_path(input: Input) -> int:
    def _get_longest_path(node: tuple[int, int], visited: frozenset[tuple[int, int]]):
        if node == input.end:
            return 0, []

        visited = frozenset(visited | {node})
        max_path = (0, None)
        for adj_node, cost in input.graph[node].items():
            if adj_node not in visited:
                if (candidate := _get_longest_path(adj_node, visited)) is not None:
                    max_path = max(max_path, (cost + candidate[0], [adj_node, *candidate[1]]))

        if max_path[1] is None:
            return None

        return max_path

    return _get_longest_path(input.start, frozenset())


def part_1(input: Input):
    return get_longest_path(input)


def part_2(input: Input):
    return get_longest_path(input)


if __name__ == '__main__':
    sample_input = parse_input('sample_input.txt')
    input = parse_input('input.txt')

    timeit_globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals=timeit_globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals=timeit_globals
    )

    timeit_globals['input'] = sample_input
    time = part_1_timer.timeit(1)
    print('Part 1 (sample):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = part_1_timer.timeit(1)
    print('Part 1:', timeit_globals['result'], f'({time:.3} seconds)')

    sample_input_part_2 = parse_input('sample_input.txt', False)
    input_part_2 = parse_input('input.txt', False)

    timeit_globals['input'] = sample_input_part_2
    time = part_2_timer.timeit(1)
    print('Part 2 (sample):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input_part_2
    time = part_2_timer.timeit(1)
    print('Part 2 (5829 < x < 6582):', timeit_globals['result'], f'({time:.3} seconds)')
