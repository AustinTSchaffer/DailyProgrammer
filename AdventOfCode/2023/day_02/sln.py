import dataclasses
import re

COLORS = ("red", "green", "blue")

@dataclasses.dataclass
class Game:
    id: int

    # List of multi-cube draws from the bag. Each draw is
    # represented by a list of integers. Each integer represents
    # the number of cubes drawn from the bag of a single color.
    # The indexes of, and names of, the available colors are
    # defined in the COLORS constant.
    draws: list[list[int]]

game_re = re.compile(r"Game (\d+): (.+)(\n)?")

def parse_input(filename: str) -> list[Game]:
    with open(filename, 'r') as f:
        data = f.read()
    games = []

    for game in game_re.finditer(data):
        draws = []
        for draw_str in game[2].split(';'):
            draw = [0] * len(COLORS)
            for qty_color in draw_str.split(','):
                qty, color = qty_color.strip().split(" ")
                assert color in COLORS
                draw[COLORS.index(color)] = int(qty)
            draws.append(draw)
        games.append(Game(
            id=int(game[1]),
            draws=draws,
        ))

    return games


def game_is_possible(game: Game, condition: dict[str, int]) -> bool:
    quantities = [condition[color] for color in COLORS]

    for draw in game.draws:
        if draw[0] > quantities[0]:
            return False
        if draw[1] > quantities[1]:
            return False
        if draw[2] > quantities[2]:
            return False
    return True


def game_power(game: Game):
    minimum_cubes_required = [0] * len(COLORS)
    for draw in game.draws:
        for i, qty in enumerate(draw):
            if minimum_cubes_required[i] < qty:
                minimum_cubes_required[i] = qty
    
    product = 1
    for cube_requirement in minimum_cubes_required:
        product = product * cube_requirement
    return product

def part_1(games: list[Game], condition: dict[str, int]) -> int:
    total = 0
    for game in games:
        if game_is_possible(game, condition):
            total += game.id

    return total


def part_2(games: list[Game]) -> int:
    return sum(map(game_power, games))


if __name__ == '__main__':
    sample_input = parse_input("sample_input.txt")
    input = parse_input("input.txt")

    part_1_condition = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    print("Part 1 (sample):", part_1(sample_input, part_1_condition))
    print("Part 1:", part_1(input, part_1_condition))

    print("Part 2 (sample):", part_2(sample_input))
    print("Part 2:", part_2(input))

