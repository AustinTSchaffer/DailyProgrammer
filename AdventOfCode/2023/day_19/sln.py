import re
import dataclasses
import timeit
from typing import NamedTuple, Literal
import math

XMAS = 'xmas'
PART_RE = re.compile(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}')
WORKFLOW_RE = re.compile(r'(?P<id>.+)\{(?P<rules>.+)\}')
WORKFLOW_RULE_RE = re.compile(r'(?:(?P<prop>[xmas])(?P<op>[<>])(?P<val>\d+):)?(?P<dest>\w+)')

class Part(NamedTuple):
    x: int
    """Extremely cool looking score."""
    m: int
    """Musical score."""
    a: int
    """Aerodynamic score."""
    s: int
    """Shiny score."""

    def __repr__(self):
        return f'{{x={self.x},m={self.m},a={self.a},s={self.s}}}'

class PartRange(NamedTuple):
    """
    Describes a whole range of different part evaluations. Instead of each
    metric containing a single score, each metric contains a range of scores
    that can be given to that metric.

    These ranges are inclusive. Both ends of each range are contained
    within the range.
    """

    x: tuple[int, int]
    """Extremely cool looking score range."""
    m: tuple[int, int]
    """Musical score range."""
    a: tuple[int, int]
    """Aerodynamic score range."""
    s: tuple[int, int]
    """Shiny score range."""

    def __repr__(self):
        return f'{{x={self.x},m={self.m},a={self.a},s={self.s}}}'

    @classmethod
    def initial(cls):
        """
        Returns an instance of a PartRange, with the configuration as described
        in Part 2, with all metrics having a range of 1 to 4k.
        """
        return cls(*([(1, 4000)] * 4))

    def num_combinations(self):
        """
        Returns the number of different combinations of each metric
        that can be described using this range. It's just the product
        of the number of values contained in each sub range.
        """
        return math.prod(
            1 + range_[1] - range_[0]
            for range_ in self
        )


@dataclasses.dataclass
class Workflow:
    @dataclasses.dataclass
    class Rule:
        class Comparison(NamedTuple):
            part_prop: int
            """
            The index of a property of a Part or PartRange.
            Based on `"xmas"`. (See @XMAS)
            """
            operator: Literal['<', '>']
            value: int

        dest: str
        """
        The ID of another workflow.
        """

        comp: Comparison | None

        def __repr__(self):
            return f'{f'{XMAS[self.comp.part_prop]}{self.comp.operator}{self.comp.value}:' if self.comp else ''}{self.dest}'

        def apply(self, part: Part) -> str | None:
            """
            If this rule matches the part, returns the ID of the destination workflow.
            Otherwise, returns None.
            """
            if not self.comp:
                return self.dest
            if self.comp[1] == '<' and part[self.comp[0]] < self.comp[2]:
                return self.dest
            if self.comp[1] == '>' and part[self.comp[0]] > self.comp[2]:
                return self.dest
            return None

        def apply_range(self, pr: PartRange) -> list[tuple[str | None, PartRange]]:
            """
            If this rule applies any subset of parts that are contained within the
            part range, this will return the rule's destination along with that subset.
            If there is any remainder, that remainder will also be returned, without
            any explicit destination. This is denoted with `None`.
            """
            if not self.comp:
                return [(self.dest, pr)]

            pr_subrange = pr[self.comp.part_prop]
            if pr_subrange[0] <= self.comp.value <= pr_subrange[1]:
                # Split pr into a lower and upper range.

                lower_range = [*pr]
                lower_range[self.comp.part_prop] = (
                    pr_subrange[0],
                    self.comp.value - (1 if self.comp.operator == '<' else 0)
                )

                upper_range = [*pr]
                upper_range[self.comp.part_prop] = (
                    self.comp.value + (1 if self.comp.operator == '>' else 0),
                    pr_subrange[1]
                )

                return [
                    (self.dest if self.comp.operator == '<' else None, PartRange(*lower_range)),
                    (self.dest if self.comp.operator == '>' else None, PartRange(*upper_range)),
                ]

            elif self.comp.value < pr_subrange[0]:
                # The comparison's value falls below the subrange associated with the part range property.
                # Return the part range, with the destination depending on the rule's comparison operator.
                return [(self.dest if self.comp.operator == '>' else None, pr)]

            elif pr_subrange[1] < self.comp.value:
                # The comparison's value falls above the subrange associated with the part range property.
                # Return the part range, with the destination depending on the rule's comparison operator.
                return [(self.dest if self.comp.operator == '<' else None, pr)]

            raise ValueError(self, pr)

    id: str
    rules: list[Rule]

    def __repr__(self):
        return f'{self.id}{{{','.join(repr(r) for r in self.rules)}}}'

    def apply(self, part: Part) -> str:
        """
        Returns the ID of another workflow, based on this workflow's
        part-matching rules.
        """

        for rule in self.rules:
            if (result := rule.apply(part)) is not None:
                return result

        raise ValueError(self, part)

    def apply_range(self, pr: PartRange) -> list[tuple[str, PartRange]]:
        """
        Splits the input PartRange into multiple subranges, along with the
        IDs of other workflows that should be applied to those subranges,
        based on this workflow's part-matching rules.
        """

        output = []
        unprocessed = [pr]
        for rule in self.rules:
            next_round = []
            for _pr in unprocessed:
                new_prs = rule.apply_range(_pr)
                for new_pr in new_prs:
                    if new_pr[0] is not None:
                        output.append(new_pr)
                    else:
                        next_round.append(new_pr[1])
            unprocessed = next_round

        assert len(unprocessed) == 0
        return output


@dataclasses.dataclass
class Input:
    workflows: dict[str, Workflow]
    parts: list[Part]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        workflows_raw, parts_raw = f.read().split('\n\n')

        workflows = {
            wfm['id']: Workflow(
                wfm['id'],
                [
                    Workflow.Rule(
                        comp=Workflow.Rule.Comparison(
                            XMAS.index(wfrm['prop']),
                            wfrm['op'],
                            int(wfrm['val']),
                        ) if wfrm['prop'] else None,
                        dest=wfrm['dest'],
                    )
                    for wfrm in WORKFLOW_RULE_RE.finditer(wfm['rules'])
                ]
            )
            for line in workflows_raw.split('\n')
            if (wfm := WORKFLOW_RE.match(line))
        }

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
    results: dict[str, list[PartRange]] = {'R': [], 'A': []}
    prs = [('in', PartRange.initial())]
    while len(prs) > 0:
        wfid, pr = prs.pop()
        new_prs = input.workflows[wfid].apply_range(pr)
        for new_pr in new_prs:
            if new_pr[0] in results:
                results[new_pr[0]].append(new_pr[1])
            else:
                prs.append(new_pr)

    return sum(
        pr.num_combinations()
        for pr in results['A']
    )

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
