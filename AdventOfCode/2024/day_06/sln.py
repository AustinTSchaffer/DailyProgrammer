import re
import dataclasses
import time
from typing import Any


@dataclasses.dataclass
class Input:
    start: tuple[int, int, tuple[int, int]]
    width: int
    height: int
    obstacles: set[tuple[int, int]]


def parse_input(filename: str) -> Input:
    obstacles = set()
    start = ((0, 0), (0, 0))

    with open(filename, "r") as f:
        the_map = [
            line.strip() for line in f.read().split('\n')
            if line.strip()
        ]

    for i, row in enumerate(the_map):
        for j, char in enumerate(row):
            if char == "#":
                obstacles.add((i, j))
            elif char == "^":
                start = ((i, j), (-1, 0))
            elif char == ">":
                start = ((i, j), (0, 1))
            elif char in ("v", "V"):
                start = ((i, j), (1, 0))
            elif char == "<":
                start = ((i, j), (0, -1))

    return Input(
        start=start,
        height=len(the_map),
        width=len(the_map[0]),
        obstacles=obstacles,
    )


def simulate(input: Input, additional_obstacle: tuple[int, int] = None) -> tuple[bool, set[tuple[int, int]]]:
    places_visited = set[tuple[int, int]]()
    states_visited = set[tuple[tuple[int, int], tuple[int, int]]]()

    location = input.start[0]
    direction = input.start[1]

    while (
        location[0] >= 0
        and location[0] < input.height
        and location[1] >= 0
        and location[1] < input.width
    ):
        places_visited.add(location)

        if ((location, direction)) in states_visited:
            return False, places_visited
        states_visited.add((location, direction))

        next_loc = (
            location[0] + direction[0],
            location[1] + direction[1],            
        )

        if next_loc in input.obstacles or next_loc == additional_obstacle:
            direction = (
                (0, 1) if direction == (-1, 0) else
                (1, 0) if direction == (0, 1) else
                (0, -1) if direction == (1, 0) else
                (-1, 0) # if direction == (0, -1) else ...
            )
        else:
            location = next_loc

    return True, places_visited

def part_1(input: Input):
    _, places_visited = simulate(input)

    return len(places_visited)

def part_2(input: Input):
    loops_created = 0
    for i in range(input.height):
        for j in range(input.width):
            adtl_obstacle = (i, j)
            if adtl_obstacle not in input.obstacles and adtl_obstacle != input.start[0]:
                exited, _ = simulate(input, adtl_obstacle)
                if not exited:
                    loops_created += 1
    return loops_created


if __name__ == "__main__":
    input = parse_input("input.txt")
    sample_input = parse_input("sample_input.txt")

    before = time.time_ns()
    result = part_1(sample_input)
    _time = (time.time_ns() - before) / 1_000_000

    print("Part 1 (sample):", result, f"({_time} ms)")

    before = time.time_ns()
    result = part_1(input)
    _time = (time.time_ns() - before) / 1_000_000

    print("Part 1:", result, f"({_time} ms)")

    before = time.time_ns()
    result = part_2(sample_input)
    _time = (time.time_ns() - before) / 1_000_000

    print("Part 2 (sample):", result, f"({_time} ms)")

    before = time.time_ns()
    result = part_2(input)
    _time = (time.time_ns() - before) / 1_000_000

    print("Part 2:", result, f"({_time} ms)")
