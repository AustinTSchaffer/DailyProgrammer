from typing import List

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        WORD_LEN = len(word)

        # Null case
        if WORD_LEN == 0:
            return True

        HEIGHT = len(board)
        WIDTH = len(board[0])

        def _in_bounds(coord: tuple) -> bool:
            """
            Returns true if the specified coordinate is within the bounds of the
            board.
            """
            return (
                coord[0] >= 0 and coord[0] < HEIGHT
                and coord[1] >= 0 and coord[1] < WIDTH
            )

        def _unvisited_neighbors(coord: tuple, visited_cells: set):
            """
            Tuple iterator, ensuring that the coordinates in the output are in
            bounds and have not been visited.
            """
            # Down
            next_coord = (coord[0] + 1, coord[1])
            if next_coord not in visited_cells and _in_bounds(next_coord):
                yield next_coord
            # Up
            next_coord = (coord[0] - 1, coord[1])
            if next_coord not in visited_cells and _in_bounds(next_coord):
                yield next_coord
            # Right
            next_coord = (coord[0], coord[1] + 1)
            if next_coord not in visited_cells and _in_bounds(next_coord):
                yield next_coord
            # Left
            next_coord = (coord[0], coord[1] - 1)
            if next_coord not in visited_cells and _in_bounds(next_coord):
                yield next_coord

        def _recurse(coordinate: tuple, visited_cells: set) -> bool:
            """
            Internal recursive helper function. DFS through board to build a path
            that matches the input word. Since the output doesn't need to
            reconstruct and ordered path through the board, uses a set as a stack
            to keep track of visited cells, due to its O(1) lookup time.
            """
            num_visited_cells = len(visited_cells)

            if word[num_visited_cells] == board[coordinate[0]][coordinate[1]]:
                # Exit case (null case handled above)
                if num_visited_cells + 1 == WORD_LEN:
                    return True

                # Add current position to "stack"
                visited_cells.add(coordinate)

                # DFS through board
                for neighbor in _unvisited_neighbors(coordinate, visited_cells):
                    if _recurse(neighbor, visited_cells):
                        return True

                # Remove current position from "stack"
                visited_cells.remove(coordinate)

            return False

        for row in range(HEIGHT):
            for col in range(WIDTH):

                # Using a "set" as a "stack" because (a) I can and (b) I want
                # O(1) lookup times.
                stack = set()
                if _recurse((row, col), stack):
                    return True

        return False
