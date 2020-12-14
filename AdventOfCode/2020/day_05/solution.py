# %%

boarding_passes = [
    line.strip()
    for line in
    open("boarding_passes.txt").readlines()
]

def get_seat_id(boarding_pass: str) -> int:
    return int(
        (
            boarding_pass
            .replace("F", "0")
            .replace("B", "1")
            .replace("L", "0")
            .replace("R", "1")
        ),
        2
    )

seat_ids = list(map(
    get_seat_id,
    boarding_passes,
))

#%% Part 1

print("Part 1:", max(seat_ids))

#%% Part 2

import itertools

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

seat_ids_inorder = sorted(seat_ids)

for seat_a, seat_b in pairwise(seat_ids_inorder):
    if seat_a + 1 != seat_b:
        print("Part 2:", seat_a + 1)
        break
