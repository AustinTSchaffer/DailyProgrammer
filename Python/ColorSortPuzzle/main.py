import dataclasses
from typing import List, Tuple

from cv2 import cv2 as cv
from matplotlib import pyplot as plt

import android_game
import color_sort

import tempfile
import subprocess
import io

#%% Detect Game Objects in Source Image

with tempfile.NamedTemporaryFile("w", suffix=".png") as temp_png:
    subprocess.call("adb exec-out screencap -p".split(" "), stdout=temp_png)
    ORIGINAL_IMAGE = cv.imread(temp_png.name)

circles = android_game.image_processing.find_circles(ORIGINAL_IMAGE)
color_map = android_game.image_processing.generate_color_map(circles=circles,)

containers = android_game.image_processing.find_containers(ORIGINAL_IMAGE)
grouped_by_container = android_game.game_objects.group_circles_by_containers(
    circles=circles, containers=containers,
)

#%% Highlight Objects and Show

# loop over the (x, y) coordinates and radius of the circles
display_image = ORIGINAL_IMAGE.copy()
for circle in circles:
    # Outline the circle in the output image using an inverted color to improve contrast
    inv_color = (255 - circle.color[0], 255 - circle.color[1], 255 - circle.color[2])
    cv.circle(display_image, (circle.column, circle.row), circle.radius, inv_color, 2)
    cv.circle(display_image, (circle.column, circle.row), 1, inv_color, 4)
    cv.putText(
        display_image,
        org=(circle.column, circle.row),
        text=str(color_map[circle.color]),
        fontFace=cv.FONT_HERSHEY_PLAIN,
        fontScale=2,
        thickness=3,
        color=inv_color,
    )

for rectangle in containers:
    cv.rectangle(
        display_image,
        (rectangle.column, rectangle.row),
        (rectangle.column + rectangle.width, rectangle.row + rectangle.height),
        (0, 0, 0),
        2,
    )

# Show the original image side-by-side with circles circled
plt.imshow(cv.cvtColor(cv.hconcat([ORIGINAL_IMAGE, display_image]), cv.COLOR_BGR2RGB))
plt.show(block=False)

#%% Calculate winning moves

game_state = color_sort.game.GameState(
    containers=tuple(
        (
            tuple(color_map[_circle.color] for _circle in reversed(_circles))
            for container, _circles in grouped_by_container.items()
        )
    ),
    container_size=max((len(_circles) for _circles in grouped_by_container.values())),
    one_at_a_time=True,
)

actions, solveable = color_sort.breadth_first_search_solver.solve(game_state)

#%% Automate Clicks on Android Device
process = subprocess.Popen(
    args=["adb", "shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
)

import time

with process as process:
    for action in actions:
        for container_id in (action.starting_container, action.ending_container):
            container = containers[container_id]
            center_x = container.column + int(container.width / 2)
            center_y = container.row + int(container.height / 2)
            process.stdin.write(f"input tap {center_x} {center_y} &\n".encode("utf8"))
            process.stdin.flush()
            time.sleep(0.2)
