def transform(input: str) -> set[tuple[int, int]]:
    output = []

    for row in input.split():
        output.append([char == "@" for char in row.strip()])

    return output


offsets = [
    (-1, -1),
    (-1, 0),
    (-1, +1),
    (0, -1),
    (0, +1),
    (+1, -1),
    (+1, 0),
    (+1, +1),
]


def num_adj_rolls(input: list[list[bool]], row: int, col: int) -> int:
    count = 0
    for row_off, col_off in offsets:
        adj_row = row + row_off
        adj_col = col + col_off

        cmp = (
            adj_row >= 0
            and adj_row < len(input)
            and adj_col >= 0
            and adj_col < len(input[adj_row])
            and input[adj_row][adj_col]
        )

        if cmp:
            count += 1

    return count


def part_1(input: list[list[bool]]):
    accessible_rolls = 0
    for row_idx, row in enumerate(input):
        for col_idx, is_roll in enumerate(row):
            if is_roll and (num_adj_rolls(input, row_idx, col_idx) < 4):
                accessible_rolls += 1

    return accessible_rolls


def part_2(input: list[list[bool]]):
    total_rolls_removed = 0
    rolls_removed_this_round = 1

    this_round = input
    while rolls_removed_this_round > 0:
        rolls_removed_this_round = 0
        next_round = []

        for row_idx, row in enumerate(this_round):
            next_round_row = []
            next_round.append(next_round_row)
            for col_idx, is_roll in enumerate(row):
                if not is_roll:
                    next_round_row.append(False)
                    continue
                if num_adj_rolls(this_round, row_idx, col_idx) < 4:
                    next_round_row.append(False)
                    rolls_removed_this_round += 1
                    total_rolls_removed += 1

                else:
                    next_round_row.append(True)

        this_round = next_round

    return total_rolls_removed
