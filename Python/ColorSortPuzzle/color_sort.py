import dataclasses
from typing import List, Tuple, Optional, Any

@dataclasses.dataclass(frozen=True)
class Action:
    starting_container: int
    ending_container: int
    color: Any
    count: int


starting_configuration = (
    ("g", "r", "r", "b"),
    ("g", "b", "r", "y"),
    ("y", "g", "y", "g"),
    ("b", "r", "y", "b"),
    (),
    (),
)


def top_color_and_depth(container: tuple) -> Optional[Tuple[Any, int]]:
    """
    Returns the top color from the container, along with the number
    of continuous segments that are that color. 
    """
    if len(container) == 0:
        return None

    top_c = None
    for i, color in enumerate(container):
        if top_c is None:
            top_c = color
        elif top_c != color:
            return top_c, i

    return top_c, len(container)


def possible_actions(containers: Tuple[tuple], one_at_a_time=False, max_depth=4) -> List[Action]:
    """
    Returns all posible actions from the specified collection of containers.
    """
    actions = []

    # For each container...
    for sc_index, starting_container in enumerate(containers):
        # If the container is empty, there's no moves that can apply to it
        if len(starting_container) <= 0:
            continue

        # Determine "top color" in container and depth of color in container
        color_to_move, color_depth = top_color_and_depth(starting_container)

        # Check all containers you can pour the container into
        for ec_index, ending_container in enumerate(containers):
            # Can't pour a container into itself
            if ec_index == sc_index:
                continue

            can_move_here = (
                (len(ending_container) < max_depth) and
                (
                    len(ending_container) <= 0 or
                    ending_container[0] == color_to_move
                )
            )

            amount_to_move = (
                1 if one_at_a_time else
                # Partial pours are possible
                min(color_depth, max_depth - len(ending_container))
            )

            if can_move_here:
                actions.append(Action(
                    starting_container=sc_index,
                    ending_container=ec_index,
                    color=color_to_move,
                    count=amount_to_move,
                ))

    return actions


def apply_move(containers: Tuple[tuple], action: Action) -> Tuple[tuple]:
    containers = list(containers)
    
    # Apply change to starting container
    starting_container = containers[action.starting_container]
    new_starting = starting_container[action.count:]
    containers[action.starting_container] = new_starting

    # Apply change to ending container
    ending_container = containers[action.ending_container]
    new_ending = (*(action.color for _ in range(action.count)), *ending_container)
    containers[action.ending_container] = new_ending

    return tuple(containers)


def is_completed(containers: Tuple[tuple]) -> bool:
    pass


class BaseAgent:
    def make_move(self, containers: Tuple[tuple], possible_actions: List[Action]) -> Action:
        raise NotImplementedError()


class RandomAgent(BaseAgent):
    def make_move(self, containers: Tuple[tuple], possible_actions: List[Action]) -> Action:
        import random
        return random.choice(possible_actions)
