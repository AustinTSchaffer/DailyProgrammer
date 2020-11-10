import color_sort

starting_configuration = (
    "b263",
    "7a51",
    "84ac",
    "a451",
    "3699",
    "cb72",
    "8c6c",

    "73a7",
    "5938",
    "5618",
    "bb22",
    "1449",
    "",
    "",
)

state = color_sort.game.GameState(starting_configuration, 4, False)
actions, solvable = color_sort.breadth_first_search_solver.solve(state)

assert solvable
for action in actions:
    print(f"Move {action.color} from {action.starting_container + 1} to {action.ending_container + 1}")
