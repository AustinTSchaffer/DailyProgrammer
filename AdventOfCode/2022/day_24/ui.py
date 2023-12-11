from sln import *
import itertools

def display(blizzard: Input | list[list[int]], explorer_loc: tuple[int, int] = None, explorer_glyph='E', left_padding=5):
    assert len(explorer_glyph) == 1
    output = []
    for i in range(-1, len(blizzard) + 1):
        output.append(' ' * left_padding)
        for j in range(-1, len(blizzard[0]) + 1):
            if (i, j) == explorer_loc:
                output.append(f'\033[1m{explorer_glyph}\033[0m')
            elif i == -1:
                if j == 0:
                    output.append('.')
                else:
                    output.append('#')
            elif i == len(blizzard):
                if j == len(blizzard[0]) - 1:
                    output.append('.')
                else:
                    output.append('#')
            else:
                if j == -1 or j == len(blizzard[0]):
                    output.append('#')
                else:
                    try:
                        val = blizzard[i][j]
                    except Exception:
                        print(i, j)
                    if val == 0:
                        output.append('.')
                    elif val == BlizzardDir.Up.value:
                        output.append('^')
                    elif val == BlizzardDir.Down.value:
                        output.append('v')
                    elif val == BlizzardDir.Left.value:
                        output.append('<')
                    elif val == BlizzardDir.Right.value:
                        output.append('>')
                    else:
                        output.append(str(val.bit_count()))

        output.append('\n')
    print(''.join(output))

def interactive_demo(input_: Input):
    current_location = input_.start
    moves_made = 0
    location_history = []

    import io, sys, readchar, os

    while True:
        os.system('clear')
        print("=" * (5 + input_.width + 2 + 5))
        print(f"     Moves made: {moves_made}")
        print()
        display(simulate(input_, moves_made), current_location)
        print()

        if current_location == input_.end:
            break

        available_moves = possible_moves(input_, moves_made, current_location)

        while True:
            try:
                origout = sys.stdout
                sys.stdout = io.StringIO
                char = readchar.readkey()
            finally:
                sys.stdout = origout

            if char == readchar.key.BACKSPACE and len(location_history) > 0:
                current_location = location_history.pop(-1)
                moves_made -= 1
                break

            elif char == readchar.key.SPACE and (0, 0) in available_moves:
                location_history.append(current_location)
                current_location = available_moves[(0,0)]
                moves_made += 1
                break

            elif char == readchar.key.UP and (-1, 0) in available_moves:
                location_history.append(current_location)
                current_location = available_moves[(-1, 0)]
                moves_made += 1
                break

            elif char == readchar.key.DOWN and (1, 0) in available_moves:
                location_history.append(current_location)
                current_location = available_moves[(1, 0)]
                moves_made += 1
                break

            elif char == readchar.key.LEFT and (0, -1) in available_moves:
                location_history.append(current_location)
                current_location = available_moves[(0, -1)]
                moves_made += 1
                break
        
            elif char == readchar.key.RIGHT and (0, 1) in available_moves:
                location_history.append(current_location)
                current_location = available_moves[(0, 1)]
                moves_made += 1
                break

    print()
    print("=======================")
    print("       You Win!        ")
    print(f"   Moves made: {moves_made}")
    print("=======================")

def part_2_visually(input: Input):
    import time
    def neighbors(t_n: tuple[int, tuple[int, int]]):
        t, node = t_n
        for neighbor in possible_moves(input, t, node).values():
            yield (t+1, neighbor)

    def manhattan(n1, n2):
        return (
            abs(n1[1][1] - n2[1][1]) +
            abs(n1[1][0] - n2[1][0])
        )

    def is_goal_reached(node_a, node_b):
        # We don't care about t when checking to see
        # if we're at the goal.
        return node_a[1] == node_b[1]

    total_t = 0
    display(simulate(input, total_t), input.start, explorer_glyph='O')
    for start, end in itertools.cycle(((input.start, input.end), (input.end, input.start))):
        path = astar.find_path(
            (total_t, start),
            (-1, end),
            neighbors_fnct=neighbors,
            heuristic_cost_estimate_fnct=manhattan,
            is_goal_reached_fnct=is_goal_reached,
        )

        path = list(path)

        prev_node = start
        for _, node in path[1:]:
            move_decision = (node[0] - prev_node[0], node[1] - prev_node[1])
            prev_node = node
            match move_decision:
                case (0, 0):
                    move_decision = "Wait"
                case (-1, 0):
                    move_decision = "Up"
                case (1, 0):
                    move_decision = "Down"
                case (0, -1):
                    move_decision = "Left"
                case (0, 1):
                    move_decision = "Right"
                case _:
                    move_decision = "?????"

            print(f"     Iteration: {total_t:>5}. Last Move: {move_decision:<5} ")
            display(simulate(input, total_t), node, explorer_glyph='O')

            total_t += 1
            time.sleep(0.1)

if __name__ == '__main__':
    input_ = parse_input('input.txt')
    input_denoised = parse_input('input_denoised.txt')
    sample_input_1 = parse_input('sample_input_1.txt')
    sample_input_2 = parse_input('sample_input_2.txt')

    part_2_visually(input_)
