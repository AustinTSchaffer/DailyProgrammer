import dataclasses
from typing import Any, Optional, Tuple, List

@dataclasses.dataclass(frozen=True)
class Action:
    """
    Models actions that can be taken against the game.
    """
    starting_container: int
    ending_container: int
    color: Any
    count: int


@dataclasses.dataclass(frozen=True)
class GameState:
    """
    Models the current state of the game.
    """
    containers: Tuple[tuple]
    container_size: int
    one_at_a_time: bool

    @classmethod
    def copy(cls, self,
             containers=None,
             container_size=None,
             one_at_a_time=None,
             ):
        """
        Duplicates self, overriding any class properties.
        """
        return cls(
            containers=containers if containers is not None else self.containers,
            container_size=container_size if container_size is not None else self.container_size,
            one_at_a_time=one_at_a_time if one_at_a_time is not None else self.one_at_a_time,
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


def possible_actions(state: GameState) -> List[Action]:
    """
    Returns all posible actions from the specified collection of containers.
    """
    actions = []

    # For each container...
    for sc_index, starting_container in enumerate(state.containers):
        # If the container is empty, there's no moves that can apply to it
        if len(starting_container) <= 0:
            continue

        # Determine "top color" in container and depth of color in container
        color_to_move, color_depth = top_color_and_depth(starting_container)

        # Check all containers you can pour the container into
        for ec_index, ending_container in enumerate(state.containers):
            # Can't pour a container into itself
            if ec_index == sc_index:
                continue

            can_move_here = (
                (len(ending_container) < state.container_size) and
                (
                    len(ending_container) <= 0 or
                    ending_container[0] == color_to_move
                )
            )

            amount_to_move = (
                1 if state.one_at_a_time else
                # Partial pours are possible
                min(color_depth, state.container_size - len(ending_container))
            )

            if can_move_here:
                actions.append(Action(
                    starting_container=sc_index,
                    ending_container=ec_index,
                    color=color_to_move,
                    count=amount_to_move,
                ))

    return actions


def apply_action(state: GameState, action: Action) -> GameState:
    """
    Applies an action to the state, returning a new GameState instance with the results of that action.
    """

    containers = list(state.containers)
    
    # Apply change to starting container
    starting_container = containers[action.starting_container]
    new_starting = starting_container[action.count:]
    containers[action.starting_container] = new_starting

    # Apply change to ending container
    ending_container = containers[action.ending_container]
    new_ending = (*(action.color for _ in range(action.count)), *ending_container)
    containers[action.ending_container] = new_ending

    return GameState.copy(
        state,
        containers=tuple(containers),
    )


def game_won(containers: Tuple[tuple]) -> bool:
    """
    Returns true if the game can be considered "won" and the player may advance to the next level.
    """
    raise NotImplementedError()


def game_lost(state: GameState) -> bool:
    """
    Returns true if the game reaches a state with no possible actions, or if all possible actions create a cycle.
    """
    if not any(possible_actions(state)):
        return True

    raise NotImplementedError()
