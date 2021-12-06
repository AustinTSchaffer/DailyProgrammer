# %%

import common
import functools
import dataclasses


@dataclasses.dataclass()
class Location:
    depth: int
    position: int
    aim: int

    def update(self, depth=None, position=None, aim=None):
        return Location(
            depth if depth is not None else self.depth,
            position if position is not None else self.position,
            aim if aim is not None else self.aim,
        )

@dataclasses.dataclass()
class Instruction:
    direction: str
    distance: int

    def __init__(self, data: str):
        self.direction, self.distance = data.split(' ')
        self.distance = int(self.distance)

    def apply(self, loc: Location) -> Location:
        match self.direction:
            case 'forward':
                return loc.update(position=loc.position + self.distance)
            case 'up':
                return loc.update(depth=loc.depth - self.distance)
            case 'down':
                return loc.update(depth=loc.depth + self.distance)
            case _:
                raise ValueError(self.direction)

    def apply_part2(self, loc: Location) -> Location:
        match self.direction:
            case 'forward':
                return loc.update(
                    depth=loc.depth + (loc.aim * self.distance),
                    position=loc.position + self.distance,
                )
            case 'up':
                return loc.update(aim=loc.aim - self.distance)
            case 'down':
                return loc.update(aim=loc.aim + self.distance)
            case _:
                raise ValueError(self.direction)


data = common.get_input(__file__, callback=Instruction)

final_loc = functools.reduce(
    lambda loc, inst: inst.apply(loc),
    data,
    Location(0, 0, 0)
)

print("Part 1:", final_loc, '=', final_loc.depth * final_loc.position)

final_loc = functools.reduce(
    lambda loc, inst: inst.apply_part2(loc),
    data,
    Location(0, 0, 0)
)

print("Part 2:", final_loc, '=', final_loc.depth * final_loc.position)


# %%
