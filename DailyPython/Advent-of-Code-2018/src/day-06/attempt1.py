import os
import math
import collections

COORDINATES_DATA_FILE = os.path.join(
    os.path.dirname(__file__), 
    'data.txt'
)

def manhattan_distance(c1, c2):
    return (
        abs(c1[0] - c2[0]) +
        abs(c1[1] - c2[1])
    )

def load_coordinates(filename):
    coordinates = []
    with open(filename, 'r') as file:
        for coordinate_pair in file:
            if coordinate_pair:
                coordinates.append(tuple(
                    int(str.strip(coord))
                    for coord in
                    coordinate_pair.split(',')
                ))
    return coordinates

def part1(coordinates):
    x_min = min(_[0] for _ in coordinates)
    x_max = max(_[0] for _ in coordinates)
    y_min = min(_[1] for _ in coordinates)
    y_max = max(_[1] for _ in coordinates)

    infinite_areas = set()
    bounded_areas = collections.defaultdict(list)

    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            current_coordinate = (x,y)
            closest_master_coordinate = None
            closest_coordinate_is_bogus = False
            current_closest_distance = 9999999999999
            for master_coordinate in coordinates:
                current_distance = manhattan_distance(
                    current_coordinate, master_coordinate
                )
                if current_distance == current_closest_distance:
                    # This means that the current location is equally close to
                    # at least 2 master coordinates
                    closest_coordinate_is_bogus = True
                    break

                if current_distance < current_closest_distance:
                    current_closest_distance = current_distance
                    closest_master_coordinate = master_coordinate

            if closest_coordinate_is_bogus:
                continue
            
            if x == x_min or x == x_max or y == y_min or y == y_max:
                # HAH, sucker. You don't count
                infinite_areas.add(closest_master_coordinate)
                continue

            if closest_master_coordinate not in infinite_areas:
                bounded_areas[closest_master_coordinate].append(current_coordinate)
    
    for i in infinite_areas:
        if i in bounded_areas:
            del bounded_areas[i]

    ordered_by_area_size = sorted(
        bounded_areas.items(),
        key=lambda ba: len(ba[1]),
        reverse=True,
    )

    print('Done')

if __name__ == "__main__":
    coordinates = load_coordinates(COORDINATES_DATA_FILE)
    part1(coordinates)
