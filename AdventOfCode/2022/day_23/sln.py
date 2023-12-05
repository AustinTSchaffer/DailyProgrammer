import dataclasses
from typing import Any, Union

def parse_input(filename: str) -> set[tuple[int, int]]:
    with open(filename, 'r') as f:
        return {
            (i,j)
            for i, row in enumerate(f)
            for j, val in enumerate(row)
            if val == '#'
        }

@dataclasses.dataclass(frozen=True)
class CompassDirections:
    location: tuple[int, int]

    @property
    def north(self):
        return (self.location[0] - 1, self.location[1])
    @property
    def south(self):
        return (self.location[0] + 1, self.location[1])
    @property
    def east(self):
        return (self.location[0], self.location[1] + 1)
    @property
    def west(self):
        return (self.location[0], self.location[1] - 1)
    @property
    def north_east(self):
        return (self.location[0] - 1, self.location[1] + 1)
    @property
    def north_west(self):
        return (self.location[0] - 1, self.location[1] - 1)
    @property
    def south_east(self):
        return (self.location[0] + 1, self.location[1] + 1)
    @property
    def south_west(self):
        return (self.location[0] + 1, self.location[1] - 1)
    @property
    def surrounding_positions(self):
        yield self.north
        yield self.east
        yield self.south
        yield self.west
        yield self.north_east
        yield self.north_west
        yield self.south_east
        yield self.south_west

    def __hash__(self):
        return hash(self.location)

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.location == other
        return self.location == other.location

    def __getattribute__(self, __name: str) -> Any:
        if __name == 0 or __name == 1:
            return self.location[__name]
        return super().__getattribute__(__name)


def print_state(elf_positions: set[Union[tuple[int, int], CompassDirections]]):
    min_x, max_x, min_y, max_y = None, None, None, None
    for position in elf_positions:
        if isinstance(position, CompassDirections):
            position = position.location

        if min_x is None:
            min_x, max_x, min_y, max_y = position[1], position[1], position[0], position[0]
            continue

        if position[1] < min_x:
            min_x = position[1]
        if position[1] > max_x:
            max_x = position[1]
        if position[0] < min_y:
            min_y = position[0]
        if position[0] > max_y:
            max_y = position[0]

    for i in range(min_y, max_y+1):
        for j in range(min_x, max_x+1):
            print('#' if (i,j) in elf_positions else '.', end='')
        print()

def simulate_rounds(elf_positions: set[tuple[int, int]], num_rounds=10) -> set[tuple[int, int]]:
    current_round = { CompassDirections(e) for e in elf_positions }
    round_num = 0
    while True:
        if num_rounds is not None and round_num >= num_rounds:
            break

        next_round = {}

        round_move_proposals = [
            (lambda: not (nw_in_cr or n_in_cr or ne_in_cr), lambda: next_round.setdefault(north, []).append(elf)),
            (lambda: not (sw_in_cr or s_in_cr or se_in_cr), lambda: next_round.setdefault(south, []).append(elf)),
            (lambda: not (nw_in_cr or w_in_cr or sw_in_cr), lambda: next_round.setdefault(west, []).append(elf)),
            (lambda: not (ne_in_cr or e_in_cr or se_in_cr), lambda: next_round.setdefault(east, []).append(elf))
        ]

        any_elves_made_a_proposal = False
        for elf in current_round:
            nw_in_cr, n_in_cr, ne_in_cr, e_in_cr, se_in_cr, s_in_cr, sw_in_cr, w_in_cr = (
                (elf.north_west in current_round),
                ((north := elf.north) in current_round),
                (elf.north_east in current_round),
                ((east := elf.east) in current_round),
                (elf.south_east in current_round),
                ((south := elf.south) in current_round),
                (elf.south_west in current_round),
                ((west := elf.west) in current_round),
            )

            if not (nw_in_cr or n_in_cr or ne_in_cr or e_in_cr or se_in_cr or s_in_cr or sw_in_cr or w_in_cr):
                next_round.setdefault(elf, []).append(elf)
                continue

            made_a_proposal = False
            for proposal_idx in range(len(round_move_proposals)):
                if (proposal := round_move_proposals[(round_num + proposal_idx) % len(round_move_proposals)])[0]():
                    proposal[1]()
                    made_a_proposal = True
                    any_elves_made_a_proposal = True
                    break

            if not made_a_proposal:
                next_round.setdefault(elf.location, []).append(elf)

        actual_next_round = set()
        for new_location, elves in next_round.items():
            if len(elves) == 1:
                if new_location == elves[0]:
                    actual_next_round.add(elves[0])
                else:
                    actual_next_round.add(CompassDirections(new_location))
            else:
                for elf in elves:
                    actual_next_round.add(elf)

        current_round = actual_next_round
        if not any_elves_made_a_proposal:
            break
        round_num += 1

    return { e.location for e in current_round }, round_num

def part_1(elf_positions: set[tuple[int, int]]):
    elf_positions, _ = simulate_rounds(elf_positions)

    min_x, max_x, min_y, max_y = None, None, None, None
    for position in elf_positions:
        if min_x is None:
            min_x, max_x, min_y, max_y = position[1], position[1], position[0], position[0]
            continue

        if position[1] < min_x:
            min_x = position[1]
        if position[1] > max_x:
            max_x = position[1]
        if position[0] < min_y:
            min_y = position[0]
        if position[0] > max_y:
            max_y = position[0]

    return ((1 + max_x - min_x) * (1 + max_y - min_y)) - len(elf_positions)

def part_2(elf_positions: set[tuple[int, int]]):
    _, round_num = simulate_rounds(elf_positions, None)
    return round_num + 1

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print("Part 1 (sample):", part_1(sample_input))
    print("Part 1:", part_1(input))

    print("Part 2 (sample):", part_2(sample_input))
    print("Part 2:", part_2(input))
