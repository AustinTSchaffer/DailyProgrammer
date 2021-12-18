#%%

from common import get_input
octopuses_input = get_input(__file__)

def gen_octopuses_map():
    octopuses = {
        (row, col): int(octopus)
        for row, line in enumerate(octopuses_input)
        for col, octopus in enumerate(line.strip())
    }

    return octopuses

def adjacent_locations(location):
    return [
        (location[0] - 1, location[1] - 1),
        (location[0] - 1, location[1]),
        (location[0] - 1, location[1] + 1),
        (location[0], location[1] - 1),
        (location[0], location[1] + 1),
        (location[0] + 1, location[1] - 1),
        (location[0] + 1, location[1]),
        (location[0] + 1, location[1] + 1),
    ]

def print_octopuses(octopuses):
    for i in range(10):
        row = ''.join(str(octopuses[(i, j)]) for j in range(10))
        print(row)
    print()

def simulate_iteration(octopuses):
    # Step 1
    for location in octopuses:
        octopuses[location] += 1

    octopuses_flashed = set()
    def flash_octopus(location):
        if octopuses[location] > 9 and (location not in octopuses_flashed):
            octopuses_flashed.add(location)
            for adjacent_location in adjacent_locations(location):
                if adjacent_location in octopuses:
                    octopuses[adjacent_location] += 1
                    flash_octopus(adjacent_location)

    # Step 2
    for location in octopuses:
        flash_octopus(location)

    # Step 3
    for location in octopuses_flashed:
        octopuses[location] = 0

    return len(octopuses_flashed)


octopuses = gen_octopuses_map()
print("Part 1:", sum((simulate_iteration(octopuses)) for _ in range(100)))

octopuses = gen_octopuses_map()
total_num_octopuses = len(octopuses)
step = 0
while True:
    step += 1
    num_octopuses_flashed = simulate_iteration(octopuses)
    if num_octopuses_flashed == total_num_octopuses:
        break

print("Part 2:", step)
#%%

