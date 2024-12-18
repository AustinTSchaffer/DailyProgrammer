import re
import dataclasses
import time
from typing import Any

@dataclasses.dataclass
class Input:
    register_a: int
    register_b: int
    register_c: int
    program: list[int]

def parse_input(filename: str) -> Input:
    program_re = re.compile(r'Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.+)')
    with open(filename, 'r') as f:
        data = f.read()
    match_ = program_re.match(data)
    return Input(
        register_a=int(match_[1]),
        register_b=int(match_[2]),
        register_c=int(match_[3]),
        program=list(map(int, match_[4].split(',')))
    )


def simulate(input: Input, a_val: int = None) -> list[int]:
    registers = (
        [a_val, input.register_b, input.register_c]
        if a_val is not None else
        [input.register_a, input.register_b, input.register_c]
    )

    output = []
    instruction_pointer = 0
    while instruction_pointer < len(input.program):
        op_code = input.program[instruction_pointer]
        literal_operand = input.program[instruction_pointer+1]
        combo_operand = (
            literal_operand if literal_operand <= 3 else
            registers[literal_operand - 4] if literal_operand <= 6 else
            None
        )
        adv_instruction_pointer = True
        match op_code:
            case 0:
                registers[0] = registers[0] // (2 ** combo_operand)
            case 1:
                registers[1] = registers[1] ^ literal_operand
            case 2:
                registers[1] = combo_operand % 8
            case 3:
                if registers[0] != 0:
                    adv_instruction_pointer = False
                    instruction_pointer = literal_operand
            case 4:
                registers[1] = registers[1] ^ registers[2]
            case 5:
                output.append(combo_operand % 8)
            case 6:
                registers[1] = registers[0] // (2 ** combo_operand)
            case 7:
                registers[2] = registers[0] // (2 ** combo_operand)

        if adv_instruction_pointer:
            instruction_pointer += 2

    return output


def part_1(input: Input):
    output = simulate(input)
    return ",".join(map(str, output))


def part_2(input: Input):
    # Thanks Reddit!

    alt_a_options = [0]

    while True:
        alt_a_options_next = []
        for alt_a in alt_a_options:
            for i in range(8):
                result = simulate(input, alt_a | i)
                if result == input.program:
                    return alt_a | i
                if result == input.program[-len(result):]:
                    alt_a_options_next.append((alt_a | i) << 3)
        alt_a_options = alt_a_options_next

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')
    sample_input_2 = parse_input('sample_input.2.txt')

    before = time.time_ns()
    result = part_1(sample_input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1 (sample):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_1(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1:', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(sample_input_2)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2 (sample):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2:', result, f'({_time} ms)')
