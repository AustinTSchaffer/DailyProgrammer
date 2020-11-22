from typing import Dict, List, Tuple

from cv2 import cv2 as cv
import numpy as np

from . import game_objects


def create_working_image(original_image, header_trim=150, footer_trim=150):
    """
    Returns a cropped, blurred, grayscale version of the original image.
    """
    working_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
    working_image = cv.medianBlur(working_image, 5)
    working_image = working_image[header_trim:-footer_trim, :]
    return working_image


def find_circles(
    original_image,
    header_trim=150,
    footer_trim=150,
    min_radius=30,
    max_radius=50,
    min_dist=50,
) -> game_objects.Circle:
    """
    Finds all circles in the source image, excluding any circles that
    may exist in a header or footer. Returns a list of Circles, which
    includes each circle's x/y coordinate, radius, and color.
    """

    working_image = create_working_image(
        original_image, header_trim=header_trim, footer_trim=footer_trim
    )

    # TODO: What do param1 and param2 do?
    hough_circles = cv.HoughCircles(
        working_image,
        cv.HOUGH_GRADIENT,
        1,
        minDist=min_dist,
        param1=100,
        param2=30,
        minRadius=min_radius,
        maxRadius=max_radius,
    )

    assert hough_circles is not None, "Could not detect any circles"

    # convert the (x, y) coordinates and radius of the circles to integers
    hough_circles = np.round(hough_circles[0, :]).astype("int")

    circles: List[game_objects.Circle] = []
    for (column, row, radius) in hough_circles:
        # Add the header trim back
        row = row + header_trim

        # Determines the color of the circle in the original image using a mask. Masks the color
        # of the circle with a circle of half the radius, to help reduce color issues due to
        # shadows and anti-aliasing.
        mask = np.zeros(original_image.shape[:2], dtype="uint8")
        mask = cv.circle(
            mask,
            center=(column, row),
            radius=int(radius / 2),
            color=(255, 255, 255),
            thickness=cv.FILLED,
        )

        mean_color = cv.mean(original_image, mask=mask)
        mean_color = mean_color[:3]

        circle = game_objects.Circle(
            column=column,
            row=row,
            radius=radius,
            color=mean_color,
        )

        circles.append(circle)

    return circles


def find_containers(
    original_image,
    header_trim=150,
    footer_trim=150,
) -> List[game_objects.Container]:
    """
    Finds all rectangles in the source image, excluding any rectangles that
    may exist in a header or footer and any rectangle contained by any other
    rectangle, labelling each as a container. Returns a list of containers,
    which includes each container's upper-left x/y coordinate, width, and
    height.
    """

    working_image = create_working_image(original_image)

    # Converts working_image to a black/white image which makes the countours algorithm
    # work better. WHITE_THRESHOLD sets the lower/upper bounds on what brightnesses
    # should be considered "white". These values were selected through trial and error,
    # visually inspecting the resulting `thresh` with `plt.imshow`
    WHITE_THRESHOLD = (200, 255)
    _, thresh = cv.threshold(working_image, *WHITE_THRESHOLD, cv.THRESH_BINARY)

    # Uses cv.findContours to sketch out the boundaries of all objects that passed the
    # threshold filter. TODO: What is hierarchy for?
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # Generates bounding rectangles for all
    bounding_rectangles: List[game_objects.Container] = []
    for contour in contours:
        bounds = cv.boundingRect(contour)
        rectangle = game_objects.Container(
            column=bounds[0],
            row=bounds[1] + header_trim,
            width=bounds[2],
            height=bounds[3],
        )
        bounding_rectangles.append(rectangle)

    # Determine which rectangles are not bounded by any of the other bounding rectangles.
    # That should result in a list that we can consider the "containers".
    containers: List[game_objects.Container] = []

    # Casual N^2 Alg to make sure that each bounding rectangle is contained by no other bounding rectangle
    for current in bounding_rectangles:
        contained_by = next(
            (
                other
                for other in bounding_rectangles
                if other != current
                and game_objects.rect_contains_point(other, current.row, current.column)
            ),
            None,
        )

        if contained_by is None:
            containers.append(current)

    return containers


def generate_color_map(
    circles: List[game_objects.Circle], max_color_distance=3
) -> Dict[Tuple[float], int]:
    """
    Generates a map that links circle colors to common values. This is to account for the
    fact that each circle's color may not an exact value.
    """

    color_map = {}
    next_color = 0
    for circle in circles:
        matching_color = next(
            (
                color
                for color in color_map
                if game_objects.color_distance(circle.color, color)
                <= max_color_distance
            ),
            None,
        )

        if matching_color:
            color_map[circle.color] = color_map[matching_color]
        else:
            color_map[circle.color] = next_color
            next_color += 1

    return color_map
