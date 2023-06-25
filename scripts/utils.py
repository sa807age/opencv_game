import math
from copy import copy
import cv2 as cv
import numpy as np


def check_rectangles_collision(bbox1, bbox2):
    bbox2_points = ((bbox2[0], bbox2[1]), (bbox2[0]+bbox2[2], bbox2[1]), (bbox2[0], bbox2[1]+bbox2[3]),
                    (bbox2[0]+bbox2[2], bbox2[1]+bbox2[3]))
    for point in bbox2_points:
        if bbox1[0] < point[0] < bbox1[0]+bbox1[2] and bbox1[1] < point[1] < bbox1[1]+bbox1[3]:
            return True


def waste_time(frame, soldiers, time_to_waste):
    for i in range(int(time_to_waste*1000//20)):
        new_frame = copy(frame)
        soldiers.display_all_soldiers(new_frame)
        cv.imshow("game", new_frame)
        cv.waitKey(20)


def kill_with_mouse(event, x, y, flags, soldiers):
    if event == cv.EVENT_LBUTTONDOWN:
        soldiers.try_to_hit([x, y])


def rotate_vector(vector, angle):
    # Convert angle to radians
    angle = np.deg2rad(angle)

    # Create rotation matrix
    rot_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

    # Rotate vector
    rotated_vector = np.dot(rot_matrix, vector)
    return rotated_vector


def resize_image(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def translate_image(image, right_movement, down_movement, output_dimansions):
    transmat = np.float32([[1, 0, right_movement], [0, 1, down_movement]])
    return cv.warpAffine(image, transmat, output_dimansions)


def draw_image_on_image(main_image, image_to_draw, location, size=1):
    if size != 1:
        image_to_draw = cv.resize(image_to_draw, (math.ceil(image_to_draw.shape[1]*size),
                                                  math.ceil(image_to_draw.shape[0]*size)))
    aim_x = location[0] - image_to_draw.shape[1]//2
    aim_y = location[1] - image_to_draw.shape[0]//2

    mask = np.zeros([*main_image.shape[:2]], np.uint8)
    blank_image = np.zeros([*main_image.shape[:2], 3], np.uint8)

    if aim_x + image_to_draw.shape[1] <= 0 or aim_x >= main_image.shape[1]:
        return None
    if aim_y + image_to_draw.shape[0] <= 0 or aim_y >= main_image.shape[0]:
        return None

    up_trim = -min(aim_y, 0)
    left_trim = -min(aim_x, 0)

    main_right_location = min(image_to_draw.shape[1]+aim_x, main_image.shape[1])
    right_trim = max(main_right_location - main_image.shape[1], 0)

    main_down_location = min(image_to_draw.shape[0]+aim_y, main_image.shape[0])
    down_trim = max(main_down_location - main_image.shape[0], 0)

    main_left_location = aim_x + left_trim
    main_up_location = aim_y + up_trim

    second_left_location = left_trim
    second_up_location = up_trim
    second_right_location = image_to_draw.shape[1] - right_trim
    second_down_location = image_to_draw.shape[0] - down_trim

    part_to_draw = image_to_draw[second_up_location:second_down_location, second_left_location:second_right_location, :]
    mask[main_up_location:main_down_location, main_left_location:main_right_location] = part_to_draw[:, :, 3]
    mask = (mask == 255)
    blank_image[main_up_location:main_down_location, main_left_location:main_right_location] = part_to_draw[:, :, :3]

    main_image[mask] = blank_image[mask]
    return True
