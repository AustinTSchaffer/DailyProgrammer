import dataclasses
from typing import List, Tuple

import color_sort.game as game

def solve(state: game.GameState) -> List[game.Action]:
    """
    Solves the game using a BFS algorithm with no optimizations. Warning, will use multiple GBs of RAM.
    """
    seed_states = [(state, [])]

    while len(seed_states) > 0:
        state, actions_so_far = seed_states.pop(0)

        if game.game_won(state):
            return actions_so_far

        possible_actions = game.possible_actions(state)
        if len(possible_actions) <= 0:
            continue

        for action in possible_actions:
            new_seed = (
                game.apply_action(state, action),
                [*actions_so_far, action]
            )

            seed_states.append(new_seed)

    raise ValueError(f"Game cannot be won: {state}")
