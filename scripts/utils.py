import cv2 as cv
import numpy as np
from random import random
import math


def rotate_vector(vector, angle):
    """
    Rotate a 2D vector by a given angle in degrees.

    Parameters
    ----------
    vector : array_like
        A 2D vector to be rotated.
    angle : float
        The angle in degrees to rotate the vector.

    # Rotate vector
    rotated_vector = np.dot(rot_matrix, vector)
    return rotated_vector
    Returns
    -------
    ndarray
        The rotated vector.
    """


def draw_image_on_image(main_image, image_to_draw, location, size=1):
    """
    Draw an image on another image at a specified location and size.

    Parameters
    ----------
    main_image : ndarray
        The main image on which the other image will be drawn.
    image_to_draw : ndarray
        The image to be drawn on the main image.
    location : tuple
        The (x, y) coordinates where the image will be drawn.
    size : float, optional
        The scaling factor for resizing the image to draw (default is 1).

    Returns
    -------
    bool or None
        Returns True if the image was successfully drawn, None otherwise.
    """
    if size != 1:
        image_to_draw = cv.resize(image_to_draw, (math.ceil(image_to_draw.shape[1] * size),
                                                  math.ceil(image_to_draw.shape[0] * size)))
    aim_x = location[0] - image_to_draw.shape[1] // 2
    aim_y = location[1] - image_to_draw.shape[0] // 2

    if aim_x + image_to_draw.shape[1] <= 0 or aim_x >= main_image.shape[1]:
        return None
    if aim_y + image_to_draw.shape[0] <= 0 or aim_y >= main_image.shape[0]:
        return None

    up_trim = -min(aim_y, 0)
    left_trim = -min(aim_x, 0)

    main_right_location = min(image_to_draw.shape[1] + aim_x, main_image.shape[1])
    right_trim = max(main_right_location - main_image.shape[1], 0)

    main_down_location = min(image_to_draw.shape[0] + aim_y, main_image.shape[0])
    down_trim = max(main_down_location - main_image.shape[0], 0)

    main_left_location = aim_x + left_trim
    main_up_location = aim_y + up_trim

    second_left_location = left_trim
    second_up_location = up_trim
    second_right_location = image_to_draw.shape[1] - right_trim
    second_down_location = image_to_draw.shape[0] - down_trim

    part_to_draw = image_to_draw[second_up_location:second_down_location, second_left_location:second_right_location, :]
    mask = part_to_draw[:, :, 3] > 100  # Check if alpha channel is non-zero
    mask = np.expand_dims(mask, axis=2)
    mask = np.repeat(mask, 3, axis=2)
    main_part = main_image[main_up_location:main_down_location, main_left_location:main_right_location]

    main_part[mask] = part_to_draw[:, :, :3][mask]
    return True


def put_round_text(frame, big_text, small_text):
    """
    Put round text at the center of the frame.

    Parameters
    ----------
    frame : ndarray
        The image frame on which the text will be put.
    big_text : str
        The main text to be displayed.
    small_text : str
        The secondary text to be displayed below the main text.
    """
    header_position = (frame.shape[1] // 2, frame.shape[0] // 2)
    cv.putText(frame, big_text, (header_position[0] - 150, header_position[1] - 200),
               5, 3, (150, 150, 150), 3)
    cv.putText(frame, small_text, (header_position[0] - 150, header_position[1] - 100),
               5, 2, (100, 100, 100), 3)


def probability(prob):
    """
    Returns True with a probability of 'prob'.

    Parameters
    ----------
    prob : float
        The probability threshold.

    Returns
    -------
    bool
        True if the random number is less than 'prob', False otherwise.
    """
    return random() < prob


def probability_two(prob1, prob2):
    """
    Returns two booleans with probabilities 'prob1' and 'prob2'.

    Parameters
    ----------
    prob1 : float
        The probability threshold for the first boolean.
    prob2 : float
        The probability threshold for the second boolean.

    Returns
    -------
    tuple of bool
        A tuple containing two booleans.
    """
    result = random()
    return result < prob1, prob1 < result < prob1 + prob2

