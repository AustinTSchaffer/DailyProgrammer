import os

CURRENT_DIR, _ = os.path.split(__file__)
DATA_FLIE = os.path.join(CURRENT_DIR, 'data.txt')

def data_file_iter(data_file):
    with open(data_file, 'r') as data:
        for freq_change in data:
            freq_change = freq_change.strip()
            if (freq_change):
                yield int(freq_change)

def part1():
    total = 0
    for freq_change in data_file_iter(DATA_FLIE):
        total += freq_change
    print("Part 1 Total:", total)
    return total


def part2():
    previous_frequencies = set()
    current_frequency = 0
    while True:
        for freq_change in data_file_iter(DATA_FLIE):
            current_frequency += freq_change
            if current_frequency in previous_frequencies:
                print("Part 2 Repeated Frequency:", current_frequency)
                return current_frequency
            previous_frequencies.add(current_frequency)

if __name__ == '__main__':
    part1()
    part2()
