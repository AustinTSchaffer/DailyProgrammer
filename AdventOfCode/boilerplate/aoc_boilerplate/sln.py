import re
import dataclasses
import timeit

@dataclasses.dataclass
class Input:
    ...

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        ...

def part_1(input: Input):
    ...

def part_2(input: Input):
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    timeit_globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals=timeit_globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals=timeit_globals
    )

    timeit_globals['input'] = sample_input
    time = part_1_timer.timeit(1)
    print('Part 1 (sample):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = part_1_timer.timeit(1)
    print('Part 1:', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = sample_input
    time = part_1_timer.timeit(1)
    print('Part 2 (sample):', timeit_globals['result'], f'({time:.3} seconds)')

    timeit_globals['input'] = input
    time = part_2_timer.timeit(1)
    print('Part 2:', timeit_globals['result'], f'({time:.3} seconds)')
