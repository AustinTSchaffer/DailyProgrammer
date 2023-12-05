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
    numbers: list[MaybePartNumber]
    symbols: dict[tuple[int, int], str]

    def part_numbers(self) -> Iterable[MaybePartNumber]:
        for number in self.numbers:
            for location in number.surrounding_locations():
                if location in self.symbols:
                    yield number

    def gears(self) -> Iterable[tuple[tuple[int, int], MaybePartNumber, MaybePartNumber]]:
        location_to_number_map: dict[tuple[int, int], MaybePartNumber] = {}
        for number in self.numbers:
            for i in range(number.strlen):
                location_to_number_map[(number.location[0], number.location[1] + i)] = number

        for location, symbol in self.symbols.items():
            if symbol == '*':
                adj_nums: dict[int, MaybePartNumber] = {}
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i != 0 or j != 0:
                            if (number := location_to_number_map.get((location[0]+i, location[1]+j))) is not None:
                                adj_nums[id(number)] = number

                if len(adj_nums) == 2:
                    yield (location, *adj_nums.values())


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
        numbers=maybe_part_numbers,
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
