import re
import dataclasses
import functools
import itertools

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

    def iter_seed_ranges(self) -> list[int]:
        for start, length in itertools.batched(self.seeds, 2):
            yield from range(start, start + length)

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

def part_2(input: Input):
    min_ = None
    for i, seed in enumerate(input.iter_seed_ranges()):
        if i % 1000000 == 0:
            print("Processing seed number", i)
        location = input.get_location(seed)
        if min_ is None or location < min_:
            min_ = location
    return min_

if __name__ == '__main__':
    sample_input = parse_input('sample_input.txt')
    input = parse_input('input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print(f'Part 2 (sample): Processing {sample_input.total_numbers_to_consider()} seeds...')
    print('Part 2 (sample):', part_2(sample_input))

    print(f'Part 2: Processing {input.total_numbers_to_consider()} seeds...')
    print('Part 2:', part_2(input))
