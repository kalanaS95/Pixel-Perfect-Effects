from algorithms.utils import *
from numba import jit, cuda

@jit(nopython=True)
def color_negative(bgr_arr, b_threshold, g_threshold, r_threshold):
    new_bgr_arr = np.zeros(3, dtype=np.uint8)

    if (bgr_arr[0] < b_threshold):
        new_bgr_arr[0] = 255 - bgr_arr[0]
    else:
        new_bgr_arr[0] = bgr_arr[0]

    if (bgr_arr[1] < g_threshold):
        new_bgr_arr[1] = 255 - bgr_arr[1]
    else:
        new_bgr_arr[1] = bgr_arr[1]

    if (bgr_arr[2] < r_threshold):
        new_bgr_arr[2] = 255 - bgr_arr[2]
    else:
        new_bgr_arr[2] = bgr_arr[2]

    return new_bgr_arr


@jit(nopython=True)
def perform_solarization(originalImage, b_threshold, g_threshold, r_threshold):
    original_height, original_width, _ = np.shape(originalImage)
    # make a zero 2D array to store results
    solarized = np.zeros((original_height, original_width, 3), dtype=np.uint8)

    for row in range(original_height):
        for col in range(original_width):
            solarized[row][col] = color_negative(originalImage[row][col], b_threshold, g_threshold,
                                                      r_threshold)

    return solarized