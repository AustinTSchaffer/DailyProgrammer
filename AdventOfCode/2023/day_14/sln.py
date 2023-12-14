import re
import dataclasses

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

def part_2(input: Input):
    # Roll the boulders North, West, South, East iteratively.
    # Store data as to check for a cycle.
    #    - Store post shifting results as a tuple of tuples and hash them?
    #    - Use a dict for the tup-o-tups, along with instruction index, map to iteration number?
    # Figure out where in the cycle 1_000_000_000 repetitions will be.
    # Calculate load.
    history: dict[tuple[int, tuple[int, int]], int] = {}
    current_state = tuple(input.spheres)
    instruction = -1

    for iteration in range(1_000_000_000):
        instruction = (instruction + 1) % 4
        history[(instruction, current_state)] = 0
        ...
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
