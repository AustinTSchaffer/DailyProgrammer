import re
import dataclasses
import itertools

@dataclasses.dataclass
class Input:
    width: int
    height: int
    spheres: list[tuple[int, int]]
    cubes: set[tuple[int, int]]

def parse_input(filename: str) -> Input:
    cubes = set()
    spheres = []
    with open(filename, 'r') as f:
        for i, row in enumerate(f):
            for j, val in enumerate(row.strip()):
                if val == '#':
                    cubes.add((i, j))
                elif val == 'O':
                    spheres.append((i, j))

    return Input(
        cubes=cubes,
        spheres=spheres,
        height=i+1,
        width=j+1,
    )


def part_1(input: Input):
    spheres_after_rolling = set()
    for sphere in input.spheres:
        for i in range(sphere[0], -2, -1):
            if i == -1:
                spheres_after_rolling.add((0, sphere[1]))
                break

            test_loc = (i, sphere[1])
            if test_loc in spheres_after_rolling or test_loc in input.cubes:
                if (i+1, sphere[1]) in spheres_after_rolling:
                    ...
                spheres_after_rolling.add((i+1, sphere[1]))
                break

    assert len(spheres_after_rolling) == len(input.spheres)

    return sum(
        input.height - s[0]
        for s in spheres_after_rolling
    )

def part_2(input: Input, total_iterations=1_000_000_000):
    # Roll the boulders North, West, South, East iteratively.
    # Store data as to check for a cycle.
    #    - Store post shifting results as a tuple of tuples and hash them?
    #    - Use a dict for the tup-o-tups, along with instruction index, map to iteration number?
    # Figure out where in the cycle 1_000_000_000 repetitions will be.
    # Calculate load.
    history: dict[tuple[tuple[int, int], ...], int] | dict[int, tuple[tuple[int, int], ...]] = {}
    current_state = tuple(sorted(input.spheres))

    rotated_cubes_maps: list[set] = [set(sorted(input.cubes)), set(), set(), set()]

    for iter_, (source_cm, dest_cm) in enumerate(itertools.pairwise(rotated_cubes_maps)):
        for i, j in source_cm:
            dest_cm.add((j, (input.width if iter_ % 2 == 0 else input.height) - 1 - i))

    for current_iteration in range(total_iterations):
        if (repeated_iteration := history.get(current_state)) is not None:
            cycle_length = current_iteration - repeated_iteration

            # Lookup what the current state will be at iteration (1B-1)
            ending_iteration = ((total_iterations - current_iteration) % cycle_length) + repeated_iteration
            final_state = history[ending_iteration]

            return sum(
                input.height - s[0]
                for s in final_state
            )

        history[current_iteration] = current_state
        history[current_state] = current_iteration

        for instruction in range(4):
            cube_map = rotated_cubes_maps[instruction]

            spheres_after_rolling = set()
            for sphere in current_state:
                for i in range(sphere[0], -2, -1):
                    if i == -1:
                        spheres_after_rolling.add((0, sphere[1]))
                        break

                    test_loc = (i, sphere[1])
                    if test_loc in spheres_after_rolling or test_loc in cube_map:
                        spheres_after_rolling.add((i+1, sphere[1]))
                        break

            rotated = set()
            for i, j in spheres_after_rolling:
                rotated.add((j, (input.width if instruction % 2 == 0 else input.height) - 1 - i))

            current_state = tuple(sorted(rotated))


if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')
    tiny_input = parse_input('tiny_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (tiny):', part_2(tiny_input))
    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2 (99521<x<?):', part_2(input))
