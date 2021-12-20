#%%

from common import get_input

data = get_input(__file__)

map = {}
for row, line in enumerate(data):
    for col, char in enumerate(line.strip()):
        map[(row, col)] = int(char)

total_risk_level = 0
local_minimum_locations = []

for (row, col), height in map.items():
    is_local_minimum = all(
        height < map[loc]
        for loc in (
            (row+1, col),
            (row-1, col),
            (row, col+1),
            (row, col-1),
        )
        if loc in map
    )
    if is_local_minimum:
        local_minimum_locations.append((row, col))
        total_risk_level += 1 + height

print("Part 1:", total_risk_level)

#%%

def find_basin(location):
    seeds = {location}
    explored = set()
    while len(seeds) > 0:
        seed = seeds.pop()
        explored.add(seed)
        seeds.update(
            location
            for location in (
                (seed[0] + 1, seed[1]),
                (seed[0] - 1, seed[1]),
                (seed[0], seed[1] + 1),
                (seed[0], seed[1] - 1),
            )
            if location in map and map[location] != 9 and map[location] > map[seed] and location not in explored
        )

    return explored

basins = {}
for local_minimum_location in local_minimum_locations:
    basins[local_minimum_location] = find_basin(local_minimum_location)

largest_basins = sorted(basins.values(), key=lambda basin: len(basin), reverse=True)

print("Part 2:", len(largest_basins[0]) * len(largest_basins[1]) * len(largest_basins[2]))
