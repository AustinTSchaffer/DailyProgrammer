#%%

import dataclasses
from typing import ValuesView

def input_line_to_edge(line: str):
    node_1, node_2 = line.strip().split('-')
    return (node_1, node_2)

import common
import collections
graph = collections.defaultdict(list)
for edge in common.get_input(__file__, input_line_to_edge):
    graph[edge[0]].append(edge[1])
    graph[edge[1]].append(edge[0])

#%%

class Part1Path:
    def __init__(self, path: 'Part1Path', new_node: str):
        if path:
            self.path = [*path.path, new_node]
            self.visited_nodes = {*path.visited_nodes, new_node}
        else:
            self.path = [new_node]
            self.visited_nodes = {new_node}

    def can_visit(self, node: str):
        if str.isupper(node):
            return True
        return node not in self.visited_nodes

    def last(self):
        return self.path[-1]
    
    def __repr__(self):
        return str(self.path)

class Part2Path:
    def __init__(self, path: 'Part2Path', new_node: str):
        if path:
            self.path = [*path.path, new_node]
            self.visited_nodes = {*path.visited_nodes, new_node}
            self.re_visited_small_cave = (
                True
                if str.islower(new_node) and new_node in path.visited_nodes else
                path.re_visited_small_cave
            )
        else:
            self.path = [new_node]
            self.visited_nodes = {new_node}
            self.re_visited_small_cave = False

    def can_visit(self, node: str):
        if str.isupper(node) or not self.re_visited_small_cave:
            return True
        return node not in self.visited_nodes

    def last(self):
        return self.path[-1]
    
    def __repr__(self):
        return str(self.path)

def find_paths(path):
    if path.last() == 'end':
        yield path
        return
    for node in graph[path.last()]:
        if node != 'start' and path.can_visit(node):
            yield from find_paths(path.__class__(path, node))

print("Part 1:", len(list(find_paths(Part1Path(None, 'start')))))
print("Part 2:", len(list(find_paths(Part2Path(None, 'start')))))

#%%