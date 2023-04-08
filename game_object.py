import cv2 as cv


class Game:
    def __init__(self, background_image_path):
        self.background_image = cv.imread(background_image_path)

