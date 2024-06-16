import keyboard as kb
import numpy as np
import random

from scripts.utils import probability_two


class Aim:
    def __init__(self, image):
        self.image_size = image.shape
        self._x = image.shape[0] // 2
        self._y = image.shape[1] // 2
        self.breath = 0
        self.scope_y_movement = 1

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        if 620 < new_x < self.image_size[1] - 620:
            self._x = new_x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        if 410 < new_y < self.image_size[1] - 410:
            self._y = new_y

    def move_aim(self, pixels_to_move) -> None:
        """
        moves the aim point according to player input
        Parameters
        ----------
        pixels_to_move [int]: how many pixels to move each frame
        Returns
        -------
        """
        if kb.is_pressed("w"):
            self.y -= pixels_to_move
        if kb.is_pressed("s"):
            self.y += pixels_to_move
        if kb.is_pressed("d"):
            self.x += pixels_to_move
        if kb.is_pressed("a"):
            self.x -= pixels_to_move

    def move_aim_breath(self) -> None:
        """
        when in scope, mimics the player breath
        Returns
        -------
        """
        # switch direction of breath
        if self.breath in [100, -100]:
            self.scope_y_movement = -np.sign(self.breath)
        # move scope up or down
        self.y += random.randrange(0, 2) * self.scope_y_movement
        # x have a 20 percent chance to move to each side randomly
        left, right = probability_two(0.2, 0.2)
        self.x = self.x - int(left) + int(right)
        # increase or decrease breath
        self.breath += self.scope_y_movement
