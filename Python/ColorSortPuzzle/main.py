import color_sort

starting_configuration = (
    "cc21",
    "4b59",
    "63a7",
    "98a8",
    "6664",
    "2a93",
    "48c1",

    "bc82",
    "14a5",
    "7177",
    "b253",
    "b359",
    "",
    "",
)

state = color_sort.game.GameState(starting_configuration, 4, True)
actions, solvable = color_sort.breadth_first_search_solver.solve(state)

assert solvable
for action in actions:
    print(f"Move {action.color} from {action.starting_container + 1} to {action.ending_container + 1}")
