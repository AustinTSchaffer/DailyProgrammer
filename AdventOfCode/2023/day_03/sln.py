import dataclasses
import re

from typing import Iterable

@dataclasses.dataclass
class MaybePartNumber:
    value: int
    location: tuple[int, int]
    strlen: int

    def surrounding_locations(self) -> Iterable[tuple[int, int]]:
        # Left
        yield (self.location[0], self.location[1] - 1)
        # Right
        yield (self.location[0], self.location[1] + self.strlen)
        for i in range(-1, self.strlen + 1):
            # Above (incl. corners)
            yield (self.location[0] - 1, self.location[1] + i)
            # Below (incl. corners)
            yield (self.location[0] + 1, self.location[1] + i)

@dataclasses.dataclass
class ParsedInput:
    num_rows: int
    maybe_part_numbers: list[MaybePartNumber]
    symbols: dict[tuple[int, int], str]

    def part_numbers(self) -> Iterable[MaybePartNumber]:
        for number in self.maybe_part_numbers:
            for location in number.surrounding_locations():
                if location in self.symbols:
                    yield number

    def gears(self) -> Iterable[tuple[tuple[int, int], MaybePartNumber, MaybePartNumber]]:
        line_to_num_lookup: list[list[MaybePartNumber]] = [[] for _ in range(self.num_rows+2)]
        for number in self.maybe_part_numbers:
            line_to_num_lookup[number.location[0]+1].append(number)

        for location, symbol in self.symbols.items():
            if symbol == '*':
                adj_nums = []
                for nearby_rows in line_to_num_lookup[location[0]:location[0]+3]:
                    for number in nearby_rows:
                        if any(loc == location for loc in number.surrounding_locations()):
                            adj_nums.append(number)
                if len(adj_nums) == 2:
                    yield (location, adj_nums[0], adj_nums[1])


def parse_input(filename: str) -> ParsedInput:
    maybe_part_numbers = []
    symbols = {}
    with open(filename, 'r') as f:
        for row_idx, line in enumerate(f):
            for col_idx, char in enumerate(line):
                if char != '.' and not str.isspace(char) and not str.isnumeric(char):
                    symbols[(row_idx, col_idx)] = char
            for match_ in re.finditer(r'\d+', line):
                span = match_.span()
                maybe_part_numbers.append(MaybePartNumber(
                    value=int(match_[0]),
                    location=(row_idx, span[0]),
                    strlen=span[1] - span[0],
                ))

    return ParsedInput(
        maybe_part_numbers=maybe_part_numbers,
        symbols=symbols,
        num_rows=row_idx+1,
    )

if __name__ == '__main__':
    sample_input = parse_input("sample_input.txt")
    input = parse_input("input.txt")

    print("Part 1 (sample):", sum(pn.value for pn in sample_input.part_numbers()))
    print("Part 1:", sum(pn.value for pn in input.part_numbers()))

    print("Part 2 (sample):", sum(num1.value * num2.value for loc, num1, num2 in sample_input.gears()))
    print("Part 2:", sum(num1.value * num2.value for loc, num1, num2 in input.gears()))
