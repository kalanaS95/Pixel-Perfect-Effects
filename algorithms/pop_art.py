from algorithms.utils import *

class popArt:
    def __init__(self, imagePath, ImageData):
        self.utils_ = utils(imagePath)
        self.originalImage = ImageData
        self.grayScaleImage = utils.convert_to_grayScale(self.utils_, self.originalImage)


    def perform_popArt(self, backgroundColor, dotsColor, multiplier, maxdots):
        original_height, original_width = np.shape(self.grayScaleImage)

        if(original_height == max(original_height, original_width)):
            downsized = cv2.resize(self.grayScaleImage, (int(original_height * maxdots/original_width), maxdots))
        else:
            downsized = cv2.resize(self.grayScaleImage, (maxdots, int(original_height * maxdots/original_width)))

        # get downsized image height and width
        downsized_height, downsized_width = np.shape(downsized)

        # lets create a blank canvas with the user given background color
        canvas = np.full(((downsized_height * multiplier), (downsized_width * multiplier), 3), backgroundColor, dtype=np.uint8)

        # lets calculate padding value to ensure our circles are drawn starting at the edge
        padding = int(multiplier / 2)

        # lets fill the canvas with dots
        for row in range(0, downsized_height):
            for col in range(0, downsized_width):
                cv2.circle(canvas, ((col * multiplier) + padding, (row * multiplier) + padding), int((0.6 * multiplier) * ((255 - downsized[row][col]) / 255)), dotsColor, -1)


        return canvas
