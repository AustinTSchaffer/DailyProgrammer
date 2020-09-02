import itertools
import enum
from typing import Iterable, List
import decimal

import more_itertools

from hol import cards, constants


def generate_all_games(number_of_cards: int) -> Iterable[List[cards.Card]]:
    """
    Generator for all possible permutations of N cards out of a 52-card deck.
    """

    for combination in itertools.combinations(constants.ALL_CARDS, number_of_cards):
        for permutation in itertools.permutations(combination):
            yield list(permutation)


def should_pick_higher(card: cards.Card, cards_drawn: List[cards.Card]) -> bool:
    """
    Given the current card and a list of cards that have already been drawn from
    the deck, returns True if it is more likely that the next card drawn will be
    higher than the current card. If false, the player should pick lower.
    """

    remaining_cards = constants.ALL_CARDS - set(cards_drawn)
    num_cards_higher = 0
    num_cards_lower = 0

    for remaining_card in remaining_cards:
        if remaining_card > card:
            num_cards_higher += 1
        elif remaining_card < card:
            num_cards_lower += 1

    return num_cards_higher >= num_cards_lower


def is_a_winning_game(game: List[cards.Card]):
    """
    Returns true if the input list of cards describes a game that a rational
    player would win, assuming that the rational player always picks cards
    according to the result of the `should_pick_higher` function.
    """

    cards_drawn = []
    for current, next_ in more_itertools.pairwise(game):
        cards_drawn.append(current)

        if should_pick_higher(current, cards_drawn):
            if current >= next_:
                # A rational player would pick higher but the next card will
                # actually be lower, resulting in a loss.
                return False
        else:
            if current <= next_:
                # A rational player would pick lower but the next card will
                # actually be higher, resulting in a loss.
                return False

    return True


def generate_win_statistics(number_of_cards: int) -> dict:
    """
    Generates win-loss statistics across all games.
    """

    stats = {
        "number_of_cards": number_of_cards,
        "total_games": 0,
        "games_won": 0,
        "games_lost": 0,
        "starting_card_stats": {
            rank: {
                "total_games": 0,
                "games_won": 0,
                "games_lost": 0,
            }
            for rank in cards.Rank
        },
    }

    for game in generate_all_games(number_of_cards):
        stats["total_games"] += 1

        starting_card = game[0]
        starting_card_stats_record = stats["starting_card_stats"][starting_card.rank]

        starting_card_stats_record["total_games"] += 1

        if is_a_winning_game(game):
            stats["games_won"] += 1
            starting_card_stats_record["games_won"] += 1

        else:
            stats["games_lost"] += 1
            starting_card_stats_record["games_lost"] += 1

    return stats
