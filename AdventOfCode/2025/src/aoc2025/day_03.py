def transform(input: str) -> list[list[int]]:
    return [list(map(int, line.strip())) for line in input.split() if line.strip()]

digits = [9,8,7,6,5,4,3,2,1]

def find_max_joltage_in_bank_2_batteries(bank: list[int]):
    for int_a in digits:
        try:
            int_a_idx = bank.index(int_a, 0, -1)
        except:
            continue
        for int_b in digits:
            try:
                bank.index(int_b, int_a_idx + 1)
                return int((int_a * 10) + int_b)
            except:
                continue

    raise ValueError()


def part_1(input: list[list[str]]):
    sum_ = 0
    for bank in input:
        joltage = find_max_joltage_in_bank_2_batteries(bank)
        sum_ += joltage
    return sum_


def find_max_joltage_in_bank_n_batteries(
    bank: list[int], n_batteries: int, start: int
) -> int:
    if n_batteries == 0:
        return 0

    max_joltage = 0
    max_joltage_idx = -1

    for bank_idx in range(start, len(bank) - (n_batteries-1)):
        current = bank[bank_idx]
        if current > max_joltage:
            max_joltage = current
            max_joltage_idx = bank_idx
            if current == 9:
                break

    return (max_joltage * (10**(n_batteries-1))) + find_max_joltage_in_bank_n_batteries(
        bank, n_batteries-1, max_joltage_idx+1
    )

def part_2(input: list[list[int]]):
    sum_ = 0
    for bank in input:
        largest_joltage = find_max_joltage_in_bank_n_batteries(bank, 12, 0)
        sum_ += largest_joltage
    return sum_
