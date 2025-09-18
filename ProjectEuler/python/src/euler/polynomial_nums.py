import math

def is_triange_number(value: int) -> bool:
    n = (math.sqrt((8 * value) + 1) - 1) / 2
    return int(n) == n

def is_square_number(value: int) -> bool:
    n = math.sqrt(value)
    return int(n) == n

def is_pentagonal_number(value: int) -> bool:
    n = (math.sqrt((24 * value) + 1) + 1) / 6
    return int(n) == n

def is_hexagonal_number(value: int) -> bool:
    n = (math.sqrt((8 * value) + 1) + 1) / 4
    return int(n) == n
