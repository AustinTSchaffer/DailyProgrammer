import re
import dataclasses
import timeit
from typing import NamedTuple, Callable, Literal
from collections import namedtuple

XMAS = 'xmas'
Part = namedtuple('Part', list(XMAS))
PART_RE = re.compile(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}')

@dataclasses.dataclass
class Workflow:
    @dataclasses.dataclass
    class Rule:
        dest: Literal['A'] | Literal['R'] | str
        comp: tuple[
            int,
            Literal['<', '>'],
            int,
        ] | None

        def apply(self, part: Part) -> str | None:
            if not self.comp:
                return self.dest
            if self.comp[1] == '<' and part[self.comp[0]] < self.comp[2]:
                return self.dest
            if self.comp[1] == '>' and part[self.comp[0]] > self.comp[2]:
                return self.dest
            return None

    id: str
    rules: list[Rule]

    def apply(self, part: Part) -> str | None:
        for rule in self.rules:
            if (result := rule.apply(part)) is not None:
                return result
        return None

WORKFLOW_RE = re.compile(r'(?P<id>.+)\{(?P<rules>.+)\}')
WORKFLOW_RULE_RE = re.compile(r'(?:(?P<prop>[xmas])(?P<op>[<>])(?P<val>\d+):)?(?P<dest>\w+)')

@dataclasses.dataclass
class Input:
    workflows: dict[str, Workflow]
    parts: list[Part]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        workflows_raw, parts_raw = f.read().split('\n\n')

        workflows = {}
        for line in workflows_raw.split('\n'):
            wfm = WORKFLOW_RE.match(line)
            workflows[wfm['id']] = Workflow(
                wfm['id'],
                [
                    Workflow.Rule(
                        comp=(
                            XMAS.index(wfrm['prop']),
                            wfrm['op'],
                            int(wfrm['val']),
                        ) if wfrm['prop'] else None,
                        dest=wfrm['dest'],
                    )
                    for wfrm in WORKFLOW_RULE_RE.finditer(wfm['rules'])
                ]
            )

        parts = [
            Part(*map(int, (pm[1], pm[2], pm[3], pm[4])))
            for line in
            parts_raw.split('\n')
            if (pm := PART_RE.match(line))
        ]

        return Input(
            workflows=workflows,
            parts=parts,
        )

def part_1(input: Input):
    results = {'R': [], 'A': []}

    for part in input.parts:
        wfid = 'in'
        while wfid not in results:
            wfid = input.workflows[wfid].apply(part)
        results[wfid].append(part)

    return sum(sum(p) for p in results['A'])

def part_2(input: Input):
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    globals = {'input': input, 'part_1': part_1, 'part_2': part_2}

    part_1_timer = timeit.Timer(
        'global result; result = part_1(input)',
        globals = globals
    )

    part_2_timer = timeit.Timer(
        'global result; result = part_2(input)',
        globals = globals
    )

    print('Part 1 (sample):', part_1(sample_input))
    time = part_1_timer.timeit(1)
    print('Part 1:', globals['result'], f'({time:.3} seconds)')

    print('Part 2 (sample):', part_2(sample_input))
    time = part_2_timer.timeit(1)
    print('Part 2:', globals['result'], f'({time:.3} seconds)')
