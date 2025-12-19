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

_adj_loc_cache = {}
def adj_locations(cache_key: int, input: list[list[bool]], row: int, col: int) -> list[tuple[int, int]]:
    if cache_key in _adj_loc_cache:
        input_adj_cache = _adj_loc_cache[cache_key]
    else:
        input_adj_cache = [[None for _ in range(len(input[row]))] for row in range(len(input))]
        _adj_loc_cache[cache_key] = input_adj_cache

    if input_adj_cache[row][col]:
        return input_adj_cache[row][col]

    _adj_locations = []
    for row_off, col_off in offsets:
        adj_row = row + row_off
        adj_col = col + col_off

        in_bounds = (
            adj_row >= 0
            and adj_row < len(input)
            and adj_col >= 0
            and adj_col < len(input[adj_row])
        )

        if in_bounds:
            _adj_locations.append((adj_row, adj_col))

    input_adj_cache[row][col] = _adj_locations
    return _adj_locations


def num_adj_rolls(cache_key: int, input: list[list[bool]], row: int, col: int) -> int:
    count = 0

    for adj_row, adj_col in adj_locations(cache_key, input, row, col):
        if input[adj_row][adj_col]:
            count += 1

    return count


def part_1(input: list[list[bool]]):
    cache_key = id(input)
    accessible_rolls = 0
    for row_idx, row in enumerate(input):
        for col_idx, is_roll in enumerate(row):
            if is_roll and (num_adj_rolls(cache_key, input, row_idx, col_idx) < 4):
                accessible_rolls += 1

    return accessible_rolls


def part_2(input: list[list[bool]]):
    cache_key = id(input)
    total_rolls_removed = 0

    # Placeholder value to get the ball rolling.
    first_time = True

    this_round = input
    rolls_removed_last_round = set()
    while first_time or rolls_removed_last_round:
        rolls_removed_this_round = set()
        next_round = [
            row.copy()
            for row in this_round
        ]

        if first_time:
            for row_idx, row in enumerate(this_round):
                for col_idx, is_roll in enumerate(row):
                    if not is_roll:
                        continue
                    if num_adj_rolls(cache_key, this_round, row_idx, col_idx) < 4:
                        next_round[row_idx][col_idx] = False
                        rolls_removed_this_round.add((row_idx, col_idx))

        else:
            for row_idx, col_idx in rolls_removed_last_round:
                for adj_loc in adj_locations(cache_key, this_round, row_idx, col_idx):
                    adj_row_idx, adj_col_idx = adj_loc
                    if this_round[adj_row_idx][adj_col_idx] and (num_adj_rolls(cache_key, this_round, adj_row_idx, adj_col_idx) < 4):
                        next_round[adj_row_idx][adj_col_idx] = False
                        rolls_removed_this_round.add(adj_loc)

        total_rolls_removed += len(rolls_removed_this_round)

        this_round = next_round
        rolls_removed_last_round = rolls_removed_this_round
        first_time = False

    return total_rolls_removed
