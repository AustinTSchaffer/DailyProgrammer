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

def get_neighbors(row, col, seat_layout):
    return [
        seat_layout[_row][_col]
        for _row in range(row - 1, row + 2)
        for _col in range(col - 1, col + 2)
        if (
            (_row, _col) != (row, col) and
            _row >= 0 and _row < len(seat_layout) and
            _col >= 0 and _col < len(seat_layout[row])
        )
    ]

def simulate(seat_layout, get_neighbors_alg=get_neighbors):
    next_state = copy_seat_layout(seat_layout)
    anything_changed = True

    while anything_changed:
        current_state = next_state
        next_state = copy_seat_layout(current_state)

        anything_changed = False
        for row_index, row in enumerate(current_state):
            for col_index, seat in enumerate(row):
                neighbors = get_neighbors_alg(row_index, col_index, current_state)
                if seat == OPEN_SEAT:
                    if neighbors.count(OCCUPIED) <= 0:
                        anything_changed = True
                        next_state[row_index][col_index] = OCCUPIED
                elif seat == OCCUPIED:
                    if neighbors.count(OCCUPIED) >= 4:
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


