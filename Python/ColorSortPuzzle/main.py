# Using OpenCV to 
# Hough Circle Transform
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html

#%% Detect Circles in Source Image

import dataclasses
from typing import List

from cv2 import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

original_image = cv.imread("./images/level_153.png")

# Trimming factors to remove irrelevant portions of the image which might contain circles.
header_trim = 150
footer_trim = 150

working_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
working_image = cv.medianBlur(working_image, 5)
working_image = working_image[header_trim:-footer_trim, :]

# TODO: What do these params mean?
circles = cv.HoughCircles(working_image, cv.HOUGH_GRADIENT, 1, 50,
                            param1=100, param2=30,
                            minRadius=30, maxRadius=50)

assert circles is not None, "Could not detect any circles"

# convert the (x, y) coordinates and radius of the circles to integers
circles = np.round(circles[0, :]).astype("int")

# Convert the circle coordinates to the 2D space of the original image
@dataclasses.dataclass
class Circle:
    column: int
    row: int
    radius: int
    # TODO: Better datatype for color
    color: int

circles: List[Circle] = [
    Circle(
        column=x,
        row=y+header_trim,
        radius=r,
        # TODO: Determine color of dot in image. Either color of center point pixel
        # or average color of all pixels within a slightly smaller circle, to avoid
        # antialiased colors.
        color=1
    )
    for (x, y, r) in
    circles
]

#%% Highlight Circles and Show

# loop over the (x, y) coordinates and radius of the circles
display_image = original_image.copy()
for circle in circles:
    # draw the circle in the output image
    cv.circle(display_image, (circle.column, circle.row), circle.radius, (0, 0, 0), 4)
    cv.circle(display_image, (circle.column, circle.row), 1, (0, 0, 0), 4)

# Show the original image side-by-side with circles circled
plt.imshow(cv.cvtColor(cv.hconcat([original_image, display_image]), cv.COLOR_BGR2RGB))
plt.show()

#%% Group Circles into Containers

# Group circles into containers. This first sorts them
# by column with some flex to allow for issues related to imperfect circle
# detection, then groups them into their respective containers.

import collections

column_flex = 2
grouped_by_column = collections.defaultdict(list)
for circle in circles:
    found_friends = False
    for column_num, circle_group in grouped_by_column.items():
        if abs(circle.column - column_num) <= column_flex:
            found_friends = True
            circle_group.append(circle)
    if not found_friends:
        grouped_by_column[circle.column].append(circle)

# TODO: Determine this from the data somehow. Maybe in the future it would be
# better to determine the bounding boxes using opencv instead.
container_size = 4
empty_containers = 2

grouped_by_container = []
for column_group in grouped_by_column.values():
    pass

puzzle = ()
