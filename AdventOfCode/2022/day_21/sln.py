import dataclasses
from typing import Union
import re
import collections
import graphlib

@dataclasses.dataclass
class Expression:
    term_variables: tuple[str, str]
    operator: str


expression_re = re.compile(r"(?P<key>\w{4}): ((?P<value>\d+)|((?P<term_1_var>\w{4}) (?P<operator>.) (?P<term_2_var>\w{4})))")


def apply(input: dict[str, int | Expression], expression: int | Expression, raise_if_number=False) -> int:
    if isinstance(expression, int | float):
        if raise_if_number:
            raise ValueError()
        return expression

    if not isinstance(term_a := input[expression.term_variables[0]], int | float):
        raise ValueError(input[expression.term_variables[0]])

    if not isinstance(term_b := input[expression.term_variables[1]], int | float):
        raise ValueError(input[expression.term_variables[1]])

    if expression.operator == '+':
        return term_a + term_b

    if expression.operator == '-':
        return term_a - term_b

    if expression.operator == '*':
        return term_a * term_b

    if expression.operator == '/':
        return term_a / term_b

    raise NotImplementedError(expression.operator)


def parse_input(filename) -> dict[str, int | Expression]:
    output = {}
    with open(filename, "r") as f:
        for expression_match in expression_re.finditer(f.read()):
            key = expression_match["key"]
            expression_match = expression_match.groupdict()
            if (value := expression_match['value']) is not None:
                output[key] = int(value)
            else:
                output[key] = Expression(
                    (expression_match["term_1_var"], expression_match["term_2_var"]),
                    expression_match["operator"]
                )

    return output


def part_1(input: dict[str, int | Expression]) -> int:
    input = input.copy()
    dag = graphlib.TopologicalSorter()
    for key, expr in input.items():
        if isinstance(expr, Expression):
            dag.add(key, *expr.term_variables)

    for expr_key in dag.static_order():
        input[expr_key] = apply(input, input[expr_key])

    return input["root"]


def part_2(input: dict[str, int | Expression]) -> int:
    """
    This works for the sample input, but not for the actual input.
    This was replaced by part2attempt2, which just tries a ton of possibliities.
    Trying out different values for the bounds and step eventually resulted in finding the
    right solution.
    """

    input = input.copy()

    input["root"].operator = "=="
    input["humn"] = None

    still_simplifying = True
    while still_simplifying:
        still_simplifying = False
        for key, expression in input.items():
            if key not in ("root", "humn"):
                try:
                    result = apply(input, expression, raise_if_number=True)
                    input[key] = result
                    still_simplifying = True
                except:
                    ...

    key = 'root'
    rewritten_expressions = {}
    while key != 'humn':
        expression = input[key]
        expression_expression_is_first = True
        expression_expression, value_expression = input[expression.term_variables[0]], input[expression.term_variables[1]]
        expression_key, value_key = expression.term_variables[0], expression.term_variables[1]

        if isinstance(expression_expression, Expression) and isinstance(value_expression, Expression):
            raise ValueError()

        if isinstance(expression_expression, int | float):
            expression_expression, value_expression = value_expression, expression_expression
            expression_key, value_key = value_key, expression_key
            expression_expression_is_first = False

        if expression.operator == '==':
            rewritten_expressions[expression_key] = input[value_key]
        else:
            rewritten_expressions[expression_key] = Expression(
                # term_variables=(value_key, key) if expression_expression_is_first else (key, value_key),
                term_variables=(key, value_key),
                operator=(
                    '+' if expression.operator == '-' else
                    '-' if expression.operator == '+' else
                    '/' if expression.operator == '*' else
                    '*'
                )
            )

        key = expression_key

    rewritten_input = {
        **input,
        **rewritten_expressions,
    }

    del rewritten_input['root']

    dag = graphlib.TopologicalSorter()
    for key, expr in rewritten_input.items():
        if isinstance(expr, Expression):
            dag.add(key, *expr.term_variables)

    for expr_key in dag.static_order():
        rewritten_input[expr_key] = apply(rewritten_input, rewritten_input[expr_key])

    return rewritten_input["humn"]


def part_2_attempt_2(input: dict[str, int | Expression], starting_guess: int, numbers_to_check: int = 10000, step: int = 1):
    input_backup = input.copy()
    input_backup['humn'] = None
    terms_of_root = input_backup['root'].term_variables

    still_simplifying = True
    while still_simplifying:
        still_simplifying = False
        for key, expression in input_backup.items():
            if key not in ("root", "humn"):
                try:
                    result = apply(input_backup, expression, raise_if_number=True)
                    input_backup[key] = result
                    still_simplifying = True
                except:
                    ...

    for iter, guess_for_humn in enumerate(range(starting_guess, starting_guess+(step*numbers_to_check)+1, step)):
        if iter % 100 == 0:
            print(f"Trying {guess_for_humn} for humn...", end=" ")

        working_copy = input_backup.copy()
        del working_copy['root']
        working_copy['humn'] = guess_for_humn

        dag = graphlib.TopologicalSorter()
        for key, expr in working_copy.items():
            if isinstance(expr, Expression):
                dag.add(key, *expr.term_variables)

        for expr_key in dag.static_order():
            working_copy[expr_key] = apply(working_copy, working_copy[expr_key])

        if working_copy[terms_of_root[0]] == working_copy[terms_of_root[1]]:
            print("it worked!")
            return guess_for_humn
        elif working_copy[terms_of_root[0]] > working_copy[terms_of_root[1]]:
            if iter % 100 == 0:
                print(f"{working_copy[terms_of_root[0]]} > {working_copy[terms_of_root[1]]}")
        else:
            if iter % 100 == 0:
                print(f"{working_copy[terms_of_root[0]]} < {working_copy[terms_of_root[1]]}")


    raise ValueError(f"Answer not found between {starting_guess} and {starting_guess+(step*numbers_to_check)+1}, (step = {step}).")


if __name__ == "__main__":
    sample_input = parse_input("sample_input.txt")
    input = parse_input("input.txt")

    print(f"Part 1 (sample):", part_1(sample_input))
    print(f"Part 1:", part_1(input))

    print(f"Part 2 (sample):", part_2(sample_input))
    print(f"Part 2:", part_2_attempt_2(input, 3916936880000, numbers_to_check=1000, step=1))

    # print(f"Part 2 (sample):", part_2_attempt_2(sample_input, 301))
    # print(f"Part 2:", part_2_attempt_2(input, 600))

    # print(f"Part 2:", part_2_attempt_2(input, 600))
