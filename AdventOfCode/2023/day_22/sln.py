import re
import dataclasses
import timeit
from collections import namedtuple, defaultdict, deque
from typing import Iterable

Coordinates = namedtuple("Coordinates", ["x", "y", "z"])
Coordinates.__repr__ = lambda c: f'({c.x}, {c.y}, {c.z})'

@dataclasses.dataclass(frozen=True)
class Brick:
    a: Coordinates
    """
    (x,y,z) coordinates of the front-most, left-most, bottom-most
    voxel of the brick (e.g. the minimum tuple).
    """

    b: Coordinates
    """
    (x,y,z) coordinates of the back-most, right-most, top-most
    voxel of the brick (e.g. the maximum tuple).
    """

    def coordinates(self) -> Iterable[Coordinates]:
        for x in range(self.a.x, self.b.x+1):
            for y in range(self.a.y, self.b.y+1):
                for z in range(self.a.z, self.b.z+1):
                    yield Coordinates(x, y, z)

def parse_input(filename: str) -> list[Brick]:
    with open(filename, 'r') as f:
        return [
            Brick(
                *sorted([
                    Coordinates(*map(int, split[0].split(','))),
                    Coordinates(*map(int, split[1].split(','))),
                ])
            )
            for line in f
            if len(split := line.split('~')) == 2
        ]


def p1_and_p2(input: list[Brick]):
    # Bricks sorted by their z-index
    sorted_bricks = sorted(input, key=lambda brick: brick.a.z)

    # Dictionary of settled bricks.
    brictionary: dict[tuple[int, int, int], Brick] = {} # ;)

    # Settle the bricks
    new_bricks = []
    for brick in sorted_bricks:
        brick_settled = False
        z_off = 0

        brick_settled = lambda: (
            brick.a.z + z_off == 1 or any(
                (x, y, brick.a.z + z_off - 1) in brictionary
                for x in range(brick.a.x, brick.b.x + 1)
                for y in range(brick.a.y, brick.b.y + 1)
            )
        )

        while not brick_settled():
            z_off -= 1

        new_brick = Brick(
            Coordinates(brick.a.x, brick.a.y, brick.a.z + z_off),
            Coordinates(brick.b.x, brick.b.y, brick.b.z + z_off),
        )

        new_bricks.append(new_brick)

        for x in range(brick.a.x, brick.b.x + 1):
            for y in range(brick.a.y, brick.b.y + 1):
                for z in range(brick.a.z + z_off, brick.b.z + z_off + 1):
                    brictionary[(x, y, z)] = new_brick

    # Determine stacking
    bricks_above = defaultdict(set)
    bricks_below = defaultdict(set)
    for brick in new_bricks:
        for x in range(brick.a.x, brick.b.x + 1):
            for y in range(brick.a.y, brick.b.y + 1):
                if brick_above := brictionary.get((x, y, brick.b.z + 1)):
                    bricks_above[brick].add(brick_above)
                    bricks_below[brick_above].add(brick)

    # Determine proper jenga moves
    can_remove = 0
    for brick in new_bricks:
        valid = True
        for brick_above in bricks_above[brick]:
            if len(bricks_below[brick_above]) == 1:
                valid = False
                break
        if valid:
            can_remove += 1

    # Determine the total number of bricks that will fall if you remove
    # a brick, on a per-brick basis. Sum this value for all bricks.
    bricks_moved_by_chain_reaction = 0
    for brick in new_bricks:
        bricks_moved = { brick }
        q = deque([brick])
        while len(q):
            b = q.popleft()
            for bab in bricks_above[b]:
                if len(bricks_below[bab] - bricks_moved) == 0:
                    bricks_moved.add(bab)
                    q.append(bab)
        if len(bricks_moved) > 1:
            bricks_moved_by_chain_reaction += (len(bricks_moved) - 1)

    return can_remove, bricks_moved_by_chain_reaction


if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    timeit_globals = {'input': input, 'p1_and_p2': p1_and_p2}

    timer = timeit.Timer(
        'global result; result = p1_and_p2(input)',
        globals=timeit_globals
    )

    timeit_globals['input'] = sample_input
    time = timer.timeit(1)
    print('Part 1 and 2 (sample):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = timer.timeit(1)
    print('Part 1 and 2:', timeit_globals['result'], f'({time:.3} seconds)')
