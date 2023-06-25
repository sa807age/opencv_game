import time

import cv2 as cv

from scripts.round_class import Round
from scripts.cut_scenes import welcome_screen
from scripts.sounds import worms_music

welcome_screen()


round1_img_path = 'media/photos/pexels-david-bartus-1166209.jpg'
round1_img = cv.imread(round1_img_path)
while True:
    time.sleep(0.3)
    round1 = Round(round1_img, 5, 5, 2, 120, worms_music, 2500, 1/400)
    if round1.start_round():
        break
