import color_sort

starting_configuration = (
    "26c3",
    "4832",
    "42a1",
    "9b9c",
    "1455",
    "1395",
    "887c",

    "bb18",
    "a296",
    "674b",
    "637a",
    "7ac5",
    "",
    "",
)

initial_state = color_sort.game.GameState(starting_configuration, 4, True)

state_graph = {}
state_hash_lookup = {}
states_to_check = [initial_state]

while len(states_to_check) > 0:
    current_state = states_to_check.pop(0)
    current_state_hash = hash(current_state)
    if current_state_hash in state_hash_lookup:
        continue
    state_hash_lookup[current_state_hash] = current_state

    edges = []
    state_graph[current_state_hash] = edges
    for action in color_sort.game.possible_actions(current_state):
        new_state = color_sort.game.apply_action(current_state, action)
        new_state_hash = hash(new_state)
        states_to_check.append(new_state)
        edges.append({
            "action": action,
            "state_hash": new_state_hash,
        })

print(len(state_graph))
