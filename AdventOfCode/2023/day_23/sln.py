import re
import dataclasses
import timeit
from typing import Literal
import collections

@dataclasses.dataclass
class Input:
    start: tuple[int, int]
    end: tuple[int, int]
    raw_graph: dict[tuple[int, int], list[tuple[int, int]]]
    """
    `(x_1, y_1) -> [(x_2, y_2), ...]`
    """
    graph: dict[tuple[int, int], list[tuple[int, tuple[int, int]]]]
    """
    `(x_1, y_1) -> [(cost, (x_2, y_2)), ...]`
    """

def parse_input(filename: str) -> Input:
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
                    glyphs[coord] = val

    raw_graph: dict[tuple[int, int], list[tuple[int, int]]] = {}
    num_adj_nodes = collections.defaultdict(int)
    for coord, glyph in glyphs.items():
        raw_adjs = raw_graph.setdefault(coord, [])

        if (adj := (coord[0], coord[1] + 1)) in glyphs:
            num_adj_nodes[coord] += 1
            if glyph in '.>' and glyphs[adj] != '<':
                raw_adjs.append(adj)
        if (adj := (coord[0], coord[1] - 1)) in glyphs:
            num_adj_nodes[coord] += 1
            if glyph in '.<' and glyphs[adj] != '>':
                raw_adjs.append(adj)
        if (adj := (coord[0] - 1, coord[1])) in glyphs:
            num_adj_nodes[coord] += 1
            if glyph in '.^' and glyphs[adj] != 'v':
                raw_adjs.append(adj)
        if (adj := (coord[0] + 1, coord[1])) in glyphs:
            num_adj_nodes[coord] += 1
            if glyph in '.v' and glyphs[adj] != '^':
                raw_adjs.append(adj)

    graph: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
    visited = set()
    q = collections.deque([(None, start)])
    while len(q):
        prev_node, node = q.popleft()
        raw_adjs = raw_graph[node]

        # If the number of incoming/outgoing edges is <= 2, then the
        # node is in the middle part of a hallway, e.g. not at a junction.
        if num_adj_nodes[node] <= 2 and prev_node and node in graph[prev_node]:
            unvisited_adjs = [ra for ra in raw_adjs if ra not in visited]
            if len(unvisited_adjs) == 1:
                new_adj = unvisited_adjs[0]
            elif len(raw_adjs) == 1 and raw_adjs[0] in graph:
                new_adj = raw_adjs[0]
            elif node == end:
                continue
            else:
                raise ValueError()

            cost = graph[prev_node].pop(node)
            graph[prev_node][new_adj] = cost + 1
            q.extend((prev_node, n) for n in raw_adjs if n not in visited)
        else:
            graph[node] = {adj: 1 for adj in raw_adjs}
            q.extend((node, n) for n in raw_adjs if n not in visited)
        visited.add(node)

    # Sanity check, the ending node should be the last node
    # in 
    assert end in [
        k
        for v in graph.values()
        for k in v.keys()
    ]

    return Input(
        start=start,
        end=end,
        raw_graph=raw_graph,
        graph=graph,
    )

def part_1(input: Input):
    ...

def part_2(input: Input):
    ...

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

    timeit_globals['input'] = sample_input
    time = part_1_timer.timeit(1)
    print('Part 2 (sample):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = part_2_timer.timeit(1)
    print('Part 2:', timeit_globals['result'], f'({time:.3} seconds)')
