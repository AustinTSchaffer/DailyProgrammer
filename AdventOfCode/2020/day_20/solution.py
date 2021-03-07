#%%

import re
import dataclasses

tile_data = open("tiles.txt").read()
tile_regex = re.compile(r"Tile (?P<tile_id>\d+):\n(?P<tile_data>(?:[#\.]{10}\n){9}[#\.]{10})")

class Tile:
    def __init__(self, tile_id: str, tile_data: str, make_generated_props: bool=True):
        self.tile_id = tile_id
        self.tile_data = tile_data
        self.operations_performed = ()

        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.possible_edges = None

        if make_generated_props:
            _data = tile_data.split("\n")
            self.north = _data[0]
            self.south = _data[-1]
            self.east = "".join(row[-1] for row in _data)
            self.west = "".join(row[0] for row in _data)

            self.possible_edges = {
                self.north,
                self.south,
                self.east,
                self.west,
                "".join(reversed(self.north)),
                "".join(reversed(self.south)),
                "".join(reversed(self.east)),
                "".join(reversed(self.west)),
            }

    def copy(self):
        _tile = Tile(self.tile_id, self.tile_data, False)
        _tile.north = self.north
        _tile.south = self.south
        _tile.east = self.east
        _tile.west = self.west
        _tile.possible_edges = self.possible_edges
        return _tile

    def flipped_h(self):
        self = self.copy()
        temp = self.east
        self.east = self.west
        self.west = temp
        self.north = "".join(reversed(self.north))
        self.south = "".join(reversed(self.south))
        return self

    def flipped_v(self):
        self = self.copy()
        temp = self.north
        self.north = self.south
        self.south = temp
        self.east = "".join(reversed(self.east))
        self.west = "".join(reversed(self.west))
        return self

    def rotated_r(self):
        self = self.copy()
        temp = self.north
        self.north = "".join(reversed(self.west))
        self.west = self.south
        self.south = "".join(reversed(self.east))
        self.east = temp
        return self

    def rotated_l(self):
        self = self.copy()
        self.north = self.east
        self.east = "".join(reversed(self.south))
        self.south = self.west
        self.west = "".join(reversed(self.north))
        return self

    def as_tuple(self) -> tuple:
        return (self.tile_id, self.north, self.east, self.south, self.west)

    def __repr__(self) -> str:
        return repr(self.as_tuple())

    def __eq__(self, other) -> bool:
        return self.as_tuple() == other.as_tuple()

    def __hash__(self) -> int:
        return hash(self.as_tuple())

tiles = []
for tile in tile_regex.finditer(tile_data):
    tiles.append(Tile(tile["tile_id"], tile["tile_data"]))

#%% Part 1

def all_possible_neighbors(tile, tiles):
    return [
        _tile for _tile in tiles
        if _tile != tile and any(
            edge for edge in _tile.possible_edges
            if edge in (tile.north, tile.south, tile.east, tile.west)
        )
    ]

tiles_and_neighbors = {
    tile: all_possible_neighbors(tile, tiles)
    for tile in tiles
}

corner_tiles = [
    tile
    for tile, possible_neighbors in tiles_and_neighbors.items()
    if len(possible_neighbors) == 2
]

assert len(corner_tiles) == 4
import math
print("Part 1:", math.prod(int(tile.tile_id) for tile in corner_tiles))

#%% Part 2


