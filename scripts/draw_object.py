import numpy as np
import cv2 as cv


def create_sniper_mask():
    mask_size = 300
    mask_center = (600, 400)
    blank_image = np.zeros((800, 1200), dtype=np.uint8)
    sniper_mask = cv.circle(blank_image, mask_center, mask_size, 255, -1)
    return sniper_mask


def draw_scope_lines(image):
    line_color = (0, 0, 0)
    cv.line(image, (400, 400), (800, 400), line_color, 1, cv.LINE_AA)
    cv.line(image, (600, 300), (600, 800), line_color, 1, cv.LINE_AA)
