#%%

def parse_input(line: str):
    return tuple(map(int, line.strip().split(",")))

import re

def parse_fold_instruction(line: str):
    match = re.search(r'(?P<axis>[xy])=(?P<position>\d+)$', line)
    return (
        match['axis'],
        int(match['position']),
    )

import common
dots = set(common.get_input(__file__, parse_input, 'input.txt'))
folds = common.get_input(__file__, parse_fold_instruction, filename='fold_instructions.txt')



def apply_fold(fold: tuple, image: set):
    fold_axis, fold_position = fold

    next_image = set()
    # Always fold bottom to top and right to left.
    for dot in image:
        if fold_axis == 'x':
            next_dot = (
                (fold_position - (dot[0] - fold_position), dot[1])
                if dot[0] > fold_position else
                dot
            )

            next_image.add(next_dot)
        elif fold_axis == 'y':
            next_dot = (
                (dot[0], fold_position - (dot[1] - fold_position))
                if dot[1] > fold_position else
                dot
            )
            next_image.add(next_dot)
        else:
            raise ValueError(fold)

    return next_image

part_1 = apply_fold(folds[0], dots)
print("Part 1:", len(part_1))

part_2 = dots
for fold in folds:
    part_2 = apply_fold(fold, part_2)


max_x, _ = max(part_2, key=lambda dot: dot[0])
_, max_y = max(part_2, key=lambda dot: dot[1])

print("Part 2:")
for col in range(6):
    print(''.join(
        '#' if (row, col) in part_2 else ' '
        for row in range(50)
    ))


#%%
