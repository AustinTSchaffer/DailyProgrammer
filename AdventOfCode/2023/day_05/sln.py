import re
import dataclasses
import functools
import itertools
import random

@dataclasses.dataclass
class MappingRange:
    src_range_start: int
    dst_range_start: int
    range_len: int

    def has_src(self, source: int) -> bool:
        return self.src_range_start <= source < (self.src_range_start + self.range_len)

    def get_dst(self, source: int) -> int | None:
        if not self.has_src(source):
            return None
        return (source - self.src_range_start) + self.dst_range_start


greedy_int_re = re.compile(r'\d+')
src_to_dst_map_re = re.compile(r'(?P<dst_range_start>\d+) (?P<src_range_start>\d+) (?P<range_len>\d+)')

# Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

@dataclasses.dataclass
class Input:
    seeds: list[int]
    maps: list[list[MappingRange]]

    def total_numbers_to_consider(self) -> int:
        """
        (for part 2)
        """

        return sum(
            length
            for _, length in
            itertools.batched(self.seeds, 2)
        )

    def seed_ranges(self) -> list[tuple[int, int]]:
        return [
            (start, start + length)
            for start, length in itertools.batched(self.seeds, 2)
        ]

    def iter_seed_ranges(self) -> list[int]:
        for range in self.seed_ranges():
            yield from (range[0], range[1])

    def map_source(self, mapping_ranges: list[MappingRange], source: int) -> int:
        for mapping_range in mapping_ranges:
            if (destination := mapping_range.get_dst(source)) is not None:
                return destination

        return source

    def get_location(self, seed: int) -> int:
        return functools.reduce(lambda prev, map_: self.map_source(map_, prev), self.maps, seed)


def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.read()
        seeds, *mapping_sections = data.split('\n\n')
        parsed_mapping_sections: list[list[MappingRange]] = [[] for _ in range(len(mapping_sections))]

        parsed_seeds = list(map(lambda match_: int(match_[0]), greedy_int_re.finditer(seeds)))
        for i, mapping_section in enumerate(mapping_sections):
            for match_ in src_to_dst_map_re.finditer(mapping_section):
                parsed_mapping_sections[i].append(MappingRange(
                    src_range_start=int(match_['src_range_start']),
                    dst_range_start=int(match_['dst_range_start']),
                    range_len=int(match_['range_len'])
                ))

        return Input(parsed_seeds, parsed_mapping_sections)

def part_1(input: Input):
    min_ = None
    for seed in input.seeds:
        location = input.get_location(seed)
        if min_ is None or location < min_:
            min_ = location
    return min_


def part_2(input: Input) -> int:
    """
    This algorithm iteratively passes entire seed ranges through entire mapping layers.
    As it progresses through mapping layers, individual seed ranges will potentially be
    split up into smaller ranges with differing offsets.

    This algorithm works because all of the individual mapping ranges in the input
    are of the form `f(x) = x + c`. Across an entire mapping layer, the function is not
    contiguous.

    To start, all of the seed ranges are initialized with a `c` value of 0. This signifies
    that all of the seed values are currently passing through the function `f(x) = x`.

    For each mapping layer, each of the ranges are checked against all of the maps to
    see if there are any overlaps. Overlaps are determined using the output of each
    range's current function. Any overlaps that are detected are stripped off of the
    range, have their `c` values updated, and are then pushed down to the next layer.
    The rest of the range is pushed back into the list of current functions being
    evaluated. If a range does not overlap with any of the maps, then it is also
    pushed down to the next layer without updating its output function.

    The part described above can probably be slightly optimized if the maximum range
    end of the layer is compared against the current function's lower bounds (and
    vice-versa), as that would definitively mean that the function cannot overlap
    with anything in the current layer.

    At the end of this algorithm, the `current_functions` list will contain the full
    function definition, aggregating the ranges and coefficients across all layers
    into a single set of transformers of the form `f(x) = x + c`, each with
    non-overlapping ranges.

    For the actual part 2 question, we can add the coefficients and the function range
    lower bounds to determine the minimum result that can be produced by that range.
    Taking the minimum across all ranges results in the function's global minimum.
    """

    # List if linear functions.
    #   0: Range start inclusive
    #   1: Range start exclusive
    #   2: Constant coefficient
    current_functions = [(*range_, +0) for range_ in input.seed_ranges()]
    for mapping_functions in input.maps:
        function_layer = [
            (
                m.src_range_start,
                m.src_range_start + m.range_len,
                m.dst_range_start - m.src_range_start
            )
            for m in mapping_functions
        ]

        functions_next_round = set()
        while len(current_functions) > 0:
            func = current_functions.pop(-1)
            found_overlap = False

            # This is the output of the source range after it has passed through
            # the layers above the current mapping ranges. This is the range
            # of values that must be compared with the input ranges on the
            # current layer.
            offset_src = (func[0] + func[2], func[1] + func[2])

            for layer_func in function_layer:
                if offset_src[0] < layer_func[0]:
                    if layer_func[0] < offset_src[1] <= layer_func[1]:
                        # ...ssss
                        #      mmmmm

                        current_functions.append((
                            func[0],
                            func[0] + (layer_func[0] - offset_src[0]),
                            func[2],
                        ))

                        functions_next_round.add((
                            func[0] + (layer_func[0] - offset_src[0]),
                            func[1],
                            func[2] + layer_func[2]
                        ))

                        found_overlap = True
                        break

                    elif offset_src[1] > layer_func[1]:
                        # ...sssssss...
                        #      mmm
                        current_functions.append((
                            func[0],
                            func[0] + (layer_func[0] - offset_src[0]),
                            func[2]
                        ))

                        functions_next_round.add((
                            func[0] + (layer_func[0] - offset_src[0]),
                            func[0] + (layer_func[0] - offset_src[0]) + (layer_func[1] - layer_func[0]),
                            func[2] + layer_func[2]
                        ))

                        current_functions.append((
                            func[0] + (layer_func[0] - offset_src[0]) + (layer_func[1] - layer_func[0]),
                            func[1],
                            func[2]
                        ))

                        found_overlap = True
                        break

                elif layer_func[0] <= offset_src[0] < layer_func[1]:
                    if offset_src[1] <= layer_func[1]:
                        #   ssss(s)
                        # mmmmmmmm
                        functions_next_round.add((
                            func[0],
                            func[1],
                            func[2] + layer_func[2],
                        ))

                        found_overlap = True
                        break

                    else:
                        #    sssss...
                        # mmmmmm
                        functions_next_round.add((
                            func[0],
                            func[0] + (layer_func[1] - offset_src[0]),
                            func[2] + layer_func[2]
                        ))

                        current_functions.append((
                            func[0] + (layer_func[1] - offset_src[0]),
                            func[1],
                            func[2]
                        ))

                        found_overlap = True
                        break

            if not found_overlap:
                functions_next_round.add(func)

        current_functions = list(functions_next_round)

    return min(r[0] + r[2] for r in current_functions), current_functions


def part_2_sampling_and_climbing(input: Input, num_samples_per_range = 100000) -> tuple[int, int]:
    seed_ranges = input.seed_ranges()

    total_locations_calculated = 0

    print("Generating samples...")

    min_location_parent_range = None
    min_location_seed = None
    min_location = None
    for i, seed_range in enumerate(seed_ranges):
        seed_generator = itertools.chain(
            (
                random.randint(seed_range[0], seed_range[1])
                for _ in range(num_samples_per_range)
            ),
            [
                seed_range[0],
                seed_range[1],
            ]
        )

        for seed in seed_generator:
            location = input.get_location(seed)
            if min_location is None or location < min_location:
                min_location = location
                min_location_seed = seed
                min_location_parent_range = seed_range

    total_locations_calculated += len(seed_ranges) * (num_samples_per_range + 2)

    print("Searching backwards...")

    best_seed = min_location_seed
    while best_seed >= min_location_parent_range[0]:
        best_seed -= 1
        location = input.get_location(best_seed)
        total_locations_calculated += 1

        if location > min_location:
            best_seed += 1
            break

        min_location = location

    return min_location, best_seed, min_location_parent_range, total_locations_calculated


def analyze_input(input_: Input):
    seed_ranges = input_.seed_ranges()

    sum_range_lengths = input_.total_numbers_to_consider()
    min_seed_number = min(range[0] for range in seed_ranges)
    max_seed_number = max(range[1] for range in seed_ranges)
    overall_range = max_seed_number - min_seed_number

    print(f"min_seed_number    :   {min_seed_number:,}")
    print(f"max_seed_number    : {max_seed_number:,}")
    print(f"overall_range      : {overall_range:,}")
    print(f"sum_range_lengths  : {sum_range_lengths:,}")

    def overlapping(r1, r2):
        if r2[0] < r1[0]:
            r1, r2 = r2, r1
        return (r1, r2) if r2[0] < r1[1] else None

    overlapping_ranges = {
        ors
        for i, range_1 in enumerate(seed_ranges)
        for j, range_2 in enumerate(seed_ranges)
        if i != j
        if (ors := overlapping(range_1, range_2)) is not None
    }

    sorted_seed_ranges = sorted(seed_ranges, key=lambda r: r[0])

    gap_lengths = [
        (range_2[0] - range_1[1])
        for (range_1, range_2) in itertools.pairwise(sorted_seed_ranges)
    ]

    print(f"overlapping_ranges : {overlapping_ranges}")
    print(f"gaps_lengths       : {gap_lengths}")
    print(f"total_seeds_dne    : {sum(gap_lengths):,}")

    import random

    full_sample_x = []
    full_sample_y = []

    for i, seed_range in enumerate(sorted_seed_ranges):
        num_random_samples = 10000
        sample = [0] * (num_random_samples + 2)
        sample[0] = seed_range[0]
        sample[-1] = seed_range[1]

        for j in range(num_random_samples):
            sample[j+1] = random.randint(seed_range[0]+1, seed_range[1]-1)

        values = [input.get_location(x) for x in sample]

        import matplotlib.pyplot as plt
        plt.scatter(sample, values)
        plt.suptitle(f"Seed Range {i+1} ({num_random_samples:,} samples)")
        plt.title(f"({seed_range[0]:,}) to ({seed_range[1]:,})")
        plt.savefig(f"./figures/seed_range_{i+1}.{seed_range[0]}-{seed_range[1]}.png")

        full_sample_x.extend(sample)
        full_sample_y.extend(values)

        plt.clf()

    plt.scatter(full_sample_x, full_sample_y)
    plt.title(f"All Seed Ranges")
    plt.savefig("./figures/all_seed_ranges.png")


if __name__ == '__main__':
    sample_input = parse_input('sample_input.txt')
    input = parse_input('input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    result, _ = part_2(sample_input)
    print('Part 2 (sample):', result)

    result, function_ranges = part_2(input)
    print('Part 2:', result)

    print('f(x) = {')
    for i, range in enumerate(sorted(function_ranges)):
        function_def = '\tx'
        if range[2] > 0:
            function_def += f' + {range[2]}'
        elif range[2] < 0:
            function_def += f' - {-range[2]}'
        
        function_def += f' for {range[0]:,} <= x < {range[1]:,}'
        if i < (len(function_ranges) - 1):
            function_def += ', and'
        else:
            function_def += '.'
        print(function_def)
    print('}')
