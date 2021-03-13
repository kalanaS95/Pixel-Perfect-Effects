import cv2
import numpy as np
from random import randrange

class utils:
    def __init__(self, imagePath):
        self.Imagepath = imagePath

    def load_image_data(self):
        return cv2.imread(self.Imagepath, cv2.IMREAD_COLOR)

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def convert_to_grayScale(self, ImageData):
        return cv2.cvtColor(ImageData, cv2.COLOR_BGR2GRAY)

    def image_negative(self, ImageData):
        return 255 - ImageData

    # algorithm reference: https://courses.cs.vt.edu/~masc1044/L17-Rotation/ScalingNN.html
    def reSize_img_grayScale(self, imgData, newHeight, newWidth):
        original_height, original_width = np.shape(imgData)

        #create an empty matrix to hold new data
        resized = np.zeros((newHeight, newWidth), dtype=np.uint8)

        for col in range(newWidth):
            for row in range(newHeight):
                src_row = min(int(round(float(row)/float(newHeight) * float(original_height))), original_height - 1)
                src_col = min(int(round(float(col)/float(newWidth) * float(original_width))), original_width - 1)
                resized[row][col] = imgData[src_row][src_col]

        return resized

