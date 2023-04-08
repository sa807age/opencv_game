import random
from copy import copy
import cv2 as cv
from scripts.image_manipulation import draw_image_on_image


class Heart:
    all_hearts = []
    image = cv.imread('kindpng_5455794.png', -1)

    def __init__(self):
        self.x_location = random.randrange(-50, 1000)
        self.y_location = 1000
        self.size = random.random() / 3
        self.is_alive = True
        Heart.all_hearts.append(self)

    def update(self):
        self.x_location += random.randrange(-2, 3)
        self.y_location += random.randrange(-10, 0)

    def kill(self):
        Heart.all_hearts.remove(self)
        del self
        print("OUCH!!")

    def draw_on_image(self, photo):
        if not draw_image_on_image(photo, Heart.image, (self.x_location, self.y_location), self.size):
            self.is_alive = False

    @classmethod
    def display_all_hearts(cls, img):
        for heart in cls.all_hearts:
            if not heart.is_alive:
                heart.kill()
        for heart in cls.all_hearts:
            heart.draw_on_image(img)
            heart.update()

    @staticmethod
    def create_heart():
        return Heart()


image = cv.imread('maayan.jpg')
cv.putText(image, 'I Love', (100, 200), 5, 10, (0, 0, 255), 3)
cv.putText(image, 'Maayan!!', (100, 500), 5, 10, (0, 0, 255), 3)
while True:
    frame = copy(image)
    if random.randrange(0, 40) == 1:
        Heart.create_heart()
    Heart.display_all_hearts(frame)
    cv.imshow('image', frame)
    cv.waitKey(1)
