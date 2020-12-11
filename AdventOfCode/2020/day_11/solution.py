# %%

seat_layout = [
    list(line.strip())
    for line in
    open("seat_layout.txt").readlines()
]

FLOOR = "."
OPEN_SEAT = "L"
OCCUPIED = "#"

def copy_seat_layout(seat_layout):
    return [
        list(row)
        for row in
        seat_layout
    ]

# %% Part 1

def in_bounds(row, col, seat_layout):
    return (
        row >= 0 and row < len(seat_layout) and
        col >= 0 and col < len(seat_layout[row])
    )

def get_neighbors(row, col, seat_layout):
    return [
        seat_layout[_row][_col]
        for _row in range(row - 1, row + 2)
        for _col in range(col - 1, col + 2)
        if (
            (_row, _col) != (row, col) and
            in_bounds(_row, _col, seat_layout)
        )
    ]

def simulate(seat_layout, get_neighbors_alg=get_neighbors, crowded_threshold=4):
    next_state = copy_seat_layout(seat_layout)
    anything_changed = True

    while anything_changed:
        current_state = next_state
        next_state = copy_seat_layout(current_state)

        anything_changed = False
        for row_index, row in enumerate(current_state):
            for col_index, seat in enumerate(row):
                if seat == OPEN_SEAT:
                    neighbors = get_neighbors_alg(row_index, col_index, current_state)
                    if neighbors.count(OCCUPIED) <= 0:
                        anything_changed = True
                        next_state[row_index][col_index] = OCCUPIED
                elif seat == OCCUPIED:
                    neighbors = get_neighbors_alg(row_index, col_index, current_state)
                    if neighbors.count(OCCUPIED) >= crowded_threshold:
                        anything_changed = True
                        next_state[row_index][col_index] = OPEN_SEAT

    return current_state

def seats_occupied(seat_layout):
    return sum((
        row.count(OCCUPIED)
        for row in seat_layout
    ))

print("Part 1:", seats_occupied(simulate(seat_layout)))

# %% Part 2

def get_line_of_sight_neighbors(row, col, seat_layout):
    los_neighbors = []
    directions = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    for d_row, d_col in directions:
        _row, _col = row + d_row, col + d_col
        while in_bounds(_row, _col, seat_layout):
            value = seat_layout[_row][_col]
            if value != FLOOR:
                los_neighbors.append(value)
                break

            _row, _col = _row + d_row, _col + d_col

    return los_neighbors

print("Part 2:", seats_occupied(simulate(seat_layout, get_line_of_sight_neighbors, crowded_threshold=5)))

# %%
