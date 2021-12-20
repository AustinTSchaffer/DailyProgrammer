import collections
import itertools
import common


def transform(line: str):
    line = line.strip()
    return tuple(map(str.strip, line.split("->")))


SEED = "SFBBNKKOHHHPFOFFSPFV"

transforms = dict(common.get_input(__file__, transform))


def expand(value: str):
    output = []
    for pair in itertools.pairwise(value):
        output.append(pair[0])
        if transform := transforms.get(''.join(pair)):
            output.append(transform)

    output.append(pair[1])
    return ''.join(output)


seed = SEED
for _ in range(10):
    seed = expand(seed)

histogram = collections.Counter(seed).most_common()
print("Part 1:", histogram[0][1] - histogram[-1][1])

# %%

# The part 1 algorithm will generate a string that's TBs in length if we go through with 40 iterations.
# Similar to the algorithm used to solve Day 6, if we instead just keep track of 2 histograms:
#   - Num occurrences of each letter
#   - Num occurrences of each pair
# then we can batch each transformation operation for each pair. If a pair is found in the transforms
# map, we can take the quantity of that pair and duplicate it to 2 separate entries in the next pair
# histogram, and also, for the letter in the transform, increment the letter histogram by the same :quantity.

pair_histogram = collections.defaultdict(int)
for pair in itertools.pairwise(SEED):
    pair_histogram[''.join(pair)] += 1
letter_histogram = collections.Counter(SEED)

def run_histogram_iteration(pair_histogram, letter_histogram):
    next_pair_histogram = collections.defaultdict(int)
    next_letter_histogram = collections.Counter() | letter_histogram
    for pair, quantity in pair_histogram.items():
        if transform := transforms.get(pair):
            next_letter_histogram[transform] += quantity
            next_pair_histogram[pair[0] + transform] += quantity
            next_pair_histogram[transform + pair[1]] += quantity
        else:
            next_pair_histogram[pair] = quantity
    return next_pair_histogram, next_letter_histogram


current_pair_histogram = pair_histogram
current_letter_histogram = letter_histogram
for _ in range(40):
    current_pair_histogram, current_letter_histogram = run_histogram_iteration(
        current_pair_histogram, current_letter_histogram)

histogram = current_letter_histogram.most_common()
print("Part 2:", histogram[0][1] - histogram[-1][1])
