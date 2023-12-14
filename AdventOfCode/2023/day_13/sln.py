import re
import dataclasses
import itertools
from typing import Literal

@dataclasses.dataclass
class Pattern:
    data: list[str]

    def rows(self):
        return self.data

    def cols(self):
        return [
            ''.join(row[i] for row in self.data)
            for i in range(len(self.data[0]))
        ]

    def reflection_line(self) -> tuple[Literal['H', 'V'], int]:
        rows = self.rows()
        cols = self.cols()

        for i, (r1, r2) in enumerate(itertools.pairwise(rows)):
            if r1 != r2:
                continue

            if all(r1 == r2 for r1, r2 in zip(rows[i+1::], rows[i::-1])):
                return 'H', i+1

        for j, (c1, c2) in enumerate(itertools.pairwise(cols)):
            if c1 != c2:
                continue

            if all(c1 == c2 for c1, c2 in zip(cols[j+1::], cols[j::-1])):
                return 'V', j+1

        raise ValueError(self)


    def p2_reflection_line(self) -> tuple[Literal['H', 'V'], int]:
        rows = self.rows()
        cols = self.cols()

        for i, (row1, row2) in enumerate(itertools.pairwise(rows)):
            num_diffs = 0
            for row1, row2 in zip(rows[i+1::], rows[i::-1]):
                for char1, char2 in zip(row1, row2):
                    if char1 != char2:
                        num_diffs += 1
                if num_diffs > 1:
                    break
            if num_diffs == 1:
                return 'H', i+1

        for j, (col1, col2) in enumerate(itertools.pairwise(cols)):
            num_diffs = 0
            for col1, col2 in zip(cols[j+1::], cols[j::-1]):
                for char1, char2 in zip(col1, col2):
                    if char1 != char2:
                        num_diffs += 1
                if num_diffs > 1:
                    break
            if num_diffs == 1:
                return 'V', j+1

        raise ValueError(self)

def parse_input(filename: str) -> list[Pattern]:
    with open(filename, 'r') as f:
        return [
            Pattern(chunk.split('\n'))
            for chunk in
            f.read().split('\n\n')
        ]

def part_1(input: list[Pattern]):
    total = 0
    for pattern in input:
        direction, index = pattern.reflection_line()
        if direction == 'H':
            total += 100 * index
        else:
            total += index
    return total

def part_2(input: list[Pattern]):
    total = 0
    for pattern in input:
        direction, index = pattern.p2_reflection_line()
        if direction == 'H':
            total += 100 * index
        else:
            total += index
    return total

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
