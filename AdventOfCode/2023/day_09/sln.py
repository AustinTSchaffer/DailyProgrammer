import re
import dataclasses

@dataclasses.dataclass
class Input:
    series: list[list[int]]
    """
    Smeagol voice: serieses
    """

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        return Input(
            series=[
                [int(val) for val in line.split()]
                for line in f
            ]
        )

def part_1(input: Input):
    for series in input.series:
        derivatives = []
    ...

def part_2(input: Input):
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
