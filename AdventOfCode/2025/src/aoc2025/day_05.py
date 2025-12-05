import dataclasses

@dataclasses.dataclass(frozen=True)
class Input:
    ranges: list[tuple[int, int]]
    ids: list[int]

def transform(input: str) -> Input:
    ranges, ids = input.split('\n\n')
    ranges = [
        tuple([int(v) for v in line.split('-')])
        for line in ranges.split()
        if line
    ]

    ids = [
        int(id_)
        for id_ in ids.split()
        if id_
    ]

    return Input(
        ranges=ranges,
        ids=ids,
    )

def part_1(input: Input):
    n_fresh = 0
    for id_ in input.ids:
        is_fresh = False
        for left, right in input.ranges:
            if id_ >= left and id_ <= right:
                is_fresh = True
                break
        if is_fresh:
            n_fresh += 1
    return n_fresh

def part_2(input: Input):
    sorted_ranges = sorted(input.ranges)
    combined_ranges = [sorted_ranges[0]]
    for range_ in sorted_ranges[1:]:
        if range_[0] <= combined_ranges[-1][1]:
            combined_ranges[-1] = (
                combined_ranges[-1][0],
                max(combined_ranges[-1][1], range_[1])
            )
        else:
            combined_ranges.append(range_)
    
    total_fresh = sum(
        right - left + 1
        for left, right in combined_ranges
    )

    return total_fresh
