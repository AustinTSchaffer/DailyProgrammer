import re
import dataclasses

BLIZZARD_GLYPHS = [ '^', 'V', '<', '>' ]

@dataclasses.dataclass(frozen=True)
class Input:
    blizzard_glyphs: dict[tuple[int, int], list[int]]
    start: tuple[int, int]
    end: tuple[int, int]
    width: int
    height: int

def parse_input(filename: str) -> Input:
    blizzard_glyphs = {}
    start = None
    end = None
    width = 0
    height = 0

    with open(filename, 'r') as f:
        for row_idx, row in f:
            for col_idx, value in row:
                if value == '#':
                    continue
                location = (row_idx, col_idx - 1)
                if start is None:
                    start = location

                if (glyph_index := BLIZZARD_GLYPHS.in)
                    blizzard_glyphs[location] = []
            height = col_idx - 1
        width = row_idx - 1
        end = location
    
    return Input(
        blizzard_glyphs=blizzard_glyphs,
        start=start,
        end=end,
        width=width,
        height=height,
    )



def part_1(input):
    ...

def part_2(input):
    ...

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
