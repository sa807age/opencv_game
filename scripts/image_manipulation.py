import math

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


def draw_image_on_image(main_image, image_to_draw, location, size):
    # new_image_shape = (math.ceil(image_to_draw.shape[1]*size)+10, math.ceil(image_to_draw.shape[0]*size)+10)
    # image_to_draw = cv.resize(image_to_draw, new_image_shape)
    # x_offset, y_offset = location[1] - image_to_draw.shape[1]//2, location[0] - image_to_draw.shape[0]//2
    # x_max = x_offset + image_to_draw.shape[1]
    # y_max = y_offset + image_to_draw.shape[0]
    # if x_offset < 0:
    #     if x_max > main_image.shape[1]:
    #         x_max = main_image.shape[1]
    #     image_to_draw = image_to_draw[-1*x_offset:x_max, :, :]
    #     x_offset = 0
    # if y_offset < 0:
    #     if y_offset > main_image.shape[0]:
    #         y_max = main_image.shape[0]
    #     image_to_draw = image_to_draw[:, -1*y_offset:y_max, :]
    #     y_offset = 0
    #     image_to_draw = image_to_draw[:, :y_max, :]
    # alpha_s = image_to_draw[:y_max, :x_max, 3] / 255.0
    # alpha_l = 1.0 - alpha_s
    # for c in range(0, 3):
    #     main_image[y_offset:y_max, x_offset:x_max, c] = \
    #         (alpha_s * image_to_draw[:y_max, :x_max, c] +
    #          alpha_l * main_image[y_offset:y_max, x_offset:x_max, c])

    if location[1] <= -image_to_draw.shape[1]:
        return None
    if location[0] <= -image_to_draw.shape[0]:
        return None
    if location[1] >= image_to_draw.shape[1]:
        return None
    if location[0] >= image_to_draw.shape[0]:
        return None

    up_trim = -location[1] if location[1] < 0 else 0
    left_trim = -location[0] if location[0] < 0 else 0
    down_trim = -location[1] if location[1] < 0 else 0gf
    right_trim = -location[0] if location[0] < 0 else 0

    main_image[location[1]+up_trim:image_to_draw.shape[1]+location[1]-2,
               location[0]+left_trim:image_to_draw.shape[0]+location[0], :] =\
        image_to_draw[0+up_trim:image_to_draw.shape[1], 0+left_trim:image_to_draw.shape[0], :3]
