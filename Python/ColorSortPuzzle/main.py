# Using OpenCV to 
# Hough Circle Transform
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html

#%% Detect Circles in Source Image

import dataclasses
from typing import List

from cv2 import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

IMAGE_LEVEL_NAME = "level_153.png"
original_image = cv.imread(f"./images/{IMAGE_LEVEL_NAME}")

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
    for (x, y, r) in circles
]

#%% Detect Containers in Source Image

import os

# Converts working_image to a black/white image which makes the countours algorithm
# work better. WHITE_THRESHOLD sets the lower/upper bounds on what brightnesses
# should be considered "white". These values were selected through trial and error,
# visually inspecting the resulting `thresh` with `plt.imshow`
WHITE_THRESHOLD = (200, 255)
_, thresh = cv.threshold(working_image, *WHITE_THRESHOLD, cv.THRESH_BINARY)

# Uses cv.findContours to sketch out the boundaries of all objects that passed the
# threshold filter.
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# TODO: What is hierarchy for?

def draw_contour(*, contour_index=-1, show, save):
    output = cv.drawContours(
        image=cv.cvtColor(working_image.copy(), cv.COLOR_GRAY2BGR),
        contours=contours,
        contourIdx=contour_index,
        color=(0,0,255), # "Red" in BGR colorspace
        thickness=2,
    )

    if show:
        plt.imshow(output)
        plt.show()

    if save:
        os.makedirs(f"./images/contours/{IMAGE_LEVEL_NAME}", exist_ok=True)
        cv.imwrite(f"./images/contours/{IMAGE_LEVEL_NAME}/contour_{contour_index}.png", output)

    return output

# Saves all contours to storage so they can be easily viewed in series.
for i, contour in enumerate(contours):
    draw_contour(contour_index=i, show=False, save=True)

@dataclasses.dataclass
class Rectangle:
    """
    Names the properties of the rectangle, where col/row refer
    to the location of the upper left corner of the rectangle.
    """
    column: int
    row: int
    width: int
    height: int

# Generates bounding rectangles for all 
bounding_rectangles: List[Rectangle] = []
for contour in contours:
    bounds = cv.boundingRect(contour)
    rectangle = Rectangle(
        column=bounds[0],
        row=bounds[1] + header_trim,
        width=bounds[2],
        height=bounds[3],
    )
    bounding_rectangles.append(rectangle)

# Determine which rectangles are not bounded by any of the other bounding rectangles.
# That should result in a list that we can consider the "containers".
containers: List[Rectangle] = []

def r1_contains_r2(r1: Rectangle, r2: Rectangle):
    return (
        r2.row >= r1.row and
        r2.row <= (r1.row + r1.height) and
        r2.column >= r1.column and
        r2.column <= (r1.column + r1.width)
    )

# Casual N^2 Alg
for current in bounding_rectangles:
    contained_by_one = any(filter(lambda other: other != current and r1_contains_r2(other, current), bounding_rectangles))
    if not contained_by_one:
        containers.append(current)

#%% Highlight Objects and Show

# loop over the (x, y) coordinates and radius of the circles
display_image = original_image.copy()
for circle in circles:
    # draw the circle in the output image
    cv.circle(display_image, (circle.column, circle.row), circle.radius, (0, 0, 0), 2)
    cv.circle(display_image, (circle.column, circle.row), 1, (0, 0, 0), 4)

for rectangle in containers:
    cv.rectangle(
        display_image,
        (rectangle.column, rectangle.row),
        (rectangle.column + rectangle.width, rectangle.row + rectangle.height),
        (0,0,0),
        2,
    )

# Show the original image side-by-side with circles circled
cv.imwrite(f"./images/objects_identified_{IMAGE_LEVEL_NAME}", display_image)
plt.imshow(cv.cvtColor(cv.hconcat([original_image, display_image]), cv.COLOR_BGR2RGB))
plt.show()

#%% Group Circles into Containers

# TODO:
