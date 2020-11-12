# Using OpenCV to 
# Hough Circle Transform
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html


from cv2 import cv2 as cv
import numpy as np

image = cv.imread("./images/level_131.png")
output = image.copy()
gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray_image = cv.medianBlur(gray_image, 5)

# TODO: What do these params mean?
circles = cv.HoughCircles(gray_image, cv.HOUGH_GRADIENT, 1, 50,
                            param1=100, param2=30,
                            minRadius=30, maxRadius=50)

if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv.circle(output, (x, y), r, (0, 255, 0), 4)
        cv.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    # show the output image
    cv.imshow("input", cv.resize(image, (int(image.shape[1]/2.5), int(image.shape[0]/2.5))))
    cv.imshow("output", cv.resize(output, (int(output.shape[1]/2.5), int(output.shape[0]/2.5))))
    cv.waitKey(0)
