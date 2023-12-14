import re
import dataclasses

@dataclasses.dataclass
class BrokenSprings:
    known: str
    lens: list[int]

def parse_input(filename: str) -> list[BrokenSprings]:
    data = []
    with open(filename, 'r') as f:
        for row in f:
            info, segment_lens = row.strip().split()
            data.append(BrokenSprings(
                known=info,
                lens=[
                    int(len_)
                    for len_ in
                    segment_lens.split(',')
                ]
            ))

    return data


def num_valid_arrangements(info: BrokenSprings) -> int:
    known, lens = info.known, info.lens
    def can_start_at(run_len: int, idx: int):
        if idx < 0 or (idx + run_len) >= len(known):
            return False

        if (after := idx + run_len) < len(known):
            if known[after] == '#':
                return False

        if (before := idx - 1) >= 0:
            if known[before] == '#':
                return False

        for i in range(run_len):
            if known[idx + i] == '.':
                return False

        return True

    wiggle_room = len(known) - sum(lens) - (len(lens) - 1)
    if wiggle_room < 0:
        raise ValueError(f"{known} {lens}")
    
    if wiggle_room == 0:
        return 1

    for i in range(wiggle_room):
        remaining_room = wiggle_room - i
        can_start_at(1, i)
        # TODO: Calculate offsets
    return 1

def part_1(input: list[BrokenSprings]):
    return sum(map(num_valid_arrangements, input))

def part_2(input: list[BrokenSprings]):
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
