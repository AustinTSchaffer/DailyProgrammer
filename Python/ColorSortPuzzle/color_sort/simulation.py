from typing import List

import color_sort.game as game


class BaseAgent:
    """
    Base class for agent implementations.
    """

    def make_move(self, state: game.GameState, possible_actions: List[game.Action]) -> game.Action:
        raise NotImplementedError()
