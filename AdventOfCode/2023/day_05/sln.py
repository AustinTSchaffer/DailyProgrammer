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

@dataclasses.dataclass
class SrcToDstMap:
    range_info: list[MappingRange]

    def map_source(self, source: int) -> int:
        mapped_value = None

        for range in self.range_info:
            if (destination := range.get_dst(source)) is not None:
                if mapped_value is None:
                    mapped_value = destination
                else:
                    raise ValueError("Yes, this should return a list.")

        return mapped_value if mapped_value is not None else source


greedy_int_re = re.compile(r'\d+')
src_to_dst_map_re = re.compile(r'(?P<dst_range_start>\d+) (?P<src_range_start>\d+) (?P<range_len>\d+)')

# Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

@dataclasses.dataclass
class Input:
    seeds: list[int]
    seed_to_soil_map: SrcToDstMap
    soil_to_fert_map: SrcToDstMap
    fert_to_water_map: SrcToDstMap
    water_to_light_map: SrcToDstMap
    light_to_temp_map: SrcToDstMap
    temp_to_humid_map: SrcToDstMap
    humid_to_loc_map: SrcToDstMap

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


    def get_location(self, seed: int) -> int:
        maps = [
            self.seed_to_soil_map,
            self.soil_to_fert_map,
            self.fert_to_water_map,
            self.water_to_light_map,
            self.light_to_temp_map,
            self.temp_to_humid_map,
            self.humid_to_loc_map,
        ]

        return functools.reduce(lambda prev, map_: map_.map_source(prev), maps, seed)


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

        return Input(parsed_seeds, *map(SrcToDstMap, parsed_mapping_sections))

def part_1(input: Input):
    min_ = None
    for seed in input.seeds:
        location = input.get_location(seed)
        if min_ is None or location < min_:
            min_ = location
    return min_

def part_2(input: Input, num_samples_per_range = 100000) -> tuple[int, int]:
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

    current_seed = min_location_seed
    while current_seed >= min_location_parent_range[0]:
        current_seed -= 1
        location = input.get_location(current_seed)
        total_locations_calculated += 1

        if location > min_location:
            break

        min_location = location

    return min_location, total_locations_calculated

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

    part_2_result = part_2(sample_input, 10)
    print('Part 2 (sample):', part_2_result[0])
    print(f'\tGenerated {part_2_result[1]:,} locations\n\tTotal seeds: {sample_input.total_numbers_to_consider():,}\n\tPercentage of seed space searched: {(part_2_result[1]/sample_input.total_numbers_to_consider())*100:.4}%')

    part_2_result = part_2(input, 10_000)
    print('Part 2:', part_2_result[0])
    print(f'\tGenerated {part_2_result[1]:,} locations\n\tTotal seeds: {input.total_numbers_to_consider():,}\n\tPercentage of seed space searched: {(part_2_result[1]/input.total_numbers_to_consider())*100:.4}%')

