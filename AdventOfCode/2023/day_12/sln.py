import re
import dataclasses
import itertools
from typing import Iterable
import functools
import timeit

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
    broken_spring_mask = [c == '#' for c in known]

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

    # Determines the valid positions of pairs of lengths, based on
    # the allowed starting positions of the 2 lengths, such that there
    # are no overlaps between them, and that there are no broken springs
    # ocurring in the range between the 2 lengths.
    network: list[dict[int, list[int]]] = []
    for i, (len_1, len_2) in enumerate(itertools.pairwise(lens)):
        local_graph = {}
        network.append(local_graph)
        for allowed_pos_1 in allowed_positions[i]:
            for allowed_pos_2 in allowed_positions[i+1]:
                pos_1_ending_idx = allowed_pos_1 + len_1
                if pos_1_ending_idx < allowed_pos_2 and not any(broken_spring_mask[j] for j in range(pos_1_ending_idx+1, allowed_pos_2)):
                    local_graph.setdefault(allowed_pos_1, []).append(allowed_pos_2)

    #
    # Now we just need to find all of the routes through the network. Ez pz.
    #
                    
    # Seed the results from the last layer in the network.
    num_routes_aggregated = {
        k: len(v)
        for k,v in
        network[-1].items()
    }

    # For the rest of the layers in reverse...
    for layer in network[-2::-1]:
        next_agg = {}
        for position, next_positions in layer.items():
            next_agg[position] = 0
            for next_position in next_positions:
                if next_position in num_routes_aggregated:
                    next_agg[position] += num_routes_aggregated[next_position]
        num_routes_aggregated = next_agg

    return sum(num_routes_aggregated.values())

def part_1(input: list[BrokenSprings]):
    return sum(map(num_valid_arrangements, input))

def part_2(input: list[BrokenSprings]):
    total = 0
    for i, entry in enumerate(input):
        total += num_valid_arrangements(BrokenSprings(
            '?'.join(entry.known for _ in range(5)),
            entry.lens * 5,
        ))
    return total

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

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

    print('Part 2 (sample):', part_2(sample_input))
    time = part_2_timer.timeit(1)
    print('Part 2:', globals['result'], f'({time:.3} seconds)')
