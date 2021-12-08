#%%
import common
crabs = list(map(int, common.get_input(__file__)[0].split(',')))

import collections
crab_map = collections.Counter(crabs)

fuel_costs = {}
for posistion in range(max(crabs) + 1):
    fuel_costs[posistion] = 0
    for crab_position, num_crabs_there in crab_map.items():
        # Fuel cost is linear
        fuel_costs[posistion] += abs(crab_position - posistion) * num_crabs_there

print("Part 1:", min(fuel_costs.items(), key=lambda item: item[1]))

fuel_costs = {}
for posistion in range(max(crabs) + 1):
    fuel_costs[posistion] = 0
    for crab_position, num_crabs_there in crab_map.items():
        # Fuel cost is correlated with the triangle number
        # for the difference between 2 locations.
        difference = abs(crab_position - posistion)
        fuel_cost = (difference * (difference + 1)) // 2
        fuel_costs[posistion] += fuel_cost * num_crabs_there

print("Part 2:", min(fuel_costs.items(), key=lambda item: item[1]))


#%%
