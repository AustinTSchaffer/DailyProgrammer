# Using OpenCV to 
# Hough Circle Transform
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html

#%% Detect Circles in Source Image

import dataclasses
from typing import List, Tuple

from cv2 import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

IMAGE_LEVEL_NAME = "level_153.png"
ORIGINAL_IMAGE = cv.imread(f"./images/{IMAGE_LEVEL_NAME}")

# Trimming factors to remove irrelevant portions of the image which might contain circles.
HEADER_TRIM = 150
FOOTER_TRIM = 150

working_image = cv.cvtColor(ORIGINAL_IMAGE, cv.COLOR_BGR2GRAY)
working_image = cv.medianBlur(working_image, 5)
working_image = working_image[HEADER_TRIM:-FOOTER_TRIM, :]

def show_image(image):
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    plt.show()

# TODO: What do these params mean?
hough_circles = cv.HoughCircles(working_image, cv.HOUGH_GRADIENT, 1, 50,
                            param1=100, param2=30,
                            minRadius=30, maxRadius=50)

assert hough_circles is not None, "Could not detect any circles"

# convert the (x, y) coordinates and radius of the circles to integers
hough_circles = np.round(hough_circles[0, :]).astype("int")

# Convert the circle coordinates to the 2D space of the original image
@dataclasses.dataclass
class Circle:
    column: int
    row: int
    radius: int
    color: Tuple[float]

circles: List[Circle] = []
for (column, row, radius) in hough_circles:
    # Add the header trim back
    row = row + HEADER_TRIM

    # Determines the color of the circle in the original image using a mask. Masks the color
    # of the circle with a circle of half the radius, to help reduce color issues due to
    # shadows and anti-aliasing.
    mask = np.zeros(ORIGINAL_IMAGE.shape[:2], dtype="uint8")
    mask = cv.circle(
        mask,
        center=(column, row),
        radius=int(radius / 2),
        color=(255, 255, 255),
        thickness=cv.FILLED,
    )

    mean_color = cv.mean(ORIGINAL_IMAGE, mask=mask)
    mean_color = mean_color[:3]

    circle = Circle(
        column=column,
        row=row,
        radius=radius,
        color=mean_color,
    )

    circles.append(circle)


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
        row=bounds[1] + HEADER_TRIM,
        width=bounds[2],
        height=bounds[3],
    )
    bounding_rectangles.append(rectangle)

# Determine which rectangles are not bounded by any of the other bounding rectangles.
# That should result in a list that we can consider the "containers".
containers: List[Rectangle] = []

def rect_contains_point(rectangle: Rectangle, row: int, column: int):
    return (
        row >= rectangle.row and
        row <= (rectangle.row + rectangle.height) and
        column >= rectangle.column and
        column <= (rectangle.column + rectangle.width)
    )

# Casual N^2 Alg to make sure that each bounding rectangle is contained by no other bounding rectangles
for current in bounding_rectangles:
    contained_by = next(
        (
            other for other in bounding_rectangles
            if other != current and rect_contains_point(other, current.row, current.column)
        ),
        None
    )

    if contained_by is None:
        containers.append(current)

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
        (0,0,0),
        2,
    )

# Show the original image side-by-side with circles circled
cv.imwrite(f"./images/objects_identified_{IMAGE_LEVEL_NAME}", display_image)
plt.imshow(cv.cvtColor(cv.hconcat([ORIGINAL_IMAGE, display_image]), cv.COLOR_BGR2RGB))
plt.show()

#%% Group Circles into Containers

# TODO:
