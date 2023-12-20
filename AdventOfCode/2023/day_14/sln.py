import re
import dataclasses
import itertools
import timeit

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

    # Immutable, pre-rotated maps of where the cubes are.
    rotated_cubes_maps: list[set] = [[False] * input.width * input.height for _ in range(4)]
    for cube in input.cubes:
        rotated_cubes_maps[0][(cube[0] * input.width) + cube[1]] = True
        rotated_cubes_maps[1][(cube[1] * input.height) + (rot_i := (input.height - cube[0] - 1))] = True
        rotated_cubes_maps[2][(rot_i * input.width) + (rot_j := (input.width - cube[1] - 1))] = True
        rotated_cubes_maps[3][(rot_j * input.height) + cube[0]] = True

    # Mutable structure for tracking where the spheres are.
    spheres_after_rolling = [False] * input.width * input.height
    current_state_temp = [None] * len(input.spheres)

    state_to_iteration_map: dict[tuple[tuple[int, int], ...], int] = {}
    current_state_history: list[tuple[tuple[int, int], ...]] = []
    current_state = tuple(sorted(input.spheres))

    for current_iteration in range(total_iterations):
        if (repeated_iteration := state_to_iteration_map.get(current_state)) is not None:
            cycle_length = current_iteration - repeated_iteration

            # Lookup what the current state will be at iteration (1B-1)
            ending_iteration = ((total_iterations - current_iteration) % cycle_length) + repeated_iteration
            final_state = current_state_history[ending_iteration]

            return sum(
                input.height - s[0]
                for s in final_state
            )

        state_to_iteration_map[current_state] = current_iteration
        current_state_history.append(current_state)

        for instruction in range(4):
            cube_map = rotated_cubes_maps[instruction]
            height = input.height if instruction % 2 == 0 else input.width
            width = input.width if instruction % 2 == 0 else input.height

            # Reset
            for i in range(len(spheres_after_rolling)):
                spheres_after_rolling[i] = False

            for sphere in current_state:
                for i in range(sphere[0], -1, -1):
                    if i == 0:
                        spheres_after_rolling[sphere[1]] = True
                        break

                    curr_loc = (i * width) + sphere[1]
                    test_loc = curr_loc - width

                    if spheres_after_rolling[test_loc] or cube_map[test_loc]:
                        spheres_after_rolling[curr_loc] = True
                        break

            cs_idx = 0
            for idx, is_sphere in enumerate(spheres_after_rolling):
                i, j = idx // width, idx % width
                if is_sphere:
                    current_state_temp[cs_idx] = (j, ((height - i) - 1))
                    cs_idx += 1
                spheres_after_rolling[idx] = False

            current_state = current_state_temp
        current_state = tuple(current_state)

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')
    tiny_input = parse_input('tiny_input.txt')

    globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals = globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals = globals
    )

    print('Part 1 (sample):', part_1(sample_input))
    time = part_1_timer.timeit(1)
    print('Part 1:', globals['result'], f'({time:.3} seconds)')

    # print('Part 2 (tiny):', part_2(tiny_input))
    print('Part 2 (sample):', part_2(sample_input))
    time = part_2_timer.timeit(1)
    print('Part 2:', globals['result'], f'({time:.3} seconds)')
