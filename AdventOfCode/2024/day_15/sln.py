import re
import dataclasses
import time
from typing import Any

console_input = input

@dataclasses.dataclass
class Input:
    robot: tuple[int, int]
    walls: set[tuple[int, int]]
    boxes: set[tuple[int, int]]
    bounds: tuple[int, int]
    instructions: list[tuple[tuple[int, int], str]]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.read()
    grid, instructions = data.split('\n\n')

    bounds = (0, 0)
    walls = set()
    boxes = set()
    for i, row in enumerate(grid.split('\n')):
        for j, char in enumerate(row):
            if char == '@':
                robot = (i, j)
            elif char == '#':
                walls.add((i, j))
                bounds = max(bounds, (i, j))
            elif char == 'O':
                boxes.add((i, j))

    instructions = [
        ((
            (-1, 0) if c == '^' else
            (1, 0) if c == 'v' else
            (0, -1) if c == '<' else
            (0, 1)
        ), c)
        for c in instructions
        if c in '^v<>'
    ]

    return Input(
        robot=robot,
        walls=walls,
        boxes=boxes,
        instructions=instructions,
        bounds=bounds,
    )

def part_1(input: Input):
    boxes = input.boxes.copy()
    robot = input.robot

    for instruction, glyph in input.instructions:
        next_robot_loc = (robot[0] + instruction[0], robot[1] + instruction[1])
        if next_robot_loc in input.walls:
            continue
        if next_robot_loc not in boxes:
            robot = next_robot_loc
            continue

        boxes.remove(next_robot_loc)
        box_removed = next_robot_loc
        next_box_loc = (
            next_robot_loc[0] + instruction[0],
            next_robot_loc[1] + instruction[1],
        )
        while next_box_loc in boxes:
            next_box_loc = (
                next_box_loc[0] + instruction[0],
                next_box_loc[1] + instruction[1],
            )
        if next_box_loc in input.walls:
            boxes.add(box_removed)
            continue
        robot = next_robot_loc
        boxes.add(next_box_loc)

    return sum(
        (100 * b[0]) + b[1]
        for b in boxes
    )

def part_2(input: Input):
    boxes = {
        (b[0], 2*b[1])
        for b in input.boxes
    }

    walls = {
        (w[0], (2*w[1]) + i)
        for w in input.walls
        for i in range(2)
    }

    robot = (
        input.robot[0],
        input.robot[1] * 2,
    )

    for instruction, glyph in input.instructions:
        next_robot_loc = (robot[0] + instruction[0], robot[1] + instruction[1])
        if next_robot_loc in walls:
            continue

        if (box_head := next_robot_loc) in boxes:
            ...
        elif (box_head := (next_robot_loc[0], next_robot_loc[1] - 1)) in boxes:
            ...
        else:
            robot = next_robot_loc
            continue

        boxes.remove(box_head)
        boxes_removed = [box_head]
        next_box_locs = [(
            box_head[0] + instruction[0],
            box_head[1] + instruction[1],
        )]

        collision_detected = True
        while collision_detected:
            collision_detected = False
            for this_box_head in next_box_locs:
                # Box head hits box head.
                if this_box_head in boxes:
                    collision_detected = True
                    other_box_head = this_box_head
                    boxes.remove(other_box_head)
                    boxes_removed.append(other_box_head)
                    next_box_locs.append((
                        other_box_head[0] + instruction[0],
                        other_box_head[1] + instruction[1],
                    ))
                # Box tail hits box head.
                this_box_tail = (this_box_head[0], this_box_head[1] + 1)
                if this_box_tail in boxes:
                    collision_detected = True
                    other_box_head = this_box_tail
                    boxes.remove(other_box_head)
                    boxes_removed.append(other_box_head)
                    next_box_locs.append((
                        other_box_head[0] + instruction[0],
                        other_box_head[1] + instruction[1],
                    ))
                # Box head hits box tail.
                other_box_tail = this_box_head
                other_box_head = (other_box_tail[0], other_box_tail[1] - 1)
                if other_box_head in boxes:
                    collision_detected = True
                    boxes.remove(other_box_head)
                    boxes_removed.append(other_box_head)
                    next_box_locs.append((
                        other_box_head[0] + instruction[0],
                        other_box_head[1] + instruction[1],
                    ))

        any_box_wall_collisions = False
        for box in next_box_locs:
            if box in walls or (box[0], box[1] + 1) in walls:
                any_box_wall_collisions = True
                break
            continue

        if any_box_wall_collisions:
            for box in boxes_removed:
                boxes.add(box)
            continue

        robot = next_robot_loc
        for box in next_box_locs:
            boxes.add(box)

    return sum(
        (100 * l[0]) + l[1]
        for l in boxes
    )

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input_1 = parse_input('sample_input.1.txt')
    sample_input_2 = parse_input('sample_input.2.txt')
    sample_input_3 = parse_input('sample_input.3.txt')

    before = time.time_ns()
    result = part_1(sample_input_1)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1 (sample 1):', result, f'({_time} ms)')

    result = part_1(sample_input_1)

    before = time.time_ns()
    result = part_1(sample_input_2)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1 (sample 2):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_1(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1:', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(sample_input_1)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2 (sample 1):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(sample_input_2)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2 (sample 2):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(sample_input_3)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2 (sample 3):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2:', result, f'({_time} ms)')
