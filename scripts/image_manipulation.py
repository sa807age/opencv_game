import cv2 as cv
import numpy as np


def resize_image(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def translate_image(image, right_movement, down_movement, output_dimansions):
    transmat = np.float32([[1, 0, right_movement], [0, 1, down_movement]])
    return cv.warpAffine(image, transmat, output_dimansions)


def create_blank_image(image_dimensions):
    return np.zeros((image_dimensions[0], image_dimensions[1]), dtype="uint8")
