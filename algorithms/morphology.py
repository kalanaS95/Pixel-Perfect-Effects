from algorithms.utils import *

class morphology:
    def __init__(self, imagePath):
        self.utils_ = utils(imagePath)
        self.originalImage = utils.load_image_data(self.utils_)
        self.grayScaleImage = utils.convert_to_grayScale(self.utils_, self.originalImage)

    def create_kernel_structure(self, kernelSize, kernel_structure):
        if kernel_structure.lower() == "rectangle":
            return cv2.getStructuringElement(cv2.MORPH_RECT, (kernelSize, kernelSize))
        elif kernel_structure.lower() == "ellipse":
            return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernelSize, kernelSize))
        elif kernel_structure.lower() == "cross":
            return cv2.getStructuringElement(cv2.MORPH_CROSS, (kernelSize, kernelSize))

    def dilation(self, grayScaleImage, kernelSize, kernel_structure):
        # get kernel we need
        kernel = self.create_kernel_structure(kernelSize, kernel_structure)
        # add padding to the image
        padding_pixels = kernelSize // 2

        image_padded = np.pad(grayScaleImage, ((padding_pixels, padding_pixels), (padding_pixels, padding_pixels)), 'constant')
        padded_h, padded_w = np.shape(image_padded)
        resulting = np.zeros((padded_h, padded_w), dtype=np.uint8)


        for row in range(padding_pixels, padded_h - padding_pixels):
            for col in range(padding_pixels, padded_w - padding_pixels):
                newPixel_val = np.amax(image_padded[row - padding_pixels:row + padding_pixels + 1, col - padding_pixels:col + padding_pixels + 1] +  kernel)
                if(newPixel_val > 255):
                    newPixel_val = 255
                resulting[row][col] = newPixel_val

        # finally we need to remove the extra padding and return the image data
        return resulting[padding_pixels:padded_h - padding_pixels, padding_pixels:padded_w - padding_pixels]


    def erotion(self, grayScaleImage, kernelSize, kernel_structure):
        # get kernel we need
        kernel = self.create_kernel_structure(kernelSize, kernel_structure)
        # add padding to the image
        padding_pixels = kernelSize // 2

        image_padded = np.pad(grayScaleImage, ((padding_pixels, padding_pixels), (padding_pixels, padding_pixels)), 'constant')
        padded_h, padded_w = np.shape(image_padded)
        resulting = np.zeros((padded_h, padded_w), dtype=np.uint8)

        for row in range(padding_pixels, padded_h - padding_pixels):
            for col in range(padding_pixels, padded_w - padding_pixels):
                newPixel_val = np.amin(np.subtract(image_padded[row - padding_pixels:row + padding_pixels + 1, col - padding_pixels:col + padding_pixels + 1], kernel))
                if(newPixel_val < 0):
                    newPixel_val = 0
                resulting[row][col] = newPixel_val

        # finally we need to remove the extra padding and return the image data
        return resulting[padding_pixels:padded_h - padding_pixels, padding_pixels:padded_w - padding_pixels]

    def opening(self, ImageData, kernelSize, kernel_structure):
        eroded = self.erotion(ImageData, kernelSize, kernel_structure)
        final = self.dilation(eroded, kernelSize, kernel_structure)

        return final

    def closing(self, ImageData, kernelSize, kernel_structure):
        dilated = self.dilation(ImageData, kernelSize, kernel_structure)
        final = self.erotion(dilated, kernelSize, kernel_structure)

        return final

    def perform_morphology(self, mode, color, kernelSize, kernel_Structure):
        if color is True:
            b, g, r = cv2.split(self.originalImage)
            if mode.lower() == "dilation":
                dilated_b = self.dilation(b, kernelSize, kernel_Structure)
                dilated_g = self.dilation(g, kernelSize, kernel_Structure)
                dilated_r = self.dilation(r, kernelSize, kernel_Structure)
                return cv2.merge((dilated_b, dilated_g, dilated_r))
            elif mode.lower() == "erotion":
                eroded_b = self.erotion(b, kernelSize, kernel_Structure)
                eroded_g = self.erotion(g, kernelSize, kernel_Structure)
                eroded_r = self.erotion(r, kernelSize, kernel_Structure)
                return cv2.merge((eroded_b, eroded_g, eroded_r))
            elif mode.lower() == "opening":
                open_b = self.opening(b, kernelSize, kernel_Structure)
                open_g = self.opening(g, kernelSize, kernel_Structure)
                open_r = self.opening(r, kernelSize, kernel_Structure)
                return cv2.merge((open_b, open_g, open_r))
            elif mode.lower() == "closing":
                close_b = self.closing(b, kernelSize, kernel_Structure)
                close_g = self.closing(g, kernelSize, kernel_Structure)
                close_r = self.closing(r, kernelSize, kernel_Structure)
                return cv2.merge((close_b, close_g, close_r))
        else: # b&k
            if mode.lower() == "dilation":
                return self.dilation(self.grayScaleImage, kernelSize, kernel_Structure)
            elif mode.lower() == "erotion":
                return  self.erotion(self.grayScaleImage, kernelSize, kernel_Structure)
            elif mode.lower() == "opening":
                return self.opening(self.grayScaleImage, kernelSize, kernel_Structure)
            elif mode.lower() == "closing":
                return self.closing(self.grayScaleImage, kernelSize, kernel_Structure)
