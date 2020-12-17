test_state = [
    [0, 1, 0,],
    [0, 0, 1,],
    [1, 1, 1,],
]

puzzle_input_state = [
    [1, 1, 0, 0, 0, 0, 1, 0,],
    [1, 0, 1, 0, 0, 1, 0, 0,],
    [0, 0, 0, 1, 0, 0, 0, 0,],
    [0, 0, 0, 1, 0, 1, 0, 0,],
    [1, 1, 1, 0, 0, 0, 0, 1,],
    [1, 0, 1, 0, 0, 0, 0, 1,],
    [0, 1, 0, 0, 0, 0, 1, 1,],
    [0, 1, 0, 1, 1, 1, 0, 1,],
]

import collections
from typing import List, Dict, Set, Iterable

def simulate_2d(state: List[List[int]], n: int) -> Set[tuple]:
    currently_active_cells = {
        (x, y)
        for y, row in enumerate(state)
        for x, value in enumerate(row)
        if value == 1
    }

    for _ in range(n):

        state_tracker = collections.defaultdict(int)
        for coords in currently_active_cells:
            for x in range(coords[0] - 1, coords[0] + 2):
                for y in range(coords[1] - 1, coords[1] + 2):
                    new_coords = (x, y)
                    if new_coords != coords:
                        state_tracker[new_coords] += 1

        next_state = set()
        for coords, num_neighbors in state_tracker.items():
            if coords in currently_active_cells and num_neighbors in [2, 3]:
                next_state.add(coords)
            elif coords not in currently_active_cells and num_neighbors == 3:
                next_state.add(coords)

        currently_active_cells = next_state

    return currently_active_cells

def simulate_3d(state: List[List[int]], n: int) -> Set[tuple]:
    currently_active_cells = {
        (x, y, 0)
        for y, row in enumerate(state)
        for x, value in enumerate(row)
        if value == 1
    }

    for _ in range(n):

        state_tracker = collections.defaultdict(int)
        for coords in currently_active_cells:
            for x in range(coords[0] - 1, coords[0] + 2):
                for y in range(coords[1] - 1, coords[1] + 2):
                    for z in range(coords[2] - 1, coords[2] + 2):
                        new_coords = (x, y, z)
                        if new_coords != coords:
                            state_tracker[new_coords] += 1

        next_state = set()
        for coords, num_neighbors in state_tracker.items():
            if coords in currently_active_cells and num_neighbors in [2, 3]:
                next_state.add(coords)
            elif coords not in currently_active_cells and num_neighbors == 3:
                next_state.add(coords)

        currently_active_cells = next_state

    return currently_active_cells

def simulate_4d(state: List[List[int]], n: int) -> Set[tuple]:
    currently_active_cells = {
        (x, y, 0, 0)
        for y, row in enumerate(state)
        for x, value in enumerate(row)
        if value == 1
    }

    for _ in range(n):

        state_tracker = collections.defaultdict(int)
        for coords in currently_active_cells:
            for x in range(coords[0] - 1, coords[0] + 2):
                for y in range(coords[1] - 1, coords[1] + 2):
                    for z in range(coords[2] - 1, coords[2] + 2):
                        for w in range(coords[3] - 1, coords[3] + 2):
                            new_coords = (x, y, z, w)
                            if new_coords != coords:
                                state_tracker[new_coords] += 1

        next_state = set()
        for coords, num_neighbors in state_tracker.items():
            if coords in currently_active_cells and num_neighbors in [2, 3]:
                next_state.add(coords)
            elif coords not in currently_active_cells and num_neighbors == 3:
                next_state.add(coords)

        currently_active_cells = next_state

    return currently_active_cells


def simulate(state: List[List[int]], n: int, d: int) -> Set[tuple]:
    currently_active_cells = {
        (x, y, *(0 for _ in range(d-2)))
        for y, row in enumerate(state)
        for x, value in enumerate(row)
        if value == 1
    }

    def neighboring_coords(coordinate: tuple) -> Iterable[tuple]:
        def _neighboring_coords(index: int, coordinate: tuple) -> Iterable[tuple]:
            if index >= len(coordinate):
                yield ()
            else:
                yield from (
                    _
                    for tuple_ in _neighboring_coords(index + 1, coordinate)
                    for _ in (
                        (1 + coordinate[index], *tuple_),
                        (0 + coordinate[index], *tuple_),
                        (-1 + coordinate[index], *tuple_),
                    )
                    if _ != coordinate
                )

        return _neighboring_coords(0, coordinate)

    for _ in range(n):

        state_tracker = collections.defaultdict(int)
        for coords in currently_active_cells:
            for new_coord in neighboring_coords(coords):
                if new_coord != coords:
                    state_tracker[new_coord] += 1

        next_state = set()
        for coords, num_neighbors in state_tracker.items():
            if coords in currently_active_cells and num_neighbors in [2, 3]:
                next_state.add(coords)
            elif coords not in currently_active_cells and num_neighbors == 3:
                next_state.add(coords)

        currently_active_cells = next_state

    return currently_active_cells

test_1 = simulate(state=test_state, n=6, d=3)
assert len(test_1) == 112
part_1 = simulate(state=puzzle_input_state, n=6, d=3)
print("Part 1:", len(part_1))

test_2 = simulate(state=test_state, n=6, d=4)
assert len(test_2) == 848
part_2 = simulate(state=puzzle_input_state, n=6, d=4)
print("Part 2:", len(part_2))
