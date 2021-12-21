from typing import ValuesView
import common
input = common.get_input(__file__, str.strip)

world = {}
for row, line in enumerate(input):
    for col, risk_level in enumerate(line):
        world[(row, col)] = int(risk_level)

start = (0, 0)
end = (row, col)

def heuristic(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def neighbors(point):
    yield (point[0] - 1, point[1])
    yield (point[0] + 1, point[1])
    yield (point[0], point[1] - 1)
    yield (point[0], point[1] + 1)

def construct_path(start, end, most_efficient_edges):
    path = [end]
    while (last_node := path[-1]) != start:
        path.append(most_efficient_edges[last_node][1])
    return most_efficient_edges[end][0], list(reversed(path))

import heapq
def astar_search(start, end, world, heuristic=heuristic):
    """
    Bog-standard A* implementation.
    """

    # Node Priority Queue (PQ). Priority is "cost to node" plus "heuristic of node->end"
    node_pq = []
    heapq.heappush(node_pq, [0 + heuristic(start, end), start])

    # Also keeping track of a node_pq_set in parallel, so we can check to see if any nodes
    # are in the Node PQ without iterating over the Node PQ.
    node_pq_set = {start}

    # A graph/map that tracks the most efficient paths to any given node, tracking the cost
    # to get to that node and the node it came from.
    efficient_edges = {start: (0, None)}

    while node_pq:
        _, node = heapq.heappop(node_pq)
        if node == end:
            return construct_path(start, end, efficient_edges)
        for neighbor in neighbors(node):
            if neighbor in world:
                cost_to_neighbor = efficient_edges[node][0] + world[neighbor]
                if neighbor not in efficient_edges or cost_to_neighbor < efficient_edges[neighbor][0]:
                    efficient_edges[neighbor] = (cost_to_neighbor, node)
                    if neighbor not in node_pq_set:
                        heapq.heappush(node_pq, [cost_to_neighbor + heuristic(neighbor, end), neighbor])
                        node_pq_set.add(neighbor)

    raise ValueError("cannot reach end from start in world")

total_cost, most_efficient_path = astar_search(start, end, world)
print("Part 1:", total_cost, most_efficient_path)

WORLD_WIDTH = 100
WORLD_HEIGHT = 100

part_2_world = {}
for location, risk in world.items():
    for x_offset in range(5):
        for y_offset in range(5):
            new_risk_value = risk + x_offset + y_offset
            if new_risk_value > 9:
                new_risk_value = (new_risk_value % 9)

            part_2_world[(location[0] + (WORLD_WIDTH * x_offset), location[1] + (WORLD_HEIGHT * y_offset))] = new_risk_value

end = ((WORLD_WIDTH * 5) - 1, (WORLD_HEIGHT * 5) - 1)

total_cost, most_efficient_path = astar_search(start, end, part_2_world)
print("Part 2:", total_cost)
