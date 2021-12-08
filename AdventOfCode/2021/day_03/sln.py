# %%

from collections import defaultdict
import common
data = common.get_input(__file__, str.strip)

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

epsilon_rate = ''.join(
    ('0' if gamma_rate_bit == '1' else '1')
    for gamma_rate_bit in
    gamma_rate
)

gamma_rate = int(gamma_rate, 2)
epsilon_rate = int(epsilon_rate, 2)

print("Part 1:", gamma_rate * epsilon_rate)

# %%

from typing import List
def get_rating(data: List[str], current_bit: int, metric):
    if len(data) == 1:
        return int(data[0], 2)

    histogram = {'0': 0, '1': 0}

    for entry in data:
        histogram[entry[current_bit]] += 1

    filter_bit_value = None
    if metric == 'max':
        if histogram['0'] > histogram['1']:
            filter_bit_value = '0'
        else:
            filter_bit_value = '1'
    else:
        if histogram['1'] < histogram['0']:
            filter_bit_value = '1'
        else:
            filter_bit_value = '0'

    new_data = [
        entry
        for entry in data
        if entry[current_bit] == filter_bit_value
    ]

    return get_rating(new_data, current_bit + 1, metric)

oxygen_gen_rating = get_rating(data, 0, 'max')
co2_scrub_rating = get_rating(data, 0, 'min')

print("Part 2:", oxygen_gen_rating * co2_scrub_rating)
