import dataclasses

@dataclasses.dataclass(frozen=True)
class Input:
    start: tuple[int, int]
    splitters: set[tuple[int, int]]
    height: int

def transform(input: str) -> Input:
    start = None
    splitters = set()
    rows = input.splitlines()
    for row_idx, row in enumerate(rows):
        for col_idx, cell in enumerate(row):
            if cell == 'S':
                start = (row_idx, col_idx)
            elif cell == '^':
                splitters.add((row_idx, col_idx))
            elif cell == '.':
                ...
            else:
                raise ValueError(cell)

    return Input(start=start, splitters=splitters, height=len(rows))

def part_1(input: Input):
    times_split = 0
    tb_frontier = {input.start}

    while tb_frontier:
        next_tb_frontier = set()
        for tb in tb_frontier:
            if tb[0] > input.height:
                continue

            next_pos = (tb[0] + 1, tb[1])
            if next_pos in input.splitters:
                times_split += 1
                next_tb_frontier.add((tb[0] + 1, tb[1] - 1))
                next_tb_frontier.add((tb[0] + 1, tb[1] + 1))
            else:
                next_tb_frontier.add(next_pos)

        tb_frontier = next_tb_frontier

    return times_split


def part_2(input: Input):
    # Holds the unique locations of tachyon beams for an advancing wave
    # of tachyon beams. Assigned to each unique location is the number
    # of paths that a tachyon particle can follow to arrive at that
    # location. This propagates forward information about the number
    # timelines that have been generated so far.
    #
    # This could/should use a defaultdict(int), but I'm sick of importing
    # them every year for AoC.
    tb_frontier = {input.start: 1}

    while True:
        next_tb_frontier = {}
        for tb, n_timelines in tb_frontier.items():
            if tb[0] > input.height:
                # Once we're past the last splitter, the total number of timelines
                # is equal to the sum total of the number of ways that a tachyon
                # particle can reach each unique location in the frontier.
                return sum(tb_frontier.values())

            next_pos = (tb[0] + 1, tb[1])
            if next_pos in input.splitters:
                next_pos_l = (tb[0] + 1, tb[1] - 1)
                next_pos_r = (tb[0] + 1, tb[1] + 1)

                next_tb_frontier[next_pos_l] = next_tb_frontier.get(next_pos_l, 0) + n_timelines
                next_tb_frontier[next_pos_r] = next_tb_frontier.get(next_pos_r, 0) + n_timelines
            else:
                next_tb_frontier[next_pos] = next_tb_frontier.get(next_pos, 0) + n_timelines

        tb_frontier = next_tb_frontier
