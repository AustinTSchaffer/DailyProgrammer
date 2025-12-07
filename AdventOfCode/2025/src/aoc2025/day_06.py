import re

Input = tuple[list[list[int]], list[list[int]], list[str]]

def transform(input: str) -> Input:
    *values, operators = input.split('\n')

    values_part_1 = [
        [
            int(value)
            for value in line.split()
            if value
        ]
        for line in values
    ]

    operators = [
        op for op in
        operators.split()
        if op
    ]

    col_widths = [
        len(r) for r in
        re.findall(r"([+*]\s*)", input)
    ]

    all_values_part_2 = []

    for col_width in col_widths:
        column = [
            value_row[:col_width]
            for value_row in values
        ]

        values = [
            value_row[col_width:]
            for value_row in values
        ]

        values_part_2 = ["" for _ in range(len(column[0]))]
        for row in column:
            for col_idx, digit in enumerate(row):
                values_part_2[col_idx] += digit

        all_values_part_2.append([
            int(value.strip())
            for value in values_part_2
            if value.strip()
        ])

    return values_part_1, all_values_part_2, operators

def part_1(input: Input):
    values_part_1, _, operators = input

    acc = values_part_1[0].copy()
    for values in values_part_1[1:]:
        for idx, (acc_val, val, op) in enumerate(zip(acc, values, operators)):
            acc[idx] = (
                acc_val + val
                if op == "+" else
                acc_val * val
            )
    return sum(acc)

def part_2(input: Input):
    _, values_part_2, operators = input

    result = 0
    for op, values in zip(operators, values_part_2):
        if op == '+':
            result += sum(values)
        elif op == "*":
            local_result = values[0]
            for value in values[1:]:
                local_result *= value
            result += local_result

    return result
