import random
from typing import List, Tuple

import color_sort.game as game


class BaseAgent:
    """
    Base class for agent implementations.
    """

    def make_move(self, state: game.GameState, possible_actions: List[game.Action]) -> game.Action:
        raise NotImplementedError()

class RandomAgent(BaseAgent):
    def make_move(self, containers: Tuple[tuple], possible_actions: List[game.Action]) -> game.Action:
        return random.choice(possible_actions)
