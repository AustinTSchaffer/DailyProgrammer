import collections
import dataclasses
import math
from typing import Tuple, List, OrderedDict, Dict


@dataclasses.dataclass(frozen=True)
class Circle:
    column: int
    row: int
    radius: int
    color: Tuple[float]


@dataclasses.dataclass(frozen=True)
class Container:
    """
    Names the properties of the rectangle, where col/row refer
    to the location of the upper left corner of the rectangle.
    """

    column: int
    row: int
    width: int
    height: int


def rect_contains_point(rectangle: Container, row: int, column: int) -> bool:
    """
    Returns true if the rectangle contains the point (row, column).
    """

    return (
        row >= rectangle.row
        and row <= (rectangle.row + rectangle.height)
        and column >= rectangle.column
        and column <= (rectangle.column + rectangle.width)
    )


def color_distance(color_1: Tuple[float], color_2: Tuple[float]) -> float:
    """
    Returns the euclidean distance between 2 colors.
    """
    assert len(color_1) == len(color_2) == 3
    return math.sqrt(
        (color_1[0] - color_2[0]) ** 2
        + (color_1[1] - color_2[1]) ** 2
        + (color_1[2] - color_2[2]) ** 2
    )


def group_circles_by_containers(
    *, circles: List[Circle], containers: List[Container]
) -> OrderedDict[Container, List[Circle]]:
    """
    Groups each circle based on the container they are contained in. The output dict is ordered
    based on the order of the input list of containers. The circle lists in each value of the output
    OrderedDict will be ordered based on each circle's row coordinate.
    """

    grouped_by_container = collections.OrderedDict()
    for container in containers:
        grouped_by_container[container] = []

    for circle in circles:
        container = next(
            (
                container
                for container in containers
                if rect_contains_point(container, row=circle.row, column=circle.column)
            )
        )

        grouped_by_container[container].append(circle)

    # Sort the circles within each container based on their Y coordinate.
    for container, _circles in grouped_by_container.items():
        grouped_by_container[container] = sorted(
            _circles, key=lambda circle: circle.row, reverse=True
        )

    return grouped_by_container
