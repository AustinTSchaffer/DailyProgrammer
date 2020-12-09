#%%

data = [
    int(line.strip())
    for line in
    open("./data.txt").readlines()
]

import itertools

def is_a_sum_of_2(numbers, sum_):
    combinations = itertools.combinations(numbers, 2)
    for a, b in combinations:
        if a + b == sum_ and a != b:
            return True
    return False

def _26wise(numbers):
    iterators = itertools.tee(numbers, 26)
    for i, iterator in enumerate(iterators):
        for _ in range(i):
            next(iterator, None)
    return zip(*iterators)

bad_number = -1
for *therest, thelast in _26wise(data):
    if not is_a_sum_of_2(therest, thelast):
        bad_number = thelast

print("Part 1:", bad_number)


# %%

starting_index = 0
length = 1

while True:
    slice_ = data[starting_index:length]
    sum_  = sum(slice_)
    if sum_ == bad_number:
        print("Part 2:", min(slice_) + max(slice_))
        break
    elif sum_ > bad_number:
        starting_index += 1
        length -= 1
    else:
        length += 1

# %%
