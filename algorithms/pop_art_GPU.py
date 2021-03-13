from algorithms.utils import *
from numba import jit, cuda

def popArt(ImageData, backgroundColor, dotsColor, multiplier, maxdots):
    grayScaleImage = cv2.cvtColor(ImageData, cv2.COLOR_BGR2GRAY)
    original_height, original_width = np.shape(grayScaleImage)

    if (original_height == max(original_height, original_width)):
        downsized = cv2.resize(grayScaleImage, (int(original_height * maxdots / original_width), maxdots))
    else:
        downsized = cv2.resize(grayScaleImage, (maxdots, int(original_height * maxdots / original_width)))

    perform_popArt(downsized, backgroundColor, dotsColor, multiplier, maxdots)

@jit(nopython=True)
def perform_popArt(downsized, backgroundColor, dotsColor, multiplier, maxdots):


    # get downsized image height and width
    downsized_height, downsized_width = np.shape(downsized)

    # lets create a blank canvas with the user given background color
    canvas = np.full(((downsized_height * multiplier), (downsized_width * multiplier), 3), backgroundColor,
                     dtype=np.uint8)

    # lets calculate padding value to ensure our circles are drawn starting at the edge
    padding = int(multiplier / 2)

    # lets fill the canvas with dots
    for row in range(0, downsized_height):
        for col in range(0, downsized_width):
            cv2.circle(canvas, ((col * multiplier) + padding, (row * multiplier) + padding),int((0.6 * multiplier) * ((255 - downsized[row][col]) / 255)), dotsColor, -1)

    return canvas

