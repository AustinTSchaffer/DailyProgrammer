import color_sort

starting_configuration = (
    ("1", "7", "3", "b"),
    ("6", "9", "5", "a"),
    ("5", "4", "9", "4"),
    ("7", "5", "3", "6"),
    ("3", "a", "b", "7"),
    ("a", "7", "6", "8"),
    ("b", "2", "8", "3"),

    ("8", "9", "2", "4"),
    ("2", "9", "1", "6"),
    ("1", "2", "a", "b"),
    ("1", "8", "5", "4"),
    (),
    (),
)

state = color_sort.game.GameState(starting_configuration, 4, False)
actions, solvable = color_sort.breadth_first_search_solver.solve(state)

assert solvable
for action in actions:
    print(f"Move {action.color} from {action.starting_container + 1} to {action.ending_container + 1}")
