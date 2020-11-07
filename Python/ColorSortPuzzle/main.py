import color_sort

starting_configuration = (
    ("g", "r", "r", "b"),
    ("g", "b", "r", "y"),
    ("y", "g", "y", "g"),
    ("b", "r", "y", "b"),
    (),
    (),
)

state = color_sort.game.GameState(starting_configuration, 4, False)
moves = color_sort.breadth_first_search_solver.solve(state)

for move in moves:
    print(move)
