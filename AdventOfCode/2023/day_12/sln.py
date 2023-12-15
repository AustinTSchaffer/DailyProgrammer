import re
import dataclasses
import itertools
from typing import Iterable

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
    broken_spring_mask = [c=='#' for c in known]

    def can_start_at(run_idx: int, run_len: int, idx: int):
        """
        Returns true if
        - All of the indices of the length are in bounds.
        - There are no broken springs directly before/after the length.
        - There are no explicitly "good" springs contained within the length.

        Additionally checks to make sure that the length doesn't exclude any broken
        springs, in the event that the length is the first or last entry in `lens`.

        TODO: This can absolutely be optimized. It redoes a lot of work when you pass
        in a length at index 0, then again at index 1. This was not the most
        inefficient part of the initial solution, and the economic incentive for
        improving it is arguably worse than $0.
        """

        if run_idx == 0 and any(s for s in broken_spring_mask[0:idx] if s):
            return False

        if run_idx == (len(lens) - 1) and any(s for s in broken_spring_mask[idx+run_len:] if s):
            return False

        if idx < 0 or (idx + run_len) > len(known):
            return False

        if (after := idx + run_len) < len(known):
            if broken_spring_mask[after]:
                return False

        if (before := idx - 1) >= 0:
            if broken_spring_mask[before]:
                return False

        for i in range(run_len):
            if known[idx + i] == '.':
                return False

        return True

    # The amount of "flex" that the lengths have within the
    # map of springs, based on putting at least a gap of 1
    # between all of the lengths.
    wiggle_room = len(known) - sum(lens) - (len(lens) - 1)
    if wiggle_room < 0:
        raise ValueError(f"{known} {lens}")

    # Trivial case.
    if wiggle_room == 0:
        return 1

    # Collects the absolute minimum starting locations for each
    # of the lengths, plus a list of lists, recording all of the
    # positions where each of the lengths _could_ be.
    minimum_starts: list[int] = [None] * len(lens)
    allowed_positions: list[list[int]] = [None] * len(lens)

    for i, val in enumerate(lens):
        if i == 0:
            minimum_starts[i] = 0
        else:
            minimum_starts[i] = minimum_starts[i-1] + lens[i-1] + 1

        allowed_positions[i] = []
        for j in range(wiggle_room+1):
            if can_start_at(i, val, x := minimum_starts[i] + j):
                allowed_positions[i].append(x)

    # For each allowed position for each continuous run of broken springs, make sure that there are no overlaps.
    def non_overlapping_combinations() -> Iterable[tuple[int, ...]]:
        def non_o_combo(depth: int):
            if depth == len(allowed_positions) - 1:
                yield from (
                    (x,) for x in
                    allowed_positions[depth]
                )
            else:
                for idx, position in enumerate(allowed_positions[depth]):
                    for combo in non_o_combo(depth+1):
                        if position + lens[depth] + 1 <= combo[0]:
                            yield (position, *combo)

        # TODO: This is slow as hell. Caching might help.
        return non_o_combo(0)

    print("Generating non overlapping combinations.")

    total = 0
    for non_o_combo in non_overlapping_combinations():
        # make sure that all #'s are accounted for.
        is_valid_combination = all(
            any(c <= idx <= (c + lens[i]) for i, c in enumerate(non_o_combo))
            for idx, val in enumerate(known)
            if val == '#'
        )

        if is_valid_combination:
            total += 1

    return total

def part_1(input: list[BrokenSprings]):
    return sum(map(num_valid_arrangements, input))

def part_2(input: list[BrokenSprings]):
    total = 0
    for i, entry in enumerate(input):
        print(f"Working on {i}")
        total += num_valid_arrangements(BrokenSprings(
            '?'.join(entry.known for _ in range(5)),
            entry.lens * 5,
        ))

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample, x=21):', part_1(sample_input))
    print('Part 1 (x=7236):', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
