#%%

data = open("data.txt").readlines()

wall_outlet_joltage_rating = 0
adapter_joltage_ratings = sorted((int(adapter.strip()) for adapter in data))
device_adapter_joltage_rating = adapter_joltage_ratings[-1] + 3

joltage_ratings = [
    wall_outlet_joltage_rating,
    *adapter_joltage_ratings,
    device_adapter_joltage_rating,
]

max_input_output_delta = 3

#%% Part 1

import itertools

def pairwise(iterable):
    iter_a, iter_b = itertools.tee(iterable)
    next(iter_b, None)
    return zip(iter_a, iter_b)

differences = [0] * (1 + max_input_output_delta)

for lower, higher in pairwise(joltage_ratings):
    differences[higher - lower] += 1

print(f"Part 1:", differences[3] * differences[1])

#%% Part 2

direced_graph = {}
for index, rating_a in enumerate(joltage_ratings):
    rating_a_edges = []
    direced_graph[rating_a] = rating_a_edges
    for rating_b in joltage_ratings[index+1:]:
        if rating_b - rating_a > max_input_output_delta:
            break
        else:
            rating_a_edges.append(rating_b)

import functools

@functools.lru_cache(maxsize=len(direced_graph))
def total_paths_between(node, endpoint) -> int:
    if node == endpoint: return 1
    return sum((total_paths_between(edge, endpoint) for edge in direced_graph[node]))

print("Part 2:", total_paths_between(wall_outlet_joltage_rating, device_adapter_joltage_rating))
