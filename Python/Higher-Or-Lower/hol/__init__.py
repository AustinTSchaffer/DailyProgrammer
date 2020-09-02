r"""

Contains classes and methods that can be used when simulating the game
Higher-or-Lower and performing statistical analysis on different games.

"""

from hol import (
    cards,
    constants,
)

from hol._hol import (
    generate_all_games,
    should_pick_higher,
    is_a_winning_game,
    generate_win_statistics,
)
