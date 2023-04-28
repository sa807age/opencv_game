import cv2 as cv

from new_game.round_class import Round

round1_img_path = '../media/photos/pexels-david-bartus-1166209.jpg'
round1_img = cv.imread(round1_img_path)
round1 = Round(round1_img, 5, 5, 5)
round1.start_round()