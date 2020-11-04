import random
from typing import List, Tuple

import color_sort.game as game
import color_sort.simulation as simulation


class RandomAgent(simulation.BaseAgent):
    def make_move(self, containers: Tuple[tuple], possible_actions: List[game.Action]) -> game.Action:
        return random.choice(possible_actions)
