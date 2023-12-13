import re
import dataclasses

@dataclasses.dataclass
class Input:
    grid: list[str]
    start: tuple[int, int]
    loop: dict[tuple[int, int], tuple[tuple[int, int], tuple[int, int]]]

_diffs = ((-1, 0), (+1, 0), (0, -1), (0, +1))
def adjacent_coords_node(node: tuple[int, int], grid: list[str]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    yield from (
        (diff, (i, j))
        for diff in _diffs
        if 0 <= (i := node[0] + diff[0]) < len(grid)
        if 0 <= (j := node[1] + diff[1]) < len(grid[0])
    )

def adjacent_coords_glyph(node: tuple[int, int], glyph: str) -> tuple[tuple[int, int], tuple[int, int]]:
    match glyph:
        case '|':
            return (node[0] - 1, node[1]), (node[0] + 1, node[1])
        case '-':
            return (node[0], node[1] - 1), (node[0], node[1] + 1)
        case 'F':
            return (node[0] + 1, node[1]), (node[0], node[1] + 1)
        case 'L':
            return (node[0] - 1, node[1]), (node[0], node[1] + 1)
        case '7':
            return (node[0] + 1, node[1]), (node[0], node[1] - 1)
        case 'J':
            return (node[0] - 1, node[1]), (node[0], node[1] - 1)
        case _:
            raise ValueError(glyph)

def find_loop(grid: list[str]) -> tuple[tuple[int, int], dict[tuple[int, int], tuple[tuple[int, int], tuple[int, int]]]]:
    loop = {}
    start = next(
        (i, j)
        for i, row in enumerate(grid)
        for j, val in enumerate(row)
        if val == 'S'
    )

    loop[start] = []
    current = None

    # Let's find one of the coordinates that start connects to.
    for diff, adj_coord in adjacent_coords_node(start, grid):
        val = grid[adj_coord[0]][adj_coord[1]]
        cond = (
            (diff == (-1, 0) and val in '|F7') or
            (diff == (+1, 0) and val in '|JL') or
            (diff == (0, +1) and val in '-J7') or
            (diff == (0, -1) and val in '-LF')
        )

        if cond:
            loop[start].append(adj_coord)
            current = adj_coord

    assert current is not None
    while True:
        adj_coords = adjacent_coords_glyph(current, grid[current[0]][current[1]])
        loop[current] = adj_coords

        coords_not_in_loop = [
            c for c in adj_coords if c not in loop
        ]

        if len(coords_not_in_loop) <= 0:
            break

        current = coords_not_in_loop[0]

    return start, loop
        

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        grid = [ line.strip() for line in f ]

    start, loop = find_loop(grid)
    return Input(
        grid=grid,
        start=start,
        loop=loop,
    )

def part_1(input: Input):
    return len(input.loop) // 2

def part_2(input: Input):
    points_in_loop = 0
    northbound_glyphs = '|JL'
    def is_northbound(loc: tuple[int, int], glyph: str):
        if glyph in northbound_glyphs:
            return True

        if loc == input.start:
            if (loc[0] - 1, loc[1]) in input.loop[loc]:
                return True

        return False

    for i, row in enumerate(input.grid):
        inside_bendy_boi = False
        for j, glyph in enumerate(row):
            loc = (i,j)
            if loc in input.loop and is_northbound(loc, glyph):
                inside_bendy_boi = not inside_bendy_boi
            elif ((i,j) not in input.loop) and inside_bendy_boi:
                points_in_loop += 1
    return points_in_loop

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample, ans=4):', part_1(sample_input))
    print('Part 1:', part_1(input))

    sample_input_part_2_1 = parse_input('sample_input_part_2.1.txt')
    sample_input_part_2_2 = parse_input('sample_input_part_2.2.txt')

    print('Part 2 (sample 1, ans=8):', part_2(sample_input_part_2_1))
    print('Part 2 (sample 2, ans=10):', part_2(sample_input_part_2_2))
    print('Part 2:', part_2(input))
