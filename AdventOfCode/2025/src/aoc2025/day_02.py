import functools
import dataclasses
import math
import common


Input = list[tuple[int, int]]

def transform(input: str) -> Input:
    return [
        tuple(map(int, part.split('-')))
        for part in input.split(',')
    ]

@dataclasses.dataclass(frozen=True)
class Repeater:
    repeater: int
    repeat_val_oom: int
    min_val: int
    max_val: int

def is_repeated(value: int) -> bool:
    if value < 10:
        return False

    value_str = str(value)
    for factor in common.factors(len(value_str), proper=True):
        component = value_str[:factor]
        repetitions = (len(value_str) // factor)
        if (component * repetitions) == value_str:
            return True

    return False

def generate_repeaters(max_value: int, two_fold_only: bool) -> list[Repeater]:
    n_folds = 1
    repeaters: list[Repeater] = []

    log_10_max_value = math.log10(max_value) + 1
    while n_folds <= log_10_max_value:
        n_folds += 1

        repeat_val_oom = 0
        while True:
            repeat_val_oom += 1
            repeater = 1
            for fold in range(n_folds-1):
                repeater += 10 ** (repeat_val_oom+(fold * repeat_val_oom))
            min_val = repeater * (10 ** (repeat_val_oom - 1))

            if min_val > max_value:
                break
            
            repeaters.append(Repeater(
                repeater=repeater,
                repeat_val_oom=repeat_val_oom,
                min_val=min_val,
                max_val=(10 ** (n_folds * repeat_val_oom)) - 1,
            ))

        if two_fold_only:
            break

    return repeaters

def generate_repeated_values(repeater: Repeater, skip_repeated_factors: bool):
    start = 10 ** (repeater.repeat_val_oom - 1)
    end = 10 ** repeater.repeat_val_oom
    repeater_mult = repeater.repeater
    for repeat_val in range(start, end):
        if skip_repeated_factors and is_repeated(repeat_val):
            continue
        rv = repeater_mult * repeat_val
        yield rv

def part_1(input: Input):
    input_sorted = sorted(input)
    for a, b in zip(input_sorted[:-1], input_sorted[1:]):
        assert a[1] < b[0]
    max_value = input_sorted[-1][1]
    repeaters = generate_repeaters(max_value, True)

    unique_invalid_ids = set()

    for repeater in repeaters:
        done_with_repeater = False
        for repeated_value in generate_repeated_values(repeater, False):
            for id_range_idx, (id_range_start, id_range_stop) in enumerate(input_sorted):
                if repeater.max_val < id_range_start:
                    break

                if repeated_value > id_range_stop:
                    if ((id_range_idx+1) < len(input_sorted)) and repeater.max_val < input_sorted[id_range_idx+1][0]:
                        done_with_repeater = True
                        break
                    continue

                if repeated_value >= id_range_start:
                    unique_invalid_ids.add(repeated_value)
            if done_with_repeater:
                break

    return sum(unique_invalid_ids)

def part_2(input: Input):
    input_sorted = sorted(input)
    for a, b in zip(input_sorted[:-1], input_sorted[1:]):
        assert a[1] < b[0]
    max_value = input_sorted[-1][1]
    repeaters = generate_repeaters(max_value, False)

    invalid_id_set = set()

    for repeater in repeaters:
        done_with_repeater = False
        for repeated_value in generate_repeated_values(repeater, False):
            for id_range_idx, (id_range_start, id_range_stop) in enumerate(input_sorted):
                if repeater.max_val < id_range_start:
                    break

                if repeated_value > id_range_stop:
                    if ((id_range_idx+1) < len(input_sorted)) and repeater.max_val < input_sorted[id_range_idx+1][0]:
                        done_with_repeater = True
                        break
                    continue

                if repeated_value >= id_range_start:
                    invalid_id_set.add(repeated_value)
            if done_with_repeater:
                break

    return sum(invalid_id_set)
