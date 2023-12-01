import dataclasses
from typing import Optional, Literal

@dataclasses.dataclass
class AdjacentCoordinate:
    coordinate: tuple[int, int]
    new_heading: Literal['R', 'D', 'L', 'U', None]

@dataclasses.dataclass
class Node:
    location: tuple[int, int]
    up: Optional[AdjacentCoordinate]
    down: Optional[AdjacentCoordinate]
    left: Optional[AdjacentCoordinate]
    right: Optional[AdjacentCoordinate]

@dataclasses.dataclass
class Instruction:
    distance: Optional[int]
    turn: Optional[Literal['L', 'R']]

def index_out_of_bounds(_map: list[str], row_idx: int, col_idx: int) -> bool:
    if row_idx < 0 or col_idx < 0:
        return True
    if row_idx >= len(_map):
        return True
    if col_idx >= len(_map[row_idx]):
        return True
    if _map[row_idx][col_idx] == ' ':
        return True

    return False


def get_adjacent_coordinates_flat(_map: list[str], row_idx: int, col_idx: int, context: dict) -> list[Optional[AdjacentCoordinate]]:
    """
    Returns a list of coordinates in "up, down left, right" order, wrapping around
    as necessary. A coordinate is None if there's a wall in that direction.
    """

    output = []

    # up
    new_row_idx = row_idx - 1
    if index_out_of_bounds(_map, new_row_idx, col_idx):
        # come back in the bottom
        for new_row_idx in range(len(_map), row_idx, -1):
            if not index_out_of_bounds(_map, new_row_idx, col_idx):
                break
    output.append(AdjacentCoordinate((new_row_idx, col_idx), None) if _map[new_row_idx][col_idx] != '#' else None)

    # down
    new_row_idx = row_idx + 1
    if index_out_of_bounds(_map, new_row_idx, col_idx):
        # come back in the top
        for new_row_idx in range(0, row_idx):
            if not index_out_of_bounds(_map, new_row_idx, col_idx):
                break
    output.append(AdjacentCoordinate((new_row_idx, col_idx), None) if _map[new_row_idx][col_idx] != '#' else None)

    # left
    new_col_idx = col_idx - 1
    if index_out_of_bounds(_map, row_idx, new_col_idx):
        # come back in the right
        for new_col_idx in range(len(_map[row_idx]), col_idx, -1):
            if not index_out_of_bounds(_map, row_idx, new_col_idx):
                break
    output.append(AdjacentCoordinate((row_idx, new_col_idx), None) if _map[row_idx][new_col_idx] != '#' else None)

    # right
    new_col_idx = col_idx + 1
    if index_out_of_bounds(_map, row_idx, new_col_idx):
        # come back in the left
        for new_col_idx in range(0, col_idx):
            if not index_out_of_bounds(_map, row_idx, new_col_idx):
                break
    output.append(AdjacentCoordinate((row_idx, new_col_idx), None) if _map[row_idx][new_col_idx] != '#' else None)

    return output


def oob_remapping_specific_input() -> dict[tuple[int, int, Literal['U', 'D', 'L', 'R']], tuple[int, int, Literal['U', 'D', 'L', 'R']]]:
    oob_remapping = {}

    #    [1][2]
    #    [3]
    # [4][5]
    # [6]

    # box 1 top <-> box 6 left
    for i, col_idx in enumerate(range(50, 100)):
        oob_remapping[(0, col_idx, 'U')] = (150 + i, 0, 'R')
        oob_remapping[(150 + i, 0, 'L')] = (0, col_idx, 'D')

    # box 1 left <-> box 4 left
    for i, row_idx in enumerate(range(0, 50)):
        oob_remapping[(row_idx, 50, 'L')] = (149 - i, 0, 'R')
        oob_remapping[(149 - i, 0, 'L')] = (row_idx, 50, 'R')

    # box 3 left <-> box 4 top
    for i, row_idx in enumerate(range(50, 100)):
        oob_remapping[(row_idx, 50, 'L')] = (100, i, 'D')
        oob_remapping[(100, i, 'U')] = (row_idx, 50, 'R')

    # box 2 top <-> box 6 bottom
    for i, col_idx in enumerate(range(100, 150)):
        oob_remapping[(0, col_idx, 'U')] = (199, col_idx - 100, 'U')
        oob_remapping[(199, col_idx - 100, 'D')] = (0, col_idx, 'D')

    # box 5 bottom <-> box 6 right
    for i, col_idx in enumerate(range(50, 100)):
        oob_remapping[(149, col_idx, 'D')] = (150 + i, 49, 'L')
        oob_remapping[(150 + i, 49, 'R')] = (149, col_idx, 'U')

    # box 2 bottom <-> box 3 right
    for i, col_idx in enumerate(range(100, 150)):
        oob_remapping[(49, col_idx, 'D')] = (50 + i, 99, 'L')
        oob_remapping[(50 + i, 99, 'R')] = (49, col_idx, 'U')

    # box 2 right <-> box 5 right
    for i, row_idx in enumerate(range(0, 50)):
        oob_remapping[(row_idx, 149, 'R')] = (149-i, 99, 'L')
        oob_remapping[(149-i, 99, 'R')] = (row_idx, 149, 'L')

    return oob_remapping


def get_adjacent_coordinates_cube(_map: list[str], row_idx: int, col_idx: int, context: dict) -> list[Optional[AdjacentCoordinate]]:
    """
    Returns a list of coordinates in "up, down left, right" order, wrapping around
    as necessary. The final term of the tuple in the list indicates if you need a new heading
    if you travel in that direction. A coordinate is None if there's a wall in that direction.
    """

    output = []

    if not context.get('populated', False):
        face_size = 4 if len(_map) <= 16 else 50
        context['face_size'] = face_size

        oob_remapping = oob_remapping_specific_input()
        context['oob_remapping'] = oob_remapping

        context['populated'] = True
    else:
        face_size = context['face_size']
        oob_remapping = context['oob_remapping']


    if face_size != 50:
        raise ValueError("This was only programmed to work with the actual input.")

    # up
    new_row_idx = row_idx - 1
    new_col_idx = col_idx
    new_heading = None
    if (remapping := oob_remapping.get((row_idx, col_idx, 'U'))) is not None:
        new_row_idx, new_col_idx, new_heading = remapping
    output.append(AdjacentCoordinate((new_row_idx, new_col_idx), new_heading) if _map[new_row_idx][new_col_idx] != '#' else None)

    # down
    new_row_idx = row_idx + 1
    new_col_idx = col_idx
    new_heading = None
    if (remapping := oob_remapping.get((row_idx, col_idx, 'D'))) is not None:
        new_row_idx, new_col_idx, new_heading = remapping
    output.append(AdjacentCoordinate((new_row_idx, new_col_idx), new_heading) if _map[new_row_idx][new_col_idx] != '#' else None)

    # left
    new_row_idx = row_idx
    new_col_idx = col_idx - 1
    new_heading = None
    if (remapping := oob_remapping.get((row_idx, col_idx, 'L'))) is not None:
        new_row_idx, new_col_idx, new_heading = remapping
    output.append(AdjacentCoordinate((new_row_idx, new_col_idx), new_heading) if _map[new_row_idx][new_col_idx] != '#' else None)

    # right
    new_row_idx = row_idx
    new_col_idx = col_idx + 1
    new_heading = None
    if (remapping := oob_remapping.get((row_idx, col_idx, 'R'))) is not None:
        new_row_idx, new_col_idx, new_heading = remapping
    output.append(AdjacentCoordinate((new_row_idx, new_col_idx), new_heading) if _map[new_row_idx][new_col_idx] != '#' else None)

    return output


def parse_instructions(instructions: str) -> list[Instruction]:
    output_instructions: list[Instruction] = []

    current_move_instruction = None
    for char in instructions.strip():
        if str.isdigit(char):
            if current_move_instruction is None:
                current_move_instruction = char
            else:
                current_move_instruction = current_move_instruction + char
        else:
            if current_move_instruction is not None:
                output_instructions.append(Instruction(int(current_move_instruction), None))
                current_move_instruction = None
            output_instructions.append(Instruction(None, char))
    if current_move_instruction is not None:
        output_instructions.append(Instruction(int(current_move_instruction), None))

    return output_instructions


def parse_input(filename: str, get_adjacent_coordinates=get_adjacent_coordinates_flat) -> (Node, dict[tuple[int, int], Node], list[Instruction]):
    with open(filename, 'r') as f:
        data = f.read()

    _map, _instructions = data.split('\n\n')
    _map = [row.strip('\n') for row in _map.split('\n')]

    get_adj_coords_context = {}

    starting_node: Node = None
    output_map: dict[tuple[int, int], Node] = {}
    for row_idx, row in enumerate(_map):
        for col_idx, val in enumerate(row):
            if val != '.':
                continue
    
            adj_coords: list[Optional[AdjacentCoordinate]] = get_adjacent_coordinates(_map, row_idx, col_idx, get_adj_coords_context)
            output_map[(row_idx, col_idx)] = Node(
                location=(row_idx, col_idx),
                up=adj_coords[0],
                down=adj_coords[1],
                left=adj_coords[2],
                right=adj_coords[3],
            )

            if starting_node is None:
                starting_node = output_map[(row_idx, col_idx)]

    output_instructions = parse_instructions(_instructions)
    return starting_node, output_map, output_instructions


def follow_instructions(current_node: Node, map_: dict[tuple[int, int], Node], instructions: list[Instruction]) -> int:
    headings = ( 'R', 'D', 'L', 'U' )
    current_heading: Literal['R', 'D', 'L', 'U'] = "R"
    for idx, instruction in enumerate(instructions):
        if instruction.distance is not None:
            for _ in range(instruction.distance):
                adj_coordinate: AdjacentCoordinate = (
                    current_node.right if current_heading == 'R' else
                    current_node.left if current_heading == 'L' else
                    current_node.down if current_heading == 'D' else
                    current_node.up
                )

                if adj_coordinate is None:
                    break

                current_node = map_[adj_coordinate.coordinate]
                if adj_coordinate.new_heading is not None:
                    current_heading = adj_coordinate.new_heading

        elif instruction.turn is not None:
            current_heading = headings[(headings.index(current_heading) + (
                1 if instruction.turn == 'R' else
                -1
            )) % len(headings)]
        else:
            raise ValueError(f"Empty instruction at index {idx}: {instruction}")

    return (
        (1000 * (current_node.location[0] + 1)) +
        (4 * (current_node.location[1] + 1)) +
        headings.index(current_heading)
    )

if __name__ == '__main__':
    sample_input = parse_input('sample_input.txt')
    input = parse_input('input.txt')

    print("Part 1 (sample):", follow_instructions(*sample_input))
    print("Part 1:", follow_instructions(*input))

    # sample_input = parse_input('sample_input.txt', get_adjacent_coordinates_cube)
    input = parse_input('input.txt', get_adjacent_coordinates_cube)

    # print("Part 2 (sample):", follow_instructions(*sample_input))
    print("Part 2:", follow_instructions(*input))
