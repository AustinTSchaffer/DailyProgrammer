#%%

data = open("data.txt").readlines()

wall_outlet_joltage_rating = 0
adapter_joltage_ratings = sorted((int(adapter.strip()) for adapter in data))
device_adapter_joltage_rating = adapter_joltage_ratings[-1] + 3

max_input_output_delta = 3

import itertools

def pairwise(iterable):
    iter_a, iter_b = itertools.tee(iterable)
    next(iter_b, None)
    return zip(iter_a, iter_b)

differences = [0] * (1 + max_input_output_delta)

for lower, higher in pairwise([wall_outlet_joltage_rating] + adapter_joltage_ratings + [device_adapter_joltage_rating]):
    differences[higher - lower] += 1    

print(f"Part 1:", differences[3] * differences[1])

# %%
