#%%

data = [
    int(line.strip())
    for line in
    open("./data.txt").readlines()
]

import itertools

def is_a_sum_of_2(numbers, sum_):
    combinations = itertools.combinations(numbers, 2)
    for combination in combinations:
        if sum(combination) == sum_:
            return True
    return False

def _26wise(numbers):
    iterators = itertools.tee(numbers, 26)
    for i, iterator in enumerate(iterators):
        for _ in range(i):
            next(iterator, None)
    return zip(*iterators)

for *therest, thelast in _26wise(data):
    if not is_a_sum_of_2(therest, thelast):
        print(thelast)
