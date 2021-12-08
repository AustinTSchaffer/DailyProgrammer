#%%

class LineSegment:
    def __init__(self, data: str):
        self._data = data
        start, end = data.split(" -> ")
        self.start = tuple(map(int, start.split(",")))
        self.end = tuple(map(int, end.split(",")))

    def __repr__(self):
        return self._data
    
    def is_diagonal(self) -> bool:
        return (
            self.start[0] != self.end[0] and
            self.start[1] != self.end[1]
        )

    def points(self):
        if self.is_diagonal():
            yield from self.diagonal_points()
            return

        increment_index = (
            1
            if self.start[0] == self.end[0] else
            0
        )

        increment_value = (
            1
            if self.start[increment_index] < self.end[increment_index] else
            -1
        )

        point = self.start
        while point != self.end:
            yield point
            point = [point[0], point[1]]
            point[increment_index] += increment_value
            point = tuple(point)

        yield point

    def diagonal_points(self):
        x_increment = (
            1
            if self.start[0] < self.end[0] else
            -1
        )

        y_increment = (
            1
            if self.start[1] < self.end[1] else
            -1
        )

        point = self.start
        while point != self.end:
            yield point
            point = (point[0] + x_increment, point[1] + y_increment)

        yield point

import common
line_segments = common.get_input(__file__, LineSegment)

import collections
map_ = collections.defaultdict(int)

for segment in line_segments:
    if segment.is_diagonal():
        continue

    for point in segment.points():
        map_[point] += 1

part_1 = 0
for value in map_.values():
    if value > 1:
        part_1 += 1

print("Part 1:", part_1)

map_ = collections.defaultdict(int)
for segment in line_segments:
    for point in segment.points():
        map_[point] += 1

part_2 = 0
for value in map_.values():
    if value > 1:
        part_2 += 1

print("Part 2:", part_2)
# %%
