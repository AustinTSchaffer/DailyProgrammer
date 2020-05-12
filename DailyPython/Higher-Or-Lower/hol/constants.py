from hol import enums

ALL_CARDS = [
    (card, suit)
    for card in enums.Card
    for suit in enums.Suit
]
