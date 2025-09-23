import collections

HIGH_CARD = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OAK = 3
STRAIGHT = 4
FLUSH = 5
FULL_HOUSE = 6
FOUR_OAK = 7
STRAIGHT_FLUSH = 8
ROYAL_FLUSH = 9


def determine_result(poker_hand: list[tuple[int, str]]) -> tuple[int, ...]:
    poker_hand = sorted(poker_hand)

    values = tuple([card[0] for card in poker_hand])
    unique_suits = {card[1] for card in poker_hand}

    is_straight = (
        values[0] + 1 == values[1] and
        values[1] + 1 == values[2] and
        values[2] + 1 == values[3] and
        values[3] + 1 == values[4]
    )
    is_flush = len(unique_suits) == 1
    high_card = max(values)

    if values == (14, 2, 3, 4, 5):
        # Special case
        is_straight = True
        high_card = 5

    if is_straight and is_flush:
        if high_card == 14:
            return (ROYAL_FLUSH, high_card)
        return (STRAIGHT_FLUSH, high_card)

    groups = [
        (count, value)
        for value, count in
        sorted(collections.Counter(values).items(), key=lambda t: (t[1], t[0]))
    ]

    if groups[-1][0] == 4:
        return (FOUR_OAK, groups[-1][1])

    if groups[-1][0] == 3 and groups[-2][0] == 2:
        return (FULL_HOUSE, groups[-1][1], groups[-2][1])

    if is_flush:
        return (FLUSH, high_card)

    if is_straight:
        return (STRAIGHT, high_card)

    if groups[-1][0] == 3:
        return (THREE_OAK, groups[-1][1])

    if groups[-1][0] == 2:
        if groups[-2][0] == 2:
            return (TWO_PAIR, groups[-1][1], groups[-2][1])
        
        return (ONE_PAIR, groups[-1][1])

    return (HIGH_CARD, high_card)
