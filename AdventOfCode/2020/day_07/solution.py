#%% Load puzzle input

SHINY_GOLD = "shiny gold"
puzzle_input = open("./puzzle_input.txt").readlines()

#%% Generate Directed Graph and Reverse Directed Graph

# The puzzle input is essentially a text-based directed graph,
# showing which bag colors any bag color can contain. This section
# loads that data into memory as a searchable directed graph.

# This section also reverses that directed graph, so the script
# can later perform a graph search from "shiny gold". All nodes
# reachable from "shiny gold" represent outer bag colors that can
# contain a "shiny gold" bag anywhere within.

import re
import collections

# Stores the data as-is
directed_graph = {}

# Stores the data as a reverse directed graph, discarding any "count" data.
# Austin <3 defaultdict
reverse_directed_graph = collections.defaultdict(list)

for line in puzzle_input:
    # Clean up irrelevant data
    line = re.sub(r"bags?\.?", "", line)

    # Split line into node and edges
    node, edges = line.split("contain")
    node = node.strip()

    edges = (
        [] if "no other" in edges else
        list(map(str.strip, edges.split(",")))
    )

    for i, edge in enumerate(edges):
        count, *color_data = edge.split(" ")
        edges[i] = {
            "count": int(count),
            "color": " ".join(color_data),
        }

    # Persist the data as-is
    directed_graph[node] = edges

    # Reverse the direction
    for edge in edges:
        reverse_directed_graph[edge["color"]].append(node)

#%% Part 1: Graph Search on Reverse Directed Graph

# Simple graph algorithm that visits all nodes connected to
# SHINY_GOLD in an arbitrary order. This is probably a BFS.

include_shiny_gold = False
colors_visited = set()
colors_to_visit = [SHINY_GOLD]

while any(colors_to_visit):
    current_color = colors_to_visit.pop(0)
    colors_visited.add(current_color)
    for next_color in reverse_directed_graph[current_color]:
        if next_color not in colors_visited:
            colors_to_visit.append(next_color)

        elif next_color == SHINY_GOLD:
            # In this case, a shiny gold bag can eventually contain
            # another shiny gold bag. If this is not reached, the
            # length of colors_visited is 1 too big.
            include_shiny_gold = True

valid_outer_colors = (
    len(colors_visited) +
    (0 if include_shiny_gold else -1)
)

print("Valid outer colors:", valid_outer_colors)

#%% Part 2: Determine overall size of 1 shiny gold bag

# Simple recursive tree search algorithm. If there were any cycles in the graph
# this part of the problem would not be solveable, so I'm ignoring the
# possibility.

def count_bags(bag_color) -> int:
    """
    Counts the number of bags that must be contained in a single bag of
    a given color.
    """
    count = 0
    edges = directed_graph[bag_color]
    for edge in edges:
        count += (edge["count"] + (edge["count"] * count_bags(edge["color"])))
    return count

total_count = count_bags(SHINY_GOLD)
print(f"Bags contained in a single {SHINY_GOLD} bag: {total_count}")
