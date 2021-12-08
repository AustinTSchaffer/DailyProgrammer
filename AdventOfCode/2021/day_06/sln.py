#%%

import common
import dataclasses
from typing import List

import collections
lantern_fish = collections.defaultdict(int)
input = common.get_input(__file__)[0]
for fish_timer in input.split(','):
    lantern_fish[int(fish_timer)] += 1

current_generation = lantern_fish
for iteration in range(80):
    next_generation = {}

    next_generation[0] = current_generation[1]
    next_generation[1] = current_generation[2]
    next_generation[2] = current_generation[3]
    next_generation[3] = current_generation[4]
    next_generation[4] = current_generation[5]
    next_generation[5] = current_generation[6]
    next_generation[6] = current_generation[7] + current_generation[0]
    next_generation[7] = current_generation[8]
    next_generation[8] = current_generation[0]

    current_generation = next_generation

print('Part 1:', sum(current_generation.values()))

current_generation = lantern_fish
for iteration in range(256):
    next_generation = {}

    next_generation[0] = current_generation[1]
    next_generation[1] = current_generation[2]
    next_generation[2] = current_generation[3]
    next_generation[3] = current_generation[4]
    next_generation[4] = current_generation[5]
    next_generation[5] = current_generation[6]
    next_generation[6] = current_generation[7] + current_generation[0]
    next_generation[7] = current_generation[8]
    next_generation[8] = current_generation[0]

    current_generation = next_generation

print('Part 2:', sum(current_generation.values()))

#%%
