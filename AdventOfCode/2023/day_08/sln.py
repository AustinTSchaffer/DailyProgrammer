import re
import dataclasses
import math

@dataclasses.dataclass
class Input:
    instructions: str
    graph: dict[str, tuple[str, str]]

graph_edges_re = re.compile(r'(?P<node>[0-9A-Z]+) = \((?P<left_edge>[0-9A-Z]+), (?P<right_edge>[0-9A-Z]+)\)')

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.read()
        instructions, graph_description = data.split('\n\n')
        return Input(
            instructions,
            {
                m['node']: (m['left_edge'], m['right_edge'])
                for m in graph_edges_re.finditer(graph_description)
            }
        )

def part_1(input: Input):
    current_node = 'AAA'
    destination = 'ZZZ'

    i = 0
    while True:
        if current_node == destination:
            return i

        instruction = input.instructions[i % len(input.instructions)]
        current_node = input.graph[current_node][0 if instruction == 'L' else 1]
        i += 1


def egcd(a: int, b: int) -> tuple[int, int, int]:
    (x0, x1, y0, y1) = (1, 0, 0, 1)
    while b != 0:
        (q, a, b) = (a // b, b, a % b)
        (x0, x1) = (x1, x0 - q * x1)
        (y0, y1) = (y1, y0 - q * y1)
    return (a, x0, y0)


def part_2(input: Input):
    current_nodes = [n for n in input.graph.keys() if n[-1] == 'A']
    history = [{} for _ in current_nodes]
    cycles = [None] * len(current_nodes)

    iteration = 0
    while True:
        if all(map(lambda cl: cl is not None, cycles)):
            # Now we need to find the next time that all of these
            # cycles will line up! Note, for some contrived inputs,
            # this will not be possible.

            # Cycles that touch a "..Z" node more than once frighten me.
            if any(cycle for cycle in cycles if len(cycle[2]) > 1):
                raise NotImplementedError()

            cycle_eqs = [
                (c[0], c[2][0][0])
                for c in cycles
            ]

            # Cycles that don't have the "..Z" node at the end aren't
            # specifically handled, because I wasn't feeling smart enough
            # to actually use the egcd method.
            if any(eq for eq in cycle_eqs if eq[1] not in [0, eq[0]]):
                raise NotImplementedError()

            return math.lcm(*(eq[0] for eq in cycle_eqs))

        if all(map(lambda n: n[-1] == 'Z', current_nodes)):
            return iteration

        instruction_index = iteration % len(input.instructions)
        instruction = input.instructions[instruction_index]
        for ghost_number, node in enumerate(current_nodes):
            history_key = (instruction_index, current_nodes[ghost_number])
            current_nodes[ghost_number] = input.graph[node][0 if instruction == 'L' else 1]

            if cycles[ghost_number] is not None:
                # No need to keep track of history now that we
                # know that the ghost is travelling in a cycle
                # with a known length and a known starting point.
                ...
            elif (history_entry := history[ghost_number].get(history_key)) is not None:
                cycle_length = iteration - history_entry
                cycles[ghost_number] = (
                    cycle_length,  # Cycle length.
                    history_entry, # First occurance of a repeated node.
                    [              # First occurance of a "..Z" node.
                        (v, k[1])
                        for k, v in history[ghost_number].items()
                        if k[1][-1] == 'Z'
                    ],
                )
            else:
                history[ghost_number][history_key] = iteration

        iteration += 1


if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input_1 = parse_input('sample_input.txt')
    sample_input_2 = parse_input('sample_input_2.txt')
    sample_input_3 = parse_input('sample_input_3.txt')
    rachel_input = parse_input('rachel_input.txt')

    print('Part 1 (sample 1):', part_1(sample_input_1))
    print('Part 1 (sample 2):', part_1(sample_input_2))
    print('Part 1:', part_1(input))

    # print('Part 2 (sample 1):', part_2(sample_input_1))
    # print('Part 2 (sample 2):', part_2(sample_input_2))
    # print('Part 2 (sample 3):', part_2(sample_input_3))
    print('Part 2 (Rachel\'s input):', part_2(rachel_input))
    print('Part 2:', part_2(input))
