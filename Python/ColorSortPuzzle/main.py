# Using OpenCV to 
# Hough Circle Transform
# https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html


from cv2 import cv2 as cv
import numpy as np

original_image = cv.imread("./images/level_153.png")

# Helps the output of my phone's screenshots fit on my monitor when displaying, without rotating
# Phone: 1080x2220
# Monitor: 1920x1080
DOWNSCALE_FACTOR = 2.5
def display_image(title: str, image, downscale_factor: int=DOWNSCALE_FACTOR):
    cv.imshow(
        title,
        cv.resize(
            image,
            (int(image.shape[1]/2.5), int(image.shape[0]/2.5))
        )
    )


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
circles = [
    (x, y+HEADER_TRIM, r)
    for (x, y, r) in
    circles
]

# loop over the (x, y) coordinates and radius of the circles
image_with_circles_circled = original_image.copy()
for (x, y, r) in circles:
    # draw the circle in the output image
    cv.circle(image_with_circles_circled, (x, y), r, (0, 255, 0), 4)
    cv.circle(image_with_circles_circled, (x, y), 1, (0, 255, 0), 4)

# Show the original image side-by-side with circles circled
display_image("Circled", cv.hconcat([original_image, image_with_circles_circled]))
cv.waitKey(0)
