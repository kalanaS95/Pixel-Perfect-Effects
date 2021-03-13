import cv2
import numpy as np


class pencilSketch:
    def __init__(self, imageData):
        self.originalImage = imageData
        self.grayScaleImage = self.convert_to_grayScale(self.originalImage)
        self.negativeImage = self.image_negative(self.grayScaleImage)

    def load_image_data(self, path):
        return cv2.imread(path, cv2.IMREAD_COLOR)

    def display_Image(self, ImageName, ImageData):
        cv2.imshow(ImageName, ImageData)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def convert_to_grayScale(self, ImageData):
        return cv2.cvtColor(ImageData, cv2.COLOR_BGR2GRAY)

    def image_negative(self, ImageData):
        return 255 - ImageData

    def dnorm(self, x, mu, sd):
        return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)

    def gaussian_kernel(self, kernel_size, sigma=1):
        kernel_1D = np.linspace(-(kernel_size // 2), kernel_size // 2, kernel_size)
        for i in range(kernel_size):
            kernel_1D[i] = self.dnorm(kernel_1D[i], 0, sigma)
        kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)

        kernel_2D *= 1.0 / kernel_2D.max()

        return kernel_2D

    '''
    This function only accepts kernels with a mid point i.e 3x3, 5x5, 7x7, etc.
    '''

    def gaussian_blur(self, kernel_size, sigma, imageData):
        kernel = self.gaussian_kernel(kernel_size, sigma)
        # add padding to the image
        padding_pixels = kernel_size // 2
        image_padded = np.pad(imageData, ((padding_pixels, padding_pixels), (padding_pixels, padding_pixels)), 'constant')
        padded_h, padded_w = np.shape(image_padded)

        for row in range(padding_pixels, padded_h - padding_pixels):
            for col in range(padding_pixels, padded_w - padding_pixels):
                newPixel_val = np.sum(image_padded[row - padding_pixels:row + padding_pixels + 1, col - padding_pixels:col + padding_pixels + 1] * kernel)/ np.sum(kernel)
                if(newPixel_val > 255):
                    newPixel_val = 255
                image_padded[row][col] = newPixel_val

        #finally we need to remove the extra padding and return the image data
        return image_padded[padding_pixels:padded_h - padding_pixels, padding_pixels:padded_w - padding_pixels]

    def pencil_sketch(self, kernel_size, sigma):
        gaussian_negative = self.gaussian_blur(kernel_size, sigma, self.negativeImage)
        return self.dodge(self.grayScaleImage, gaussian_negative)


    def dodge(self, grayscale, negative):
        # determine the shape of the input image
        height, width = np.shape(grayscale)

        # prepare output argument with same size as image
        blend = np.zeros((height, width), np.uint8)

        for row in range(height):
            for col in range(width):
                # do for every pixel
                if negative[row, col] == 255:
                    # avoid division by zero
                    blend[row, col] = 255
                else:
                    # shift image pixel value by 8 bits
                    # divide by the inverse of the mask
                    tmp = (grayscale[row, col] << 8) / (255 - negative[row, col])

                    # make sure resulting value stays within bounds
                    if tmp > 255:
                        tmp = 255
                    blend[row, col] = tmp

        return blend