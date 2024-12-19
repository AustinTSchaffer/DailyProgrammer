import re
import dataclasses
import time
from typing import Any, Iterable

@dataclasses.dataclass
class Input:
    available_patterns: dict[str, list[str]]
    designs: list[str]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.read()

    available_patterns_raw, designs = data.split('\n\n')
    available_patterns_list = sorted(list(map(str.strip, available_patterns_raw.split(','))))

    available_patterns = {}
    for pattern in available_patterns_list:
        if (pattern_list := available_patterns.get(pattern[0])) is not None:
            pattern_list.append(pattern)
        else:
            available_patterns[pattern[0]] = [pattern]

    designs = list(map(str.strip, designs.split('\n')))
    return Input(
        available_patterns=available_patterns,
        designs=designs,
    )

_design_assembly_cache = {}
def design_can_be_assembled(design: str, available_patterns: dict[str, list[str]]) -> int:
    """
    Returns the number of possible arrangements of "available_patterns" that can be
    used to assemble the "design". "available_patterns" must be a collection of patterns
    partitioned by their starting letters.
    """

    cache_key = (design, id(available_patterns))
    if (prior_result := _design_assembly_cache.get(cache_key)) is not None:
        return prior_result

    if len(design) == 0:
        return 1

    valid_permutations = 0
    for pattern in available_patterns.get(design[0], []):
        if design.startswith(pattern):
            remainder = design[len(pattern):]
            valid_permutations += design_can_be_assembled(remainder, available_patterns)

    _design_assembly_cache[cache_key] = valid_permutations
    return valid_permutations


def part_1(input: Input):
    return sum(1 for d in input.designs if design_can_be_assembled(d, input.available_patterns))

def part_2(input: Input):
    return sum(design_can_be_assembled(d, input.available_patterns) for d in input.designs)

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
