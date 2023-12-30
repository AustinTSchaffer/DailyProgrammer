import re
import dataclasses
import timeit
import networkx as nx
import random


@dataclasses.dataclass
class Input:
    graph: nx.Graph
    nodes: list[str]


def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        graph = nx.Graph()
        nodes = set()
        for line in f:
            n, adjs = line.split(':')
            adjs = list(map(str.strip, adjs.split()))
            nodes.add(n)
            for adj in adjs:
                nodes.add(adj)
                graph.add_edge(n, adj)
        return Input(
            graph=graph,
            nodes=list(nodes),
        )

def part_1(input: Input):
    graph_copy = input.graph.copy()
    mc = nx.minimum_edge_cut(graph_copy)
    for n1, n2 in mc:
        graph_copy.remove_edge(n1, n2)
    subgraphs = list(nx.connected_components(graph_copy))
    assert len(subgraphs) == 2
    return len(subgraphs[0]) * len(subgraphs[1])

def part_2(graph: nx.Graph):
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

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
