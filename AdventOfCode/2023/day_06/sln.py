import re
import dataclasses
import math

@dataclasses.dataclass
class Race:
    max_time_allowed_ms: int
    current_record_mm: int

@dataclasses.dataclass
class Input:
    races: list[Race]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        data = f.read()
        data = data.split("\n")
        return Input(
            races=[
                Race(int(t), int(r))
                for t,r in zip(
                    re.findall(r'\d+', data[0]),
                    re.findall(r'\d+', data[1]),
                )]
        )

def calc_distance(time_button_held_ms: int, total_race_time_ms: int) -> int:
    velocity_mm_p_ms = time_button_held_ms
    return velocity_mm_p_ms * (total_race_time_ms - time_button_held_ms)


def solve_equation(race: Race) -> tuple[int, int]:
    # dist = -(time_button_held)^2 + (race.total_race_time_ms)x
    # dict > race.current_record_mm
    # y = -x^2 + (race.total_race_time_ms)x - (race.current_record_mm)

    a = -1
    b = race.max_time_allowed_ms
    c = -race.current_record_mm

    sqrt_term = math.sqrt(b**2 - (4*a*c))

    left_sln = (-b - sqrt_term) / (2*a)
    right_sln = (-b + sqrt_term) / (2*a)

    return tuple(sorted((left_sln, right_sln)))


def get_num_winning_values(race: Race) -> int:
    left_sln, right_sln = solve_equation(race)
    leading_edge = int(left_sln)
    falling_edge = int(right_sln)
    return falling_edge - leading_edge + (-1 if leading_edge == left_sln and falling_edge == right_sln else 0)

def part_1(input: Input):
    product = 1
    for race in input.races:
        product *= get_num_winning_values(race)
    return product

def part_2(input: Input):
    race = Race(
        int(''.join(str(r.max_time_allowed_ms) for r in input.races)),
        int(''.join(str(r.current_record_mm) for r in input.races)),
    )

    return get_num_winning_values(race)

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
