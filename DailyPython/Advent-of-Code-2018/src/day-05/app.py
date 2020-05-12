import os
import re
import string


POLYMER_DATA_FILE = os.path.join(
    os.path.dirname(__file__), 
    'polymer.txt'
)

def load_polymer(file):
    with open(POLYMER_DATA_FILE, 'r') as polymer_file:
        return polymer_file.read().strip()

def reduce_polymer(polymer):
    new_polymer = ''
    for right_term in polymer:
        if not new_polymer:
            new_polymer += right_term
            continue

        left_term = new_polymer[-1] if new_polymer else ''

        if left_term != right_term and left_term.lower() == right_term.lower():
            new_polymer = new_polymer[:-1]
            continue

        new_polymer += right_term
    return new_polymer

def part1(polymer):
    new_polymer = reduce_polymer(polymer)
    print('Size of polymer after all reactions:', len(new_polymer))

    return new_polymer

def part2(polymer):
    reduced_polymers = sorted(
        [
            (
                unit,
                reduce_polymer(re.sub(unit, '', polymer, flags=re.I))
            )
            for unit in string.ascii_lowercase
        ],
        key=lambda p: len(p[1])
    )

    print('Length of Shortest:', len(reduced_polymers[0][1]))

if __name__ == "__main__":
    polymer = load_polymer(POLYMER_DATA_FILE)
    reduced_polymer = part1(polymer)
    part2(reduced_polymer)
