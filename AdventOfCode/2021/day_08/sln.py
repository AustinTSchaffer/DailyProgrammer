# %%

from common import get_input
import collections


class InputOutput:
    def __init__(self, row: str):
        self._repr = row
        self.input, self.output = row.split("|")
        self.input = self.input.strip().split()
        self.output = self.output.strip().split()

    def __repr__(self) -> str:
        return self._repr

io_lines = get_input(__file__, InputOutput)

part_1_data = collections.defaultdict(int)
for line in io_lines:
    for output in line.output:
        part_1_data[len(output)] += 1

# 0 has 6 segments
# 1 has 2 segments (unique)
# 2 has 5 segments
# 3 has 5 segments
# 4 has 4 segments (unique)
# 5 has 5 segments
# 6 has 6 segments
# 7 has 3 segments (unique)
# 8 has 7 segments (unique)
# 9 has 6 segments (it's a serifed 9 I guess)
print(
    "Part 1:",
    (
        part_1_data[2] +
        part_1_data[4] +
        part_1_data[3] +
        part_1_data[7]
    )
)

# %% Part 2

def find_shapes(io_line: InputOutput):
    # Maps number of segments to shapes containing
    # that number of segments
    shapes_of_len = collections.defaultdict(list)
    for entry in io_line.input:
        shapes_of_len[len(entry)].append(set(entry))

    # Maps the numbers to sets containing the shape's segment IDs
    shapes = collections.defaultdict(set)

    # Shapes with a unique number of segments
    shapes[1] = shapes_of_len.pop(2)[0]
    shapes[4] = shapes_of_len.pop(4)[0]
    shapes[7] = shapes_of_len.pop(3)[0]
    shapes[8] = shapes_of_len.pop(7)[0]

    # Shape 9 is the only 6-segment shape that contains
    # shape 7 and shape 4 with 1 extra segment
    shapes[9] = next(
        shape for shape in shapes_of_len[6]
        if len(shape - shapes[7] - shapes[4]) == 1
    )
    shapes_of_len[6].remove(shapes[9])

    # Shape 0 is the only unidentified 6-segment
    # shape that contains shape 7 with 3 extra segments
    shapes[0] = next(
        shape for shape in shapes_of_len[6]
        if len(shape - shapes[7]) == 3
    )
    shapes_of_len[6].remove(shapes[0])

    # Shape 6 is the remaining unidentified 6-segment shape
    shapes[6] = shapes_of_len.pop(6)[0]

    # Shape 3 is the only 5-segment shape that contains
    # shape 7 with 2 extra segments
    shapes[3] = next(
        shape for shape in shapes_of_len[5]
        if len(shape - shapes[7]) == 2
    )
    shapes_of_len[5].remove(shapes[3])

    # Shape 5 is the only unidentified 5-segment shape
    # which is equivalent to shape 6 missing 1 segment
    shapes[5] = next(
        shape for shape in shapes_of_len[5]
        if len(shapes[6] - shape) == 1
    )
    shapes_of_len[5].remove(shapes[5])

    # Shape 2 is the remaining unidentified 5-segment shape
    shapes[2] = shapes_of_len.pop(5)[0]

    return shapes

from typing import Dict
def shape_id(shape: str, shapes: Dict[int, set]) -> int:
    shape = set(shape)
    for shape_id, shape_ in shapes.items():
        if not set.symmetric_difference(shape, shape_):
            return shape_id

output_value_sum = 0
for io_line in io_lines:
    shapes = find_shapes(io_line)
    multiplier = 1
    for entry in reversed(io_line.output):
        output_value_sum += (shape_id(entry, shapes) * multiplier)
        multiplier *= 10

print("Part 2:", output_value_sum)

#%%