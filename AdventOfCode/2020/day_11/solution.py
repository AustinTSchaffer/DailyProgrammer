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

def simulate(seat_layout):
    output = copy_seat_layout(seat_layout)
    anything_changed = False

    for row_index, row in enumerate(seat_layout):
        for col_index, seat in enumerate(row):
            neighbors = get_neighbors(row_index, col_index, seat_layout)
            if seat == OPEN_SEAT:
                if neighbors.count(OCCUPIED) <= 0:
                    anything_changed = True
                    output[row_index][col_index] = OCCUPIED
            elif seat == OCCUPIED:
                if neighbors.count(OCCUPIED) >= 4:
                    anything_changed = True
                    output[row_index][col_index] = OPEN_SEAT

    return output, anything_changed

simulated_seat_layout = seat_layout
anything_changed = True
while anything_changed:
    simulated_seat_layout, anything_changed = simulate(simulated_seat_layout)

seats_occupied = sum((
    row.count(OCCUPIED)
    for row in simulated_seat_layout
))

print("Part 1:", seats_occupied)
