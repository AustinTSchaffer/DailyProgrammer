import re
import dataclasses
import time
from typing import Any

@dataclasses.dataclass
class Input:
    grid: list[list[int]]
    width: int
    height: int
    trailheads: list[tuple[int, int]]

def parse_input(filename: str) -> Input:
    trailheads = []
    grid = []

    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue

            row = []
            grid.append(row)

            for j, char in enumerate(line):
                value = int(char)
                row.append(value)
                if value == 0:
                    trailheads.append((i, j))
    return Input(
        grid=grid,
        width=len(grid[0]),
        height=len(grid),
        trailheads=trailheads,
    )


def in_bounds(location: tuple[int, int], input: Input) -> bool:
    return (
        location[0] >= 0 and location[0] < input.height and
        location[1] >= 0 and location[1] < input.width
    )

def find_9s(start: tuple[int, int], input: Input) -> int:
    spaces_visited: set[tuple[int, int]] = set()
    frontier = [start]
    num_9s_found = 0



    while frontier:
        location = frontier.pop()
        spaces_visited.add(location)

        if input.grid[location[0]][location[1]] == 9:
            num_9s_found += 1

        for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_loc = (
                location[0] + dir[0],
                location[1] + dir[1],
            )

            if not in_bounds(adj_loc, input) or adj_loc in spaces_visited:
                continue

            if input.grid[location[0]][location[1]] + 1 == input.grid[adj_loc[0]][adj_loc[1]]:
                frontier.append(adj_loc)

    return num_9s_found


_find_9s_dfs_cache: dict[tuple[tuple[int, int], int], int] = {}
def find_9s_dfs(location: tuple[int, int], input: Input) -> int:
    if not in_bounds(location, input):
        return 0

    if input.grid[location[0]][location[1]] == 9:
        # No point in caching this result.
        # _find_9s_dfs_cache[cache_key] = 1
        return 1

    cache_key = (location, id(input))

    if (prev_result := _find_9s_dfs_cache.get(cache_key)):
        return prev_result

    result = 0
    for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        adj_loc = (
            location[0] + dir[0],
            location[1] + dir[1],
        )

        if not in_bounds(adj_loc, input):
            continue

        if input.grid[location[0]][location[1]] + 1 == input.grid[adj_loc[0]][adj_loc[1]]:
            result += find_9s_dfs(adj_loc, input)

    _find_9s_dfs_cache[cache_key] = result
    return result


def determine_rating(start: tuple[int, int], input: Input) -> int:
    return find_9s_dfs(start, input)

def part_1(input: Input):
    score = 0
    for trailhead in input.trailheads:
        score += find_9s(trailhead, input)
    return score

def part_2(input: Input):
    score = 0
    for trailhead in input.trailheads:
        score += determine_rating(trailhead, input)
    return score

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
