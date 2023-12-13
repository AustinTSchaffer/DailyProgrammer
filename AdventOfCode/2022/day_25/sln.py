import re
import dataclasses

SNAFU_DIGITS = '=-012'

@dataclasses.dataclass
class Input:
    snafu_nums: dict[str, list[int]]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        return Input(
            snafu_nums={
                line.strip(): [                
                    SNAFU_DIGITS.index(char) - 2
                    for char in line.strip()
                ]
                for line in f
            }
        )

def add_snafu_nums(num1: list[int], num2: list[int]) -> list[int]:
    ...

def to_snafu(num: int) -> str:
    output = []
    idx = 0
    to_conv = num
    while to_conv > 0:
        div = to_conv // 5
        rem = to_conv % 5

        if len(output) > idx:
            rem += output[idx]

        if rem > 2:
            if len(output) > idx:
                output[idx] = (rem - 5)
            else:
                output.append(rem - 5)
            output.append(1)
        else:
            if len(output) > idx:
                output[idx] = rem
            else:
                output.append(rem)

        idx += 1
        to_conv = div

    return ''.join(SNAFU_DIGITS[digit+2] for digit in reversed(output))

def part_1(input: Input):
    sum_ = 0
    for num in input.snafu_nums.values():
        for i, digit in enumerate(reversed(num)):
            sum_ += digit * (5**i)
    return (sum_, to_snafu(sum_))

def part_2(input: Input):
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
