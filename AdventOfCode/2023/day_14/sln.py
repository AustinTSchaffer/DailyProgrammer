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


def part_2_sets(input: Input, total_iterations=1_000_000_000):
    """
    - Uses cached sets of tuples to represent the locations for cube rocks
      for each of the 4 distinct orientations.
    - Uses a tuple to represent the current state of the sphere rocks.
    - Slides each sphere rock individually within its column.
    - History is implemented as a bi-directional dict:
      - iteration (int) -> state (tuple)
      - state (tuple) -> iteration (int)
    """

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

            spheres_after_rolling_rotated = [None] * len(spheres_after_rolling)
            for idx, (i, j) in enumerate(spheres_after_rolling):
                spheres_after_rolling_rotated[idx] = (j, (input.width if instruction % 2 == 0 else input.height) - 1 - i)

            current_state = tuple(sorted(spheres_after_rolling_rotated))


def part_2_sets_better_tilting(input: Input, total_iterations=1_000_000_000):
    """
    - Uses cached sets of tupls to represent the locations for cube rocks
      for each of the 4 distinct orientations.
    - Uses a tuple/set to represent the current state of the sphere rocks.
    - Slides each sphere rock individually within its column.
    - History is implemented with 2 data structures
      - list of states so far (maps iteration -> state)
      - dict of state -> iteration
    """

    history_dict: dict[tuple[tuple[int, int], ...], int] = {}
    history_list: list[tuple[tuple[int, int], ...]] = []
    current_state = tuple(sorted(input.spheres))

    rotated_cubes_maps: list[set] = [set(sorted(input.cubes)), set(), set(), set()]

    for iter_, (source_cm, dest_cm) in enumerate(itertools.pairwise(rotated_cubes_maps)):
        for i, j in source_cm:
            dest_cm.add((j, (input.width if iter_ % 2 == 0 else input.height) - 1 - i))

    for current_iteration in range(total_iterations):
        if (repeated_iteration := history_dict.get(current_state)) is not None:
            cycle_length = current_iteration - repeated_iteration

            # Lookup what the current state will be at iteration (1B-1)
            ending_iteration = ((total_iterations - current_iteration) % cycle_length) + repeated_iteration
            final_state = history_list[ending_iteration]

            return sum(
                input.height - s[0]
                for s in final_state
            )

        history_dict[current_state] = current_iteration
        history_list.append(current_state)

        for instruction in range(4):
            cube_map = rotated_cubes_maps[instruction]
            width = (input.width if instruction % 2 == 0 else input.height)
            height = (input.height if instruction % 2 == 0 else input.width)

            current_state = set(current_state)
            spheres_after_rolling = [None] * len(current_state)
            sar_idx = 0
            for j in range(width):
                num_spheres = 0
                last_cube_i = -1
                for i in range(height):
                    if (i, j) in cube_map:
                        for sphere_i in range(1 + last_cube_i, 1 + last_cube_i + num_spheres):
                            spheres_after_rolling[sar_idx] = (sphere_i, j)
                            sar_idx += 1
                        last_cube_i = i
                        num_spheres = 0
                    if (i, j) in current_state:
                        num_spheres += 1

                for sphere_i in range(1 + last_cube_i, 1 + last_cube_i + num_spheres):
                    spheres_after_rolling[sar_idx] = (sphere_i, j)
                    sar_idx += 1

            spheres_after_rolling_rotated = [None] * len(spheres_after_rolling)
            for idx, (i, j) in enumerate(spheres_after_rolling):
                spheres_after_rolling_rotated[idx] = (j, width - 1 - i)

            current_state = tuple(sorted(spheres_after_rolling_rotated))


def part_2_1d_arrays(input: Input, total_iterations=1_000_000_000):
    """
    - Uses cached 1D arrays of bools to represent the locations for cube rocks.
    - Uses a tuple to represent the current state of the sphere rocks.
    - Slides each sphere rock individually within its column.
    - History is implemented with 2 data structures
      - list of states so far (maps iteration -> state)
      - dict of state -> iteration
    """

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



def part_2_2D_array_better_tilting(input: Input, total_iterations=1_000_000_000):
    """
    - Uses cached 2D arrays of bools to represent the locations for cube rocks,
      for each unique orientation.
    - Uses a tuple/set to represent the current state of the sphere rocks.
    - Performs each tilt by counting the number of spheres in between cubes in a
      particular column.
    - History is implemented with 2 data structures
      - list of states so far (maps iteration -> state)
      - dict of state -> iteration
    """

    # Immutable, pre-rotated maps of where the cubes are.
    rotated_cubes_maps: list[list[list[bool]]] = [
        [
            [
                False for _ in
                range(input.width if i % 2 == 0 else input.height)
            ]
            for _ in range(input.height if i % 2 == 0 else input.width)
        ] * input.width * input.height
        for i in range(4)
    ]

    for i in range(input.height):
        for j in range(input.width):
            if (i, j) in input.cubes:
                rotated_cubes_maps[0][i][j] = True
                rotated_cubes_maps[1][j][input.height - i - 1] = True
                rotated_cubes_maps[2][input.height - i - 1][input.width - j - 1] = True
                rotated_cubes_maps[3][input.width - j - 1][i] = True

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

            current_state = set(current_state)
            spheres_after_rolling = [None] * len(current_state)
            sar_idx = 0

            for j in range(width):
                last_cube_i = -1
                num_spheres = 0
                for i in range(height):
                    if cube_map[i][j]:
                        for sphere_i in range(1 + last_cube_i, 1 + last_cube_i + num_spheres):
                            spheres_after_rolling[sar_idx] = (sphere_i, j)
                            sar_idx += 1
                        last_cube_i = i
                        num_spheres = 0
                    if (i, j) in current_state:
                        num_spheres += 1
                for sphere_i in range(1 + last_cube_i, 1 + last_cube_i + num_spheres):
                    spheres_after_rolling[sar_idx] = (sphere_i, j)
                    sar_idx += 1

            current_state_rot = [None] * len(current_state)
            for idx, (i, j) in enumerate(spheres_after_rolling):
                current_state_rot[idx] = (j, ((height - i) - 1))

            current_state = current_state_rot
        current_state = tuple(current_state)


if __name__ == '__main__':
    sample_input = parse_input('sample_input.txt')
    tiny_input = parse_input('tiny_input.txt')
    input = parse_input('input.txt')

    timeit_globals = {'input': input, 'part_1': part_1, 'part_2': part_2_1d_arrays}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals = timeit_globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals = timeit_globals
    )

    print('Part 1 (sample):', part_1(sample_input))
    time = part_1_timer.timeit(1)
    print('Part 1:', timeit_globals['result'], f'({time:.3} seconds)')

    print()

    # print('Part 2 (tiny):', part_2(tiny_input))
    print('Part 2 (sample, sets):', part_2_sets(sample_input))
    print('Part 2 (sample, 1D arrays):', part_2_1d_arrays(sample_input))
    print('Part 2 (sample, sets, better tilting):', part_2_sets_better_tilting(sample_input))
    print('Part 2 (sample, 2D arrays, better tilting):', part_2_2D_array_better_tilting(sample_input))

    print()

    timeit_globals['part_2'] = part_2_sets
    time = part_2_timer.timeit(1)
    print('Part 2 (sets):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['part_2'] = part_2_1d_arrays
    time = part_2_timer.timeit(1)
    print('Part 2 (1D arrays):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['part_2'] = part_2_sets_better_tilting
    time = part_2_timer.timeit(1)
    print('Part 2 (sets, better tilting):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['part_2'] = part_2_2D_array_better_tilting
    time = part_2_timer.timeit(1)
    print('Part 2 (2D arrays, better tilting):', timeit_globals['result'], f'({time:.3} seconds)')
