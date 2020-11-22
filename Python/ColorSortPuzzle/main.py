# Using OpenCV to
# Hough Circle Transform
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html

#%% Detect Circles in Source Image

import dataclasses
from typing import List, Tuple

from cv2 import cv2 as cv
from matplotlib import pyplot as plt

import android_game
import color_sort

IMAGE_LEVEL_NAME = "level_135.png"
ORIGINAL_IMAGE = cv.imread(f"./images/{IMAGE_LEVEL_NAME}")

circles = android_game.image_processing.find_circles(ORIGINAL_IMAGE)
containers = android_game.image_processing.find_containers(ORIGINAL_IMAGE)
grouped_by_container = android_game.game_objects.group_circles_by_containers(
    circles=circles,
    containers=containers,
)

color_map = android_game.image_processing.generate_color_map(
    circles=circles,
)

#%% Highlight Objects and Show

# loop over the (x, y) coordinates and radius of the circles
display_image = ORIGINAL_IMAGE.copy()
for circle in circles:
    # Outline the circle in the output image using an inverted color to improve contrast
    inv_color = (255 - circle.color[0], 255 - circle.color[1], 255 - circle.color[2])
    cv.circle(display_image, (circle.column, circle.row), circle.radius, inv_color, 2)
    cv.circle(display_image, (circle.column, circle.row), 1, inv_color, 4)

for rectangle in containers:
    cv.rectangle(
        display_image,
        (rectangle.column, rectangle.row),
        (rectangle.column + rectangle.width, rectangle.row + rectangle.height),
        (0, 0, 0),
        2,
    )

# Show the original image side-by-side with circles circled
cv.imwrite(f"./images/objects_identified/{IMAGE_LEVEL_NAME}", display_image)
# plt.imshow(cv.cvtColor(cv.hconcat([ORIGINAL_IMAGE, display_image]), cv.COLOR_BGR2RGB))
# plt.show(block=False)

#%% Calculate winning moves

game_state = color_sort.game.GameState(
    containers=tuple(
        (
            tuple(color_map[_circle.color] for _circle in _circles)
            for container, _circles in grouped_by_container.items()
        )
    ),
    container_size=max((len(_circles) for _circles in grouped_by_container.values())),
    one_at_a_time=True,
)

actions, solveable = color_sort.breadth_first_search_solver.solve(game_state)
