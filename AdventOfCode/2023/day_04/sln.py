import re
import dataclasses

@dataclasses.dataclass
class ScratcherCard:
    card_number: int
    winning_numbers: list[bool]
    actual_numbers: list[int]

ticket_re = re.compile(r'Card\s{1,3}(?P<card_number>\d{1,3}):\s{1,2}(?P<winning_numbers>(\d{1,2}\s+)+)\|\s{1,2}(?P<actual_numbers>(\d{1,2}\s*)+)')

def parse_input(filename: str) -> list[ScratcherCard]:
    output = []
    with open(filename, 'r') as f:
        for line in f:
            winning_numbers = [0] * 100
            actual_numbers = []

            match_ = ticket_re.match(line)
            if not match_:
                print('warning', line)
                continue

            for wn in re.finditer(r'\d+', match_['winning_numbers']):
                winning_numbers[int(wn[0])] = 1
            for an in re.finditer(r'\d+', match_['actual_numbers']):
                actual_numbers.append(int(an[0]))
            output.append(ScratcherCard(
                card_number=int(match_['card_number']),
                winning_numbers=winning_numbers,
                actual_numbers=actual_numbers,
            ))

    return output

def part_1(cards: list[ScratcherCard]):
    total_points = 0
    for card in cards:
        value = 0
        for number in card.actual_numbers:
            if card.winning_numbers[number]:
                if value == 0:
                    value = 1
                else:
                    value <<= 1
        total_points += value
    return total_points

def part_2(cards: list[ScratcherCard]):
    cards_generated = [0] * len(cards)
    for i, card in enumerate(reversed(cards)):
        card_location = len(cards) - 1 - i

        cards_generated[card_location] += 1

        num_winning_nums = 0
        for num in card.actual_numbers:
            if card.winning_numbers[num]:
                num_winning_nums += 1

        for other_card in cards_generated[card_location+1:card_location+1+num_winning_nums]:
            cards_generated[card_location] += other_card

    return sum(cards_generated)

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print("Part 1 (sample):", part_1(sample_input))
    print("Part 1:", part_1(input))

    print("Part 2 (sample):", part_2(sample_input))
    print("Part 2:", part_2(input))
