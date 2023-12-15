import re
import dataclasses
from typing import Literal

@dataclasses.dataclass
class Instruction:
    label: str
    operation: Literal['-', '=']
    lens: int | None 

    def __str__(self):
        return f'{self.label}{self.operation}{'' if self.lens is None else self.lens}'

INSTRUCTION_RE = re.compile(r'(?P<label>\w+)(?P<op>-|=)(?P<lens>\d*)')

@dataclasses.dataclass
class Input:
    raw_sequence: list[str]
    instructions: list[Instruction]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        raw_seq = f.read().split(',')
        instructions = [
            Instruction(
                label=match_['label'],
                operation=match_['op'],
                lens=int(lens) if (lens := match_['lens']) else None,
            )
            for info in raw_seq
            if (match_ := INSTRUCTION_RE.match(info))
        ]

        return Input(raw_seq, instructions)

def hash_alg(data: str) -> int:
    value = 0
    for c in data:
        value += ord(c)
        value *= 17
        value %= 256
    return value

def part_1(input: Input):
    return sum(map(hash_alg, input.raw_sequence))

def part_2(input: Input):
    boxes = [[] for _ in range(256)]
    for instruction in input.instructions:
        box_id = hash_alg(instruction.label)
        box = boxes[box_id]
        if instruction.operation == '-':
            for index, (label, _) in enumerate(box):
                if label == instruction.label:
                    del box[index]
                    break
        else:
            new_entry = (instruction.label, instruction.lens)
            did_stuff = False
            for index, (label, _) in enumerate(box):
                if label == instruction.label:
                    box[index] = new_entry
                    did_stuff = True
                    break
            if not did_stuff:
                box.append(new_entry)

    return sum(
        (box_id + 1) * (slot_id + 1) * lens
        for box_id, box in enumerate(boxes)
        for slot_id, (_, lens) in enumerate(box)
    )

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
