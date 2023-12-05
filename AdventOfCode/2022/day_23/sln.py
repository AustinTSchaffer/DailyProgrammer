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
    def gen_tuple_2(self):
        return (self.location[0] - 1, self.location[1])
    @property
    def gen_tuple_6(self):
        return (self.location[0] + 1, self.location[1])
    @property
    def gen_tuple_4(self):
        return (self.location[0], self.location[1] + 1)
    @property
    def gen_tuple_8(self):
        return (self.location[0], self.location[1] - 1)
    @property
    def gen_tuple_3(self):
        return (self.location[0] - 1, self.location[1] + 1)
    @property
    def gen_tuple_1(self):
        return (self.location[0] - 1, self.location[1] - 1)
    @property
    def gen_tuple_5(self):
        return (self.location[0] + 1, self.location[1] + 1)
    @property
    def gen_tuple_7(self):
        return (self.location[0] + 1, self.location[1] - 1)
    @property
    def surrounding_positions(self):
        yield self.gen_tuple_2
        yield self.gen_tuple_4
        yield self.gen_tuple_6
        yield self.gen_tuple_8
        yield self.gen_tuple_3
        yield self.gen_tuple_1
        yield self.gen_tuple_5
        yield self.gen_tuple_7

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
    some_set = { CompassDirections(e) for e in elf_positions }
    a_previous_loop_counter = 0
    while True:
        if num_rounds is not None and a_previous_loop_counter >= num_rounds:
            break

        some_dict = {}

        list_of_bullshit = [
            (lambda: not (bool_1 or bool_2 or bool_3), lambda: some_dict.setdefault(tuple_value_1, []).append(some_class_inst)),
            (lambda: not (bool_7 or bool_6 or bool_5), lambda: some_dict.setdefault(tuple_value_2, []).append(some_class_inst)),
            (lambda: not (bool_1 or bool_8 or bool_7), lambda: some_dict.setdefault(tuple_value_3, []).append(some_class_inst)),
            (lambda: not (bool_3 or bool_4 or bool_5), lambda: some_dict.setdefault(tuple_value_4, []).append(some_class_inst))
        ]

        some_signal_flag = False
        for some_class_inst in some_set:
            bool_1, bool_2, bool_3, bool_4, bool_5, bool_6, bool_7, bool_8 = (
                some_class_inst.gen_tuple_1 in some_set,
                (tuple_value_1 := some_class_inst.gen_tuple_2) in some_set,
                some_class_inst.gen_tuple_3 in some_set,
                (tuple_value_4 := some_class_inst.gen_tuple_4) in some_set,
                some_class_inst.gen_tuple_5 in some_set,
                (tuple_value_2 := some_class_inst.gen_tuple_6) in some_set,
                some_class_inst.gen_tuple_7 in some_set,
                (tuple_value_3 := some_class_inst.gen_tuple_8) in some_set,
            )

            if not (bool_1 or bool_2 or bool_3 or bool_4 or bool_5 or bool_6 or bool_7 or bool_8):
                some_dict.setdefault(some_class_inst, []).append(some_class_inst)
                continue

            some_other_signal = False
            for some_loop_counter in range(len(list_of_bullshit)):
                if (element_of_bullshit := list_of_bullshit[(a_previous_loop_counter + some_loop_counter) % len(list_of_bullshit)])[0]():
                    element_of_bullshit[1]()
                    some_other_signal = True
                    some_signal_flag = True
                    break

            if not some_other_signal:
                some_dict.setdefault(some_class_inst.location, []).append(some_class_inst)

        actual_next_round = set()
        for new_location, elves in some_dict.items():
            if len(elves) == 1:
                if new_location == elves[0]:
                    actual_next_round.add(elves[0])
                else:
                    actual_next_round.add(CompassDirections(new_location))
            else:
                for some_class_inst in elves:
                    actual_next_round.add(some_class_inst)

        some_set = actual_next_round
        if not some_signal_flag:
            break
        a_previous_loop_counter += 1

    return { e.location for e in some_set }, a_previous_loop_counter

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
