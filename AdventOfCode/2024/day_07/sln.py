import re
import dataclasses
import time
from typing import Any
import itertools

Input = list[tuple[int, list[int]]]

def parse_input(filename: str) -> Input:
    output = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            result, *terms = line.split()
            result = int(result.strip(": "))
            terms = [int(term.strip()) for term in terms]
            output.append((result, terms))
    return output

def part_1(input: Input):
    sum_ = 0

    ops = [
        lambda a, b: a + b,
        lambda a, b: a * b,
    ]

    def operator_seq_generator(length: int):
        output = [None] * length
        for i in range(2**length):
            for j in range(length):
                output[j] = ops[(i >> j) & 1]
            yield output

    for result, terms in input:
        for operator_seq in operator_seq_generator(len(terms) - 1):
            acc = terms[0]
            for term, op in zip(terms[1:], operator_seq):
                acc = op(acc, term)
                if acc > result:
                    break
            if acc == result:
                sum_ += result
                break

    return sum_

def part_2(input: Input):
    sum_ = 0

    ops = [
        lambda a, b: a + b,
        lambda a, b: a * b,
        lambda a, b: int(str(a) + str(b)),
    ]

    def operator_seq_generator(length: int):
        output = [None] * length
        for i in range(3**length):
            for j in range(length):
                output[j] = ops[i % 3]
                i = i // 3
            yield output

    for result, terms in input:
        for operator_seq in operator_seq_generator(len(terms) - 1):
            acc = terms[0]
            for term, op in zip(terms[1:], operator_seq):
                acc = op(acc, term)
                if acc > result:
                    break
            if acc == result:
                sum_ += result
                break

    return sum_
if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    before = time.time_ns()
    result = part_1(sample_input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1 (sample):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_1(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 1:', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(sample_input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2 (sample):', result, f'({_time} ms)')

    before = time.time_ns()
    result = part_2(input)
    _time = (time.time_ns() - before) / 1_000_000

    print('Part 2:', result, f'({_time} ms)')
