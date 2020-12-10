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

def n_wise(numbers, n):
    iterators = itertools.tee(numbers, n)
    for i, iterator in enumerate(iterators):
        for _ in range(i):
            next(iterator, None)
    return zip(*iterators)

bad_number = -1
for *therest, thelast in n_wise(data, 26):
    if not is_a_sum_of_2(therest, thelast):
        bad_number = thelast

print("Part 1:", bad_number)


# %%

data # list of integers
target = bad_number # result of Part 1

# keeps track of a rolling sum between starting/ending indexes
rolling_sum = 0
starting_index = 0
ending_index = 0

# O(2n)
while rolling_sum != target:
    if rolling_sum < target:
        rolling_sum += data[ending_index]
        ending_index += 1
    else:
        rolling_sum -= data[starting_index]
        starting_index += 1

# O(3m) time, O(m) space
slice_ = data[starting_index:ending_index]
print("Part 2:", min(slice_) + max(slice_))
