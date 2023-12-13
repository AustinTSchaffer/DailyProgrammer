import re
import dataclasses
import itertools

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
    sum_ = 0
    for series in input.series:
        derivatives = [series]
        while not all(map(lambda v: v == 0, derivatives[-1])):
            derivatives.append([
                b-a
                for a, b in
                itertools.pairwise(derivatives[-1])
            ])
        for d_layer, layer in itertools.pairwise(reversed(derivatives)):
            layer.append(layer[-1] + d_layer[-1])
        sum_ += series[-1]
    return sum_

def part_2(input: Input):
    sum_ = 0
    for series in input.series:
        derivatives = [series]
        while not all(map(lambda v: v == 0, derivatives[-1])):
            derivatives.append([
                b-a
                for a, b in
                itertools.pairwise(derivatives[-1])
            ])
        for d_layer, layer in itertools.pairwise(reversed(derivatives)):
            layer.insert(0, layer[0] - d_layer[0])
        sum_ += series[0]
    return sum_

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
