import re
import dataclasses
import timeit
from typing import Literal
import itertools

T_Dir = Literal['L', 'U', 'D', 'R']

@dataclasses.dataclass
class Instruction:
    dir: T_Dir
    dist: int
    color: str

    def part_2(self) -> 'Instruction':
        dir, dist = self.color[-1], self.color[:-1]

        dir = (
            'R' if dir == '0' else
            'D' if dir == '1' else
            'L' if dir == '2' else
            'U' if dir == '3' else
            None
        )

        dist = int(dist, base=16)

        if dir is None or dist is None:
            raise ValueError(self)

        return Instruction(dir, dist, None)

INSTRUCTION_RE = re.compile(r'([LUDR]) (\d+) \(#(.{6})\)')

@dataclasses.dataclass
class Input:
    instructions: list[Instruction]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        return Input(
            instructions=[
                Instruction(
                    dir=m[1],
                    dist=int(m[2]),
                    color=m[3],
                )
                for m in INSTRUCTION_RE.finditer(f.read())
            ]
        )

def display_trench(trench: dict[tuple[int, int], Instruction]):
    min_i = min(idx[0] for idx in trench)
    max_i = max(idx[0] for idx in trench)
    min_j = min(idx[1] for idx in trench)
    max_j = max(idx[1] for idx in trench)

    output = []
    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            if (i,j) in trench:
                output.append('#')
            else:
                output.append('.')
        output.append('\n')

    print(''.join(output))

def part_1(input: Input):
    trench: dict[tuple[int, int], Instruction] = {}

    curr_i = 0
    curr_j = 0

    prev_dir = input.instructions[-1].dir
    vertices: list[tuple[int, int]] = []

    for inst in input.instructions:
        match (prev_dir, inst.dir):
            case ('U', 'R') | ('R', 'U'):
                vertices.append((curr_i, curr_j))
            case ('U', 'L') | ('L', 'U'):
                vertices.append((curr_i + 1, curr_j))
            case ('D', 'R') | ('R', 'D'):
                vertices.append((curr_i, curr_j + 1))
            case ('D', 'L') | ('L', 'D'):
                vertices.append((curr_i + 1, curr_j + 1))

        if inst.dir == 'D':
            for i in range(curr_i + 1, curr_i + inst.dist + 1):
                trench[(i, curr_j)] = inst
            curr_i = i
        elif inst.dir == 'U':
            for i in range(curr_i - 1, curr_i - inst.dist - 1, -1):
                trench[(i, curr_j)] = inst
            curr_i = i
        elif inst.dir == 'R':
            for j in range(curr_j + 1, curr_j + inst.dist + 1):
                trench[(curr_i, j)] = inst
            curr_j = j
        elif inst.dir == 'L':
            for j in range(curr_j - 1, curr_j - inst.dist - 1, -1):
                trench[(curr_i, j)] = inst
            curr_j = j
        else:
            raise ValueError(inst)

        prev_dir = inst.dir

    vertices.append((0, 0))

    # Trapezoid form of the shoelace formula.
    # https://en.wikipedia.org/wiki/Shoelace_formula
    area = sum(
        (v1[0] + v2[0]) * (v1[1] - v2[1])
        for v1, v2 in itertools.pairwise(vertices)
    ) // 2

    return area

def part_2(input: Input):
    curr_i = 0
    curr_j = 0

    prev_dir = input.instructions[-1].part_2().dir
    vertices: list[tuple[int, int]] = []

    for inst in input.instructions:
        inst = inst.part_2()

        match (prev_dir, inst.dir):
            case ('U', 'R') | ('R', 'U'):
                vertices.append((curr_i, curr_j))
            case ('U', 'L') | ('L', 'U'):
                vertices.append((curr_i + 1, curr_j))
            case ('D', 'R') | ('R', 'D'):
                vertices.append((curr_i, curr_j + 1))
            case ('D', 'L') | ('L', 'D'):
                vertices.append((curr_i + 1, curr_j + 1))

        if inst.dir == 'D':
            curr_i = curr_i + inst.dist
        elif inst.dir == 'U':
            curr_i = curr_i - inst.dist
        elif inst.dir == 'R':
            curr_j = curr_j + inst.dist
        elif inst.dir == 'L':
            curr_j = curr_j - inst.dist
        else:
            raise ValueError(inst)

        prev_dir = inst.dir

    vertices.append((0, 0))

    # Trapezoid form of the shoelace formula.
    # https://en.wikipedia.org/wiki/Shoelace_formula
    area = sum(
        (v1[0] + v2[0]) * (v1[1] - v2[1])
        for v1, v2 in itertools.pairwise(vertices)
    ) // 2

    return area

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals = globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals = globals
    )

    print('Part 1 (sample):', part_1(sample_input))
    time = part_1_timer.timeit(1)
    print('Part 1:', globals['result'], f'({time:.3} seconds)')

    print('Part 2 (sample):', part_2(sample_input))
    time = part_2_timer.timeit(1)
    print('Part 2:', globals['result'], f'({time:.3} seconds)')
