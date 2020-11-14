# Using OpenCV to 
# Hough Circle Transform
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html

#%%

import dataclasses

from cv2 import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

original_image = cv.imread("./images/level_153.png")

# Trimming factors to remove irrelevant portions of the image which might contain circles.
HEADER_TRIM = 150
FOOTER_TRIM = 150

working_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
working_image = cv.medianBlur(working_image, 5)
working_image = working_image[HEADER_TRIM:-FOOTER_TRIM, 0:]

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

circles = [
    Circle(x, y+HEADER_TRIM, r)
    for (x, y, r) in
    circles
]

#%%

# loop over the (x, y) coordinates and radius of the circles
display_image = original_image.copy()
for circle in circles:
    # draw the circle in the output image
    cv.circle(display_image, (circle.column, circle.row), circle.radius, (0, 255, 0), 4)
    cv.circle(display_image, (circle.column, circle.row), 1, (0, 255, 0), 4)

# Show the original image side-by-side with circles circled
plt.imshow(cv.hconcat([original_image, display_image]))
plt.show()
