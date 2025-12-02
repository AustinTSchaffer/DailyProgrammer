def part_1(input: str) -> int:
    zeroes = 0
    dial_position = 50
    for line in input.split():
        if line:
            direction = -1 if line[0] == 'L' else +1
            distance = int(line[1:])
            dial_position = (dial_position + (direction * distance)) % 100
            if dial_position == 0:
                zeroes += 1
    return zeroes

def part_2(input: str) -> int:
    zeroes = 0
    dial_position = 50
    for line in input.split():
        if line:
            direction = -1 if line[0] == 'L' else +1
            distance = int(line[1:])
            for _ in range(distance):
                dial_position = (dial_position + direction) % 100
                if dial_position == 0:
                    zeroes += 1
    return zeroes
    