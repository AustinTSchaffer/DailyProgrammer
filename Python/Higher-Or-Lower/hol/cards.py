import enum


class Rank(enum.Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14


class Suit(enum.Enum):
    Clubs = 1
    Diamonds = 2
    Hearts = 3
    Spades = 4


class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
    
    def __lt__(self, card):
        return self.rank.value < card.rank.value

    def __le__(self, card):
        return self.rank.value <= card.rank.value

    def __gt__(self, card):
        return self.rank.value > card.rank.value

    def __ge__(self, card):
        return self.rank.value >= card.rank.value

    def __hash__(self) -> int:
        return (
            self.rank.value +
            (Rank.Ace.value * self.suit.value)
        )

    def __eq__(self, card) -> bool:
        return (
            self.rank == card.rank and
            self.suit == card.suit
        )
