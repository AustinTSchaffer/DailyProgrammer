import dataclasses
from typing import List, Tuple

import color_sort.game as game

def solve(state: game.GameState) -> List[game.Action]:
    """
    Solves the game using a BFS algorithm with no optimizations. Warning, will use multiple GBs of RAM.
    """

    seed_states = [(state, [])]
    states_visited = {state}

    while len(seed_states) > 0:
        current_state, actions_so_far = seed_states.pop(0)

        if game.game_won(current_state):
            return actions_so_far

        possible_actions = game.possible_actions(current_state)
        if len(possible_actions) <= 0:
            continue

        for action in possible_actions:
            new_state = game.apply_action(current_state, action)
            if new_state in states_visited:
                continue

            states_visited.add(new_state)

            new_seed = (
                new_state,
                [*actions_so_far, action],
            )

            seed_states.append(new_seed)

    raise ValueError(f"Game cannot be won: {state}")
