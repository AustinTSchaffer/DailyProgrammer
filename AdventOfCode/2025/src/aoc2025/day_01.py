def main():
    sample_input = open('data/day_01.sample.txt').read()
    real_input = open('data/day_01.txt').read()

    print("Day 01")
    print("\tPart 1 (sample):", part_1(sample_input))
    print("\tPart 1:", part_1(real_input))
    print("\tPart 2 (sample):", part_2(sample_input))
    print("\tPart 2:", part_2(real_input))

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
