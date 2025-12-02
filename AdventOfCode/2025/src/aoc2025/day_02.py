import common

Input = list[tuple[int, int]]

def transform(input: str) -> Input:
    return sorted([
        tuple(map(int, part.split('-')))
        for part in input.split(',')
    ])

def part_1(input: Input):
    invalid_id_sum = 0
    for range_ in input:
        for id in range(range_[0], range_[1]+1):
            id_str = str(id)
            if len(id_str) % 2 != 0:
                continue
            if id_str[:len(id_str) // 2] == id_str[len(id_str) // 2:]:
                invalid_id_sum += id
    return invalid_id_sum

def part_2(input: Input):
    invalid_id_sum = 0
    for range_ in input:
        for id in range(range_[0], range_[1]+1):
            if id < 10:
                continue
            id_str = str(id)
            for factor in common.factors(len(id_str), proper=True):
                component = id_str[:factor]
                repetitions = (len(id_str) // factor)
                if (component * repetitions) == id_str:
                    invalid_id_sum += id
                    break
    return invalid_id_sum
