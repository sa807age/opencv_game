import cv2 as cv
from copy import deepcopy
from scripts.game_mechanics import move_aim

from scripts.utils import draw_image_on_image

if __name__ == '__main__':
    background_image = '../media/photos/big floppa.jpg'
    top_image = '../media/photos/scary_soldier2.webp'
    l_img = cv.imread(background_image, -1)
    s_img = cv.imread(top_image, -1)
    aim = [0, 0]
    while True:
        frame = deepcopy(l_img)
        aim = move_aim(aim, 'launcher')
        draw_image_on_image(frame, s_img, aim, 0.5)
        cv.imshow('image', frame)
        cv.waitKey(15)