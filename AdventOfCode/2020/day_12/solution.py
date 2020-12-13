# %% 

directions = [
    (line[0], int(line[1:].strip()))
    for line in
    open("directions.txt").readlines()
]

test_directions = [
    ("F", 10),
    ("N", 3),
    ("F", 7),
    ("R", 90),
    ("F", 11),
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

x, y, _ = simulate(test_directions)
assert (abs(x) + abs(y) == 25), f"Expected {25} actual {abs(x) + abs(y)}"

x, y, _ = simulate(directions)
print("Part 1:", abs(x) + abs(y))

# %% Part 2

def simulate_part_2(directions: List[Tuple[str, int]]) -> Tuple[int, int, int]:
    ship_x, ship_y = 0, 0
    waypoint_x, waypoint_y = 10, 1

    for action, value in directions:
        if action == "N":
            waypoint_y += value
        elif action == "E":
            waypoint_x += value
        elif action == "S":
            waypoint_y -= value
        elif action == "W":
            waypoint_x -= value
        elif action in "RL":
            rotation = (-value if action == "L" else value) % 360
            if rotation == 0:
                pass
            elif rotation == 90:
                waypoint_x, waypoint_y = waypoint_y, -waypoint_x
            elif rotation == 180:
                waypoint_x, waypoint_y = -waypoint_x, -waypoint_y
            elif rotation == 270:
                waypoint_x, waypoint_y = -waypoint_y, waypoint_x
            else:
                raise ValueError(f"Invalid rotation value: {rotation}")
        elif action == "F":
            ship_x += waypoint_x * value
            ship_y += waypoint_y * value

    return ship_x, ship_y

x, y = simulate_part_2(test_directions)
assert (abs(x) + abs(y) == 286), f"Expected 286 Actual {abs(x) + abs(y)}"

x, y = simulate_part_2(directions)
print("Part 2:", abs(x) + abs(y))
