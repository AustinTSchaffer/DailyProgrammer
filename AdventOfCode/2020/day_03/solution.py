tree_map = list(map(str.strip, open("map.txt").readlines()))
TREE = "#"

def ski_and_count_trees(slope_x, slope_y):
    trees_encountered = 0
    x_coord = 0

    for line_num, line in enumerate(tree_map):
        if line_num % slope_y != 0:
            continue

        trees_encountered += (line[x_coord] == TREE)
        x_coord = (x_coord + slope_x) % len(line)

    return trees_encountered

trees_encountered = ski_and_count_trees(3, 1)
print("Part 1:", trees_encountered)

import math
part_2_result = math.prod(
    ski_and_count_trees(x, y)
    for x, y in [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
)

print("Part 2:", part_2_result)
