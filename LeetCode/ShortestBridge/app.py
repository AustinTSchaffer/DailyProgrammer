from typing import List, Tuple, Iterable
import unittest

import example_maps


def find_islands_seed_algorithm(map_: List[List[int]]) -> List[set]:
    islands = []

    # Convert map of coordinates to set of coordinates of all cells that
    # are 1. This set of coordinates will serve as the set of coordinates
    # that have not yet been grouped as being part of any island. A set is
    # appropriate because O(1) lookup time will be useful later.
    ungrouped_land_coordinates = {
        (i, j) for i, row in enumerate(map_) for j, cell in enumerate(row) if cell == 1
    }

    while any(ungrouped_land_coordinates):
        # Pick an arbitrary land coordinate from the set of land
        # coordinates as a "seed". Island 1 will be grown from
        # that seed by scanning outward from that seed.
        first_seed = next(iter(ungrouped_land_coordinates))
        current_island = [first_seed]
        ungrouped_land_coordinates.remove(first_seed)
        ungrown_seeds = [first_seed]

        while any(ungrown_seeds):
            next_round_of_seeds = []
            for current_seed in ungrown_seeds:

                # Calculate the coordinates of the cells that border the
                # current seed and check to see if any of them exist in
                # the set of ungrouped coordinates. Coordinates are only
                # connected vertically and horizontally.
                connected_coordinates = generate_bordering_coordinates(current_seed)

                for coordinate in connected_coordinates:
                    if coordinate in ungrouped_land_coordinates:
                        # Coordinate is now grouped under the current island
                        current_island.append(coordinate)
                        ungrouped_land_coordinates.remove(coordinate)
                        # We'll want to see if that coordinate also has neighbors.
                        next_round_of_seeds.append(coordinate)
            ungrown_seeds = next_round_of_seeds

        islands.append(current_island)

    return islands


def find_islands_disjoint_sets_algorithm(map_: List[List[int]]) -> List[set]:
    raise NotImplementedError()


def find_islands_depth_first_search(map_: List[List[int]]) -> list:
    visited_coordinates = set()

    def in_bounds(coordinate: tuple) -> bool:
        return (
            coordinate[0] >= 0 and
            coordinate[0] < len(map_) and
            coordinate[1] >= 0 and
            coordinate[1] < len(map_[0])
        )

    def dfs_add_to_island(coordinate: tuple, current_island: list):
        if coordinate in visited_coordinates:
            return
        visited_coordinates.add(coordinate)

        if not in_bounds(coordinate):
            return

        if not map_[coordinate[0]][coordinate[1]]:
            return

        current_island.append(coordinate)

        for _coordinate in generate_bordering_coordinates(coordinate):
            dfs_add_to_island(_coordinate, current_island)

    islands = []
    for i, row in enumerate(map_):
        for j, cell in enumerate(row):
            coordinate = (i,j)
            if cell and (coordinate not in visited_coordinates):
                current_island = []
                islands.append(current_island)
                dfs_add_to_island(coordinate, current_island)

    return islands


def manhattan(coord_1: Tuple[int, int], coord_2: Tuple[int, int]) -> int:
    """
    Returns the manhattan distance between 2 coordinates.
    """
    return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])


def generate_bordering_coordinates(
    coordinate: Tuple[int, int], include_diagonals=False
) -> Iterable[Tuple[int, int]]:
    """
    Generates the coordinates that border the specified coordinate.
    """

    yield (coordinate[0] + 1, coordinate[1])
    yield (coordinate[0] - 1, coordinate[1])
    yield (coordinate[0], coordinate[1] + 1)
    yield (coordinate[0], coordinate[1] - 1)

    if include_diagonals:
        yield (coordinate[0] + 1, coordinate[1] + 1)
        yield (coordinate[0] - 1, coordinate[1] - 1)
        yield (coordinate[0] - 1, coordinate[1] + 1)
        yield (coordinate[0] + 1, coordinate[1] - 1)


def determine_boundary(island: set) -> set:
    """
    Determines the border of the specified island.

    This is achieved by checking each coordinate in the island to see if it
    has any neighbors which are not in the island. Not a great algorithm for
    islands that have a lot of lakes, rivers, fjords, inlets, etc, but still
    useful for pruning land features that are not connected to any water
    features.
    """
    return {
        coordinate
        for coordinate in island
        if any(
            filter(
                lambda _coordinate: _coordinate not in island,
                generate_bordering_coordinates(coordinate),
            )
        )
    }


class Solution:
    def shortestBridge(self, A: List[List[int]]) -> int:
        return self.shortest_bridge(A, find_islands_depth_first_search,)

    @staticmethod
    def shortest_bridge(map_: List[List[int]], find_islands_alg) -> int:
        islands = find_islands_alg(map_)
        assert len(islands) == 2, "There must be 2 islands."
        island_1, island_2 = islands

        # Determine the boundaries of each island. This will dramatically improve
        # the performance of the part after this.
        island_1_boundary = determine_boundary(island_1)
        island_2_boundary = determine_boundary(island_2)

        # Determine the 2 coordinates from each island that are the shortest
        # manhattan distance from each other with a crappy O(n*m) algrorithm
        # where n and m are the size of each island.
        island_1_coordinate = next(iter(island_1_boundary))
        island_2_coordinate = next(iter(island_2_boundary))
        shortest_distance = manhattan(island_1_coordinate, island_2_coordinate)
        for coord_1 in island_1_boundary:
            for coord_2 in island_2_boundary:
                current_distance = manhattan(coord_1, coord_2)
                if current_distance < shortest_distance:
                    island_1_coordinate = coord_1
                    island_2_coordinate = coord_2
                    shortest_distance = current_distance

        # At this point we have 1 coordinate from each island, each forming 2
        # sides of a strait. The fewest number of 0s that we should need to
        # flip between the 2 coordinates in order to form the shortest land
        # bridge between the 2 islands should be 1 less than the manhattan
        # distance between the 2 points.
        return shortest_distance - 1


class Tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.find_island_algorithms = [
            find_islands_seed_algorithm,
            find_islands_depth_first_search,
        ]

    def test_example_1(self):
        for alg in self.find_island_algorithms:
            self.assertEqual(Solution().shortest_bridge(example_maps.EXAMPLE_1, alg), 1)

    def test_example_2(self):
        for alg in self.find_island_algorithms:
            self.assertEqual(Solution().shortest_bridge(example_maps.EXAMPLE_2, alg), 2)

    def test_example_3(self):
        for alg in self.find_island_algorithms:
            self.assertEqual(Solution().shortest_bridge(example_maps.EXAMPLE_3, alg), 1)

    def test_example_4(self):
        for alg in self.find_island_algorithms:
            self.assertEqual(Solution().shortest_bridge(example_maps.EXAMPLE_4, alg), 44)


if __name__ == "__main__":
    unittest.main()
