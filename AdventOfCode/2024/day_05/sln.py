import re
import dataclasses
import time
from typing import Any
import collections

@dataclasses.dataclass
class Input:
    page_ordering_rules: list[tuple[int, int]]
    page_updates: list[list[int]]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.read()

    page_ordering_rules, page_updates = data.split('\n\n')
    page_ordering_rules = [
        tuple(map(int, rule.split('|')))
        for rule in page_ordering_rules.split('\n')
        if rule
    ]

    page_updates = [
        list(map(int, update.split(',')))
        for update in page_updates.split('\n')
        if update
    ]

    return Input(
        page_ordering_rules=page_ordering_rules,
        page_updates=page_updates
    )


def part_1(input: Input):
    page_ordering_rev_dag: dict[int, set[int]] = {}
    for rule in input.page_ordering_rules:
        if list_ := page_ordering_rev_dag.get(rule[1]):
            list_.add(rule[0])
        else:
            page_ordering_rev_dag[rule[1]] = {rule[0]}

    def _valid_update_print_order(update: list[int]):
        pages_printed_so_far = []
        for page_to_print in update:
            if page_deps := page_ordering_rev_dag.get(page_to_print):
                relevant_deps = page_deps.intersection(update)
                diff = relevant_deps.difference(pages_printed_so_far)
                if diff:
                    return False

            pages_printed_so_far.append(page_to_print)
        return True

    sum_ = 0
    for update in input.page_updates:
        if _valid_update_print_order(update):
            sum_ += update[len(update) // 2]

    return sum_

def part_2(input: Input):
    page_ordering_rev_dag: dict[int, set[int]] = {}
    for rule in input.page_ordering_rules:
        if list_ := page_ordering_rev_dag.get(rule[1]):
            list_.add(rule[0])
        else:
            page_ordering_rev_dag[rule[1]] = {rule[0]}

    def _reorder_update(update: list[int]):
        list_reordered = False

        pages_to_print = collections.deque(update)
        page_print_order = []

        while len(pages_to_print):
            page_to_print = pages_to_print.popleft()
            if page_deps := page_ordering_rev_dag.get(page_to_print):
                relevant_deps = page_deps.intersection(update)
                diff = relevant_deps.difference(page_print_order)
                if diff:
                    list_reordered = True
                    pages_to_print.append(page_to_print)
                else:
                    page_print_order.append(page_to_print)
            else:
                page_print_order.append(page_to_print)

        return list_reordered, page_print_order

    sum_ = 0
    for update in input.page_updates:
        list_reordered, page_print_order = _reorder_update(update)
        if list_reordered:
            sum_ += page_print_order[len(page_print_order) // 2]

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
