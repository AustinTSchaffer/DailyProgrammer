import os
import re
from collections import defaultdict

class Claim(object):
    def __init__(self, data_row):
        match = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', data_row)
        self.id = int(match[1])
        self.x = int(match[2])
        self.y = int(match[3])
        self.width = int(match[4])
        self.height = int(match[5])

    def all_locations(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (self.x + x, self.y + y)

CURRENT_DIR, _ = os.path.split(__file__)
DATA_FLIE = os.path.join(CURRENT_DIR, 'data.txt')

def data_file_iter(data_file) -> Claim:
    with open(data_file, 'r') as data:
        for claim in data:
            claim = claim.strip()
            if (claim):
                yield Claim(claim)

def part1(claims):
    """
    This is basically a single-threaded collision detection method, 
    implemented in pure python. Computation complexity is obviously
    not a consideration.
    """
    # Determines how many times each locations was claimed
    claimed_space_registry = defaultdict(int)
    for claim in claims:
        for location in claim.all_locations():
            claimed_space_registry[location] += 1

    # Generates the set of all locations that were claimed more than once
    multi_claimed_spaces = {
        location
        for location,count in claimed_space_registry.items()
        if count > 1
    }

    # Prints the number of locations that are claimed more than once
    # and returns the set of locations that were claimed more than once
    print('Multi-Claimed Spaces:', len(multi_claimed_spaces))
    return multi_claimed_spaces

def part2(claims, multi_claimed_spaces):
    """
    Might not be the optimal solution, but it runs fast enough, and uses
    components that were already calculated in part 1.
    """
    for claim in claims:
        all_locations_are_non_overlapping = all(map(
            lambda loc: loc not in multi_claimed_spaces,
            claim.all_locations()
        ))
        
        if all_locations_are_non_overlapping:  
            print('Non-overlapping claim:', claim.id)
            return claim

if __name__ == '__main__':
    claims = list(data_file_iter(DATA_FLIE))
    mcs = part1(claims)
    santas_suit_material = part2(claims, mcs)
