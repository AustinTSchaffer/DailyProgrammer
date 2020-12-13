# %% 

directions = [
    (line[0], int(line[1:].strip()))
    for line in
    open("directions.txt").readlines()
]

# %% Part 1

from typing import Dict, Tuple, List

def simulate(directions: List[Tuple[str, int]]) -> Tuple[int, int, int]:
    x, y, rotation = 0, 0, 0

    def simulate_nesw(action, value):
        nonlocal x, y

        if action == "N":
            y += value
        elif action == "E":
            x += value
        elif action == "S":
            y -= value
        elif action == "W":
            x -= value
        else:
            raise ValueError(f"{action} not in NESW")

    for action, value in directions:
        if action in "NESW":
            simulate_nesw(action, value)
        elif action == "R":
            rotation = (rotation + value) % 360
        elif action == "L":
            rotation = (rotation - value) % 360
        elif action == "F":
            simulate_nesw(
                value=value,
                action=(
                    "E" if rotation == 0 else
                    "S" if rotation == 90 else
                    "W" if rotation == 180 else
                    "N"
                )
            )
        else:
            raise ValueError(f"Unrecognized action: {action}")

    return x, y, rotation

x, y, _ = simulate(directions)
print("Part 1:", abs(x) + abs(y))

