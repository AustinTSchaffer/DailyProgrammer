from typing import List, Tuple, Iterable
import unittest

class Solution:
    def islandPerimeter(self, grid: List[List[int]]) -> int:
        return determine_perimeter(grid)

def determine_perimeter(map_: List[List[int]]) -> list:
    def bfs_determine_perimeter(coordinate: tuple) -> int:
        visited_coordinates = set()
        seeds_current_round = [coordinate]
        perimeter = 0

        while any(seeds_current_round):
            seeds_next_round = []
            for seed in seeds_current_round:
                if seed in visited_coordinates:
                    continue
                visited_coordinates.add(seed)

                for neighbor in generate_bordering_coordinates(seed):
                    is_land = (
                        neighbor[0] >= 0 and
                        neighbor[0] < len(map_) and
                        neighbor[1] >= 0 and
                        neighbor[1] < len(map_[0]) and
                        map_[neighbor[0]][neighbor[1]]
                    )

                    if not is_land:
                        perimeter += 1
                    else:
                        seeds_next_round.append(neighbor)

            seeds_current_round = seeds_next_round

        return perimeter

    # Find the first non-0 cell
    for i, row in enumerate(map_):
        for j, cell in enumerate(row):
            if cell:
                # Return perimeter starting from that cell.
                return bfs_determine_perimeter((i,j))

    return 0

def generate_bordering_coordinates(
    coordinate: Tuple[int, int], include_diagonals=False
) -> Iterable[Tuple[int, int]]:
    """
    Generates the coordinates that border the specified coordinate.
    """
    return (
        (coordinate[0] + 1, coordinate[1]),
        (coordinate[0] - 1, coordinate[1]),
        (coordinate[0], coordinate[1] + 1),
        (coordinate[0], coordinate[1] - 1),
    )


TEST_MAP = [
    [0,1,0,0],
    [1,1,1,0],
    [0,1,0,0],
    [1,1,0,0],
]

class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(determine_perimeter(TEST_MAP), 16)
