#%%

import common
data = common.get_input(__file__, callback=int)

increased = 0
prevpoint = data[0]
for point in data[1:]:
    if prevpoint < point:
        increased += 1
    prevpoint = point

print("Part 1:", increased)

#%%

three_m_sliding_window_gen = map(sum, zip(
    data,
    data[1:],
    data[2:],
))

increased = 0
prevpoint = next(three_m_sliding_window_gen)
for point in three_m_sliding_window_gen:
    if prevpoint < point:
        increased += 1
    prevpoint = point

print("Part 2:", increased)

# %%


