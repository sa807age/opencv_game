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
    if size != 1:
        image_to_draw = cv.resize(image_to_draw, (math.ceil(image_to_draw.shape[1]*size),
                                                  math.ceil(image_to_draw.shape[0]*size)))
    aim_x = location[0] - image_to_draw.shape[1]//2
    aim_y = location[1] - image_to_draw.shape[0]//2

    if aim_x <= -image_to_draw.shape[1]:
        return None
    if aim_y <= -image_to_draw.shape[0]:
        return None
    if aim_x >= main_image.shape[1]:
        return None
    if aim_y >= main_image.shape[0]:
        return None

    up_trim = -aim_y if aim_y < 0 else 0
    left_trim = -aim_x if aim_x < 0 else 0

    right_trim = 0
    main_right_location = image_to_draw.shape[1]+aim_x
    if main_right_location > main_image.shape[1]:
        right_trim = main_right_location - main_image.shape[1]
        main_right_location = main_image.shape[1]

    down_trim = 0
    main_down_location = image_to_draw.shape[0]+aim_y
    if main_down_location > main_image.shape[0]:
        down_trim = main_down_location - main_image.shape[0]
        main_down_location = main_image.shape[0]

    main_left_location = aim_x + left_trim
    main_up_location = aim_y + up_trim

    second_left_location = left_trim
    second_up_location = up_trim
    second_right_location = image_to_draw.shape[1] - right_trim
    second_down_location = image_to_draw.shape[0] - down_trim

    part_to_draw = image_to_draw[second_up_location:second_down_location, second_left_location:second_right_location,
                   :]

    alpha_part = np.stack((part_to_draw[:, :, 3] / 255,)*3, axis=-1)
    alpha_part_negative = 1 - alpha_part

    main_image[main_up_location:main_down_location, main_left_location:main_right_location, :] = \
        (part_to_draw[:, :, :3]*alpha_part +
         main_image[main_up_location:main_down_location, main_left_location:main_right_location, :] * alpha_part_negative)
