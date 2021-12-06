#%% 

import common
data = common.get_input(__file__, str.strip)

from collections import defaultdict
position_histograms = defaultdict(lambda: defaultdict(int))

for number in data:
    for i, position in enumerate(number):
        position_histograms[i][position] += 1

gamma_rate = ""
for position_histogram in position_histograms.values():
    gamma_rate += (
        '0'
        if position_histogram['0'] > position_histogram['1'] else
        '1'
    )

gamma_rate = int(gamma_rate, 2)

# ~ is python's bitwise inversion operator. Need to do the rest to make it unsigned.
epsilon_rate = ~gamma_rate & ((1 << gamma_rate.bit_length()) - 1)

print("Part 1:", gamma_rate * epsilon_rate)

# %%
