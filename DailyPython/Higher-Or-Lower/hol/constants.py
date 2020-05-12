from hol import cards


ALL_CARDS = {
    cards.Card(rank, suit)
    for rank in cards.Rank
    for suit in cards.Suit
}
