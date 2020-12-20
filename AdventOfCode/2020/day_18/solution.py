#%%

expressions = [
    line.strip().replace(" ", "") for line in
    open("math_expressions.txt").readlines()
]

import re

simple_expression = re.compile(r"\d+[+*]\d+")
single_number_in_parens = re.compile(r"\((\d+)\)")

def perform_operation(match: re.Match) -> str:
    return 

part_1_results = {}
for expression in expressions:
    original_expression = expression
    operations_performed = 1
    while operations_performed > 0:
        operations_performed = 0

        expression, num_simple_expressions_performed = simple_expression.subn(
            repl=lambda match: str(eval(match[0])),
            string=expression,
            count=1,
        )

        operations_performed += num_simple_expressions_performed

        expression, num_parens_dropped = single_number_in_parens.subn(
            repl=r"\1",
            string=expression,
        )

        operations_performed += num_parens_dropped

    part_1_results[original_expression] = int(expression)

print("Part 1:", sum(part_1_results.values()))


class AddAndMulSwapped:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return AddAndMulSwapped(self.value * other.value)

    def __mul__(self, other):
        return AddAndMulSwapped(self.value + other.value)

part_2_results = {}
for expression in expressions:
    original_expression = expression

    expression = re.sub(
        pattern=r"(\d+)",
        repl=r"AddAndMulSwapped(\1)",
        string=expression,
    )

    expression = expression.replace("+", "-").replace("*", "+").replace("-", "*")
    part_2_results[original_expression] = int(eval(expression).value)

print("Part 2:", sum(part_2_results.values()))

#%%
