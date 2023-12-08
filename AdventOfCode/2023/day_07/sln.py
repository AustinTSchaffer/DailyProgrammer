import re
import dataclasses
import enum
import collections

CARD_VALUES = "23456789TJQKA"
CARD_VALUES_JOKER = "J23456789TQKA"

class HandType(enum.Enum):
    FiveOfAKind = 6
    FourOfAKind = 5
    FullHouse = 4
    ThreeOfAKind = 3
    TwoPair = 2
    OnePair = 1
    HighCard = 0

@dataclasses.dataclass
class HandBid:
    hand: str
    bid: int

    def get_hand_type(self, jokers=False) -> HandType:
        """
        Returns the type of the hand based on the 5 cards it contains
        (see HandType). If `jokers` is set True, this method will attempt
        to upgrade the hand type based on the number of jokers it contains.
        """

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


    def get_hand_type_rachel_edition(self, jokers=False) -> HandType:
        """
        Returns the type of the hand based on the 5 cards it contains
        (see HandType). If `jokers` is set True, this method will attempt
        to upgrade the hand type based on the number of jokers it contains.

        This is a variant of `get_hand_type` using Rachel's algorithm,
        which is just better.
        """

        hand = self.hand if not jokers else self.hand.replace('J', '')
        counter = collections.Counter(hand)
        card_counts = sorted(counter.values(), reverse=True)
        if jokers:
            if len(card_counts) > 0:
                card_counts[0] += self.hand.count('J')
            else:
                card_counts.append(self.hand.count('J'))


        match card_counts:
            case [5]:
                return HandType.FiveOfAKind
            case [4, _]:
                return HandType.FourOfAKind
            case [3, 2]:
                return HandType.FullHouse
            case [3, *_]:
                return HandType.ThreeOfAKind
            case [2, 2, _]:
                return HandType.TwoPair
            case [2, *_]:
                return HandType.OnePair
            case _:
                return HandType.HighCard


    def get_score(self, jokers=False, card_strengths=CARD_VALUES, alg=get_hand_type) -> tuple[int, int, int, int, int, int]:
        """
        Returns a tuple of 6 integers. The first indicates the value of the hand
        based on its type, the next 5 indicate the value of each card in the hand.
        Useful as a sort key

        Higher is better.
        """

        return (alg(self, jokers).value, *map(card_strengths.index, self.hand))


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

def part_1(input: Input, alg=HandBid.get_hand_type):
    ordered_hands = sorted(input.hands, key=lambda h: HandBid.get_score(h, alg=alg))
    return sum((i+1) * h.bid for i,h in enumerate(ordered_hands))

def part_2(input: Input, alg=HandBid.get_hand_type):
    ordered_hands = sorted(input.hands, key=lambda h: HandBid.get_score(h, True, CARD_VALUES_JOKER, alg))
    return sum((i+1) * h.bid for i,h in enumerate(ordered_hands))

if __name__ == '__main__':
    input = parse_input('input.txt')
    sample_input = parse_input('sample_input.txt')

    print('Part 1 (sample):', part_1(sample_input))
    print('Part 1:', part_1(input))

    print('Part 2 (sample):', part_2(sample_input))
    print('Part 2:', part_2(input))

    print('Part 2 (sample, Rachel):', part_2(sample_input, HandBid.get_hand_type_rachel_edition))
    print('Part 2 (Rachel):', part_2(input, HandBid.get_hand_type_rachel_edition))
