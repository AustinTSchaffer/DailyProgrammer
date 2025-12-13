import dataclasses
import re
from collections import deque
from queue import PriorityQueue
import random
import itertools

import z3

@dataclasses.dataclass(frozen=True)
class Machine:
    original: str
    indicator_diagram: tuple[bool]
    indicator_diagram_int: int
    buttons: tuple[tuple[int, ...]]
    buttons_int: tuple[int, ...]
    joltage_requirements: tuple[int]


def transform(input: str) -> list[Machine]:
    machines = []
    for machine_str in input.splitlines():
        indicator_diagram, *buttons, joltage_req = machine_str.split(" ")

        indicator_diagram = tuple(
            [char == "#" for char in indicator_diagram.strip("][")]
        )

        indicator_diagram_int = sum(
            2**idx for idx, indicator in enumerate(indicator_diagram) if indicator
        )

        buttons = [tuple(map(int, b.strip(")(").split(","))) for b in buttons]
        buttons_int = [sum(2**indicator for indicator in button) for button in buttons]

        joltage_req = tuple(map(int, joltage_req.strip("}{").split(",")))

        machines.append(
            Machine(
                original=machine_str,
                indicator_diagram=indicator_diagram,
                indicator_diagram_int=indicator_diagram_int,
                buttons=buttons,
                buttons_int=buttons_int,
                joltage_requirements=joltage_req,
            )
        )

    return machines


def presses_req_p1(machine: Machine) -> int:
    """
    Fairly bog-standard BFS implementation with path reconstruction.
    """
    queue = deque([0])
    traversal_order = {}
    while queue:
        current_node = queue.popleft()
        if current_node == machine.indicator_diagram_int:
            _presses_req = 0
            while current_node != 0:
                current_node = traversal_order[current_node]
                _presses_req += 1
            return _presses_req
        for button in machine.buttons_int:
            neighbor = current_node ^ button
            if neighbor not in traversal_order:
                queue.append(neighbor)
                traversal_order[neighbor] = current_node
    raise ValueError()


def part_1(input: list[Machine]):
    return sum(map(presses_req_p1, input))


def presses_req_p2(machine: Machine) -> int:
    """
    Fairly bog-standard Dijkstra implementation with path reconstruction.
    """
    n_indicators = len(machine.indicator_diagram)
    starting_node = tuple([0 for _ in range(n_indicators)])
    queue = PriorityQueue()
    queue.put((max(machine.joltage_requirements), starting_node))
    traversal_order = {}
    while queue:
        prio, current_node = queue.get()
        if current_node == machine.joltage_requirements:
            _presses_req = 0
            while current_node != starting_node:
                current_node = traversal_order[current_node]
                _presses_req += 1
            return _presses_req
        for button in machine.buttons:
            neighbor = tuple(
                [
                    current_node[idx] + 1 if idx in button else current_node[idx]
                    for idx in range(n_indicators)
                ]
            )

            diffs = [b - a for b, a in zip(machine.joltage_requirements, neighbor)]

            if any(val < 0 for val in diffs):
                continue

            if neighbor not in traversal_order:
                queue.put((prio + max(diffs), neighbor))
                traversal_order[neighbor] = current_node
    raise ValueError()


def partitions(n, k):
    """
    "Stars and Bars" implementation, hand-stolen from Stack Overflow (not
    laundered through Copilot).
    """
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]


def presses_req_p2_attempt2(machine: Machine) -> int:
    min_presses = sum(machine.joltage_requirements) // max(len(b) for b in machine.buttons)
    max_presses = sum(machine.joltage_requirements)
    button_priority = sorted(machine.buttons, key=lambda _: random.random())
    for n_presses in range(min_presses, max_presses + 1):
        for presses_partition in partitions(n_presses, len(button_priority)):
            result = [0] * len(machine.joltage_requirements)
            for button_idx, presses in enumerate(presses_partition):
                for indicator in button_priority[button_idx]:
                    result[indicator] += presses

            if tuple(result) == machine.joltage_requirements:
                return n_presses

    raise ValueError()

def presses_req_p2_z3_solver(machine: Machine) -> int:
    solver = z3.Solver()

    buttons = []
    joltage_affectors = [[] for _ in range(len(machine.joltage_requirements))]
    for idx, button in enumerate(machine.buttons):
        button_z3 = z3.Int(f'b_{idx}')
        solver.add(button_z3 >= 0)
        buttons.append(button_z3)
        for joltage_idx in button:
            joltage_affectors[joltage_idx].append(button_z3)

    total_presses = z3.Int('total_presses')
    solver.add(total_presses == sum(buttons))
    solver.add(total_presses >= max(machine.joltage_requirements))

    for jr_idx, jr in enumerate(machine.joltage_requirements):
        solver.add(sum(joltage_affectors[jr_idx]) == jr)

    best_so_far = sum(machine.joltage_requirements)
    solver.add(total_presses < best_so_far)
    while solver.check() == z3.sat:
        model = solver.model()
        best_so_far = model.eval(total_presses).py_value()
        solver.add(total_presses < best_so_far)

    return best_so_far

def part_2(input: list[Machine]):
    return sum(map(presses_req_p2_z3_solver, input))
