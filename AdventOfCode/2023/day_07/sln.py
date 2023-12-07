import re
import dataclasses
import enum
import collections

CARD_VALUES = "AKQJT98765432"
CARD_VALUES_JOKER = "AKQT98765432J"

class HandType(enum.Enum):
    FiveOfAKind = 0
    FourOfAKind = 1
    FullHouse = 2
    ThreeOfAKind = 3
    TwoPair = 4
    OnePair = 5
    HighCard = 6

@dataclasses.dataclass
class HandBid:
    hand: str
    bid: int

    def get_hand_type(self, jokers=False) -> HandType:
        counter = collections.Counter(self.hand)
        hand_type: int
        match sorted(counter.values(), reverse=True):
            case [5]:
                hand_type = HandType.FiveOfAKind
            case [4, _]:
                hand_type = HandType.FourOfAKind
            case [3, 2]:
                hand_type = HandType.FullHouse
            case [3, _, _]:
                hand_type = HandType.ThreeOfAKind
            case [2, 2, _]:
                hand_type = HandType.TwoPair
            case [2, _, _, _]:
                hand_type = HandType.OnePair
            case _:
                hand_type = HandType.HighCard

        if not jokers:
            return hand_type

        num_jokers = self.hand.count('J')

        match (hand_type, num_jokers):
            case (_, 0):
                return hand_type

            case (HandType.FourOfAKind, 4) | (HandType.FourOfAKind, 1):
                return HandType.FiveOfAKind

            case (HandType.FullHouse, 3) | (HandType.FullHouse, 2):
                return HandType.FiveOfAKind

            case (HandType.ThreeOfAKind, 3) | (HandType.ThreeOfAKind, 1):
                return HandType.FourOfAKind

            case (HandType.TwoPair, 2):
                return HandType.FourOfAKind
            case (HandType.TwoPair, 1):
                return HandType.FullHouse

            case (HandType.OnePair, 2):
                return HandType.ThreeOfAKind
            case (HandType.OnePair, 1):
                return HandType.ThreeOfAKind

            case (HandType.HighCard, 1):
                return HandType.OnePair

            case _:
                return hand_type


    def get_score(self, jokers=False, card_strengths=CARD_VALUES):
        return (self.get_hand_type(jokers).value, *map(card_strengths.index, self.hand))


@dataclasses.dataclass
class Input:
    hands: list[HandBid]

def parse_input(filename: str) -> Input:
    with open(filename, 'r') as f:
        return Input(
            hands=[
                HandBid(hand_bid[0], int(hand_bid[1]))
                for line in f
                if len(hand_bid := line.strip().split(" ")) == 2
            ]
        )

def part_1(input: Input):
    ordered_hands = sorted(input.hands, key=HandBid.get_score, reverse=True)
    return sum((i+1) * h.bid for i,h in enumerate(ordered_hands))

def part_2(input: Input):
    ordered_hands = sorted(input.hands, key=lambda h: HandBid.get_score(h, True, CARD_VALUES_JOKER), reverse=True)
    return sum((i+1) * h.bid for i,h in enumerate(ordered_hands))

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))
