import math
import os
import random

import cv2 as cv
import numpy as np

from scripts.sounds import SoundManager
from scripts.utils import rotate_vector, probability

soldiers_death_sounds = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sounds',
                                                     'death_sounds'))


class Zombie:
    zombies = []

    def __init__(self, location: list):
        """
        Initializes a Zombie instance.

        Parameters
        ----------
        location : list
            The initial location of the zombie.
        """
        self.frames_lived = 1
        self.location = location
        self.color = [random.randrange(0, 50), random.randrange(0, 255), random.randrange(0, 50)]
        self.size = (self.frames_lived ** 2) * 0.00001

    @staticmethod
    def kill_all():
        """
        Kills all zombies by clearing the zombies list.
        """
        Zombie.zombies = []

    @staticmethod
    def add_zombie(location: list):
        """
        Adds a new zombie at the specified location.

        Parameters
        ----------
        location : list
            The location to add the new zombie.
        """
        Zombie.zombies.append(Zombie(location))

    @staticmethod
    def draw_zombies(frame, aim):
        """
        Draws all zombies on the given frame and updates their state.

        Parameters
        ----------
        frame : np.ndarray
            The frame to draw zombies on.
        aim : Aim
            The aim object for relative positioning.

        Returns
        -------
        bool
            True if any zombie's frames_lived exceed 2000, else False.
        """
        for zombie in Zombie.zombies[::-1]:
            zombie.draw_on_image(frame, aim)
            if zombie.update():
                return True

    def location_to_relative(self, aim):
        """
        Converts the zombie's absolute location to a location relative to the aim.

        Parameters
        ----------
        aim : Aim
            The aim object for relative positioning.

        Returns
        -------
        list
            The relative location.
        """
        return [int(600 - aim.x + self.location[0]), int(400 - aim.y + self.location[1])]

    def kill(self):
        """
        Plays a random death sound and removes the zombie from the zombies list.
        """
        SoundManager.death_sounds[random.randrange(0, 8)].play()
        self.zombies.remove(self)
        del self

    def get_bbox(self):
        """
        Gets the bounding box of the zombie.

        Returns
        -------
        list
            The bounding box coordinates and size.
        """
        return [math.ceil(self.location[0] - 10 * self.size), math.ceil(self.location[1] - 20 * self.size),
                math.ceil(20 * self.size), math.ceil(40 * self.size)]

    def draw_arrow(self, frame, aim):
        """
        Draws an arrow pointing towards the zombie on the frame.

        Parameters
        ----------
        frame : np.ndarray
            The frame to draw the arrow on.
        aim : Aim
            The aim object for relative positioning.
        """
        arrow_color = (0, int(255 * (1600 - self.frames_lived) / 1600), int(255 * self.frames_lived / 1600))
        direction_vector = np.array([self.location[0] - aim.x, self.location[1] - aim.y])
        vector_size = np.linalg.norm(direction_vector)
        normalized_vector = (direction_vector / vector_size)
        arrow_point = [int((normalized_vector[0] * 550) + 600), int((normalized_vector[1] * 350) + 400)]
        rotated_vector1 = rotate_vector(normalized_vector, 135) * (1 / math.sqrt(vector_size)) * 2000
        rotated_vector2 = rotate_vector(normalized_vector, -135) * (1 / math.sqrt(vector_size)) * 2000
        cv.line(frame, arrow_point, [int(arrow_point[0]) + int(rotated_vector1[0]),
                                     int(arrow_point[1]) + int(rotated_vector1[1])],
                arrow_color, 10)
        cv.line(frame, arrow_point, [int(arrow_point[0]) + int(rotated_vector2[0]),
                                     int(arrow_point[1]) + int(rotated_vector2[1])],
                arrow_color, 10)

    def update(self):
        """
        Updates the zombie's location and state.

        Returns
        -------
        bool
            True if frames_lived exceeds 2000, else False.
        """
        if probability(0.5):
            self.location[0] += random.randrange(-1, 2)
        self.location[1] += 0.12
        self.frames_lived += 1
        self.size = (1.0017 ** self.frames_lived)
        if self.frames_lived == 1400:
            SoundManager.screaming.play()
        if self.frames_lived > 2000:
            return True
        return False

    def draw_on_image(self, photo: np.ndarray, aim):
        """
        Draws the zombie on the given photo frame.

        Parameters
        ----------
        photo : np.ndarray
            The photo frame to draw on.
        aim : Aim
            The aim object for relative positioning.
        """
        relative_location = list(self.location_to_relative(aim))
        self.draw_body(photo, relative_location)
        self.draw_face(photo, relative_location)
        if self.frames_lived > 1400:
            self.draw_angry_face(photo, relative_location)
        if not (600 > self.location[0] - aim.x > -600 and 400 > self.location[1] - aim.y > -400):
            self.draw_arrow(photo, aim)

    def draw_angry_face(self, photo, relative_location: list):
        """
        Draws an angry face on the zombie.

        Parameters
        ----------
        photo : np.ndarray
            The photo frame to draw on.
        relative_location : list
            The relative location of the zombie.
        """
        # eyebrows
        cv.line(photo, [relative_location[0] - math.ceil(6 * self.size),
                        relative_location[1] - math.ceil(12.5 * self.size)],
                [relative_location[0] - math.ceil(3.5 * self.size),
                 relative_location[1] - math.ceil(11.5 * self.size)], [0, 0, 0], math.ceil(0.5 * self.size))
        cv.line(photo, [relative_location[0] + math.ceil(6 * self.size),
                        relative_location[1] - math.ceil(12.5 * self.size)],
                [relative_location[0] + math.ceil(3.5 * self.size),
                 relative_location[1] - math.ceil(11.5 * self.size)], [0, 0, 0], math.ceil(0.5 * self.size))
        # mouth
        cv.circle(photo, [relative_location[0], relative_location[1] - math.ceil(5 * self.size)],
                  math.ceil(2.5 * self.size), [0, 0, 0], -1)

    def draw_body(self, photo, relative_location: list):
        """
        Draws the zombie's body on the photo.

        Parameters
        ----------
        photo : np.ndarray
            The photo frame to draw on.
        relative_location : list
            The relative location of the zombie.
        """
        cv.circle(photo, [int(relative_location[0]), int(relative_location[1] - math.ceil(10 * self.size))],
                  math.ceil(10 * self.size), self.color, -1)
        cv.line(photo, [relative_location[0], relative_location[1]],
                [relative_location[0], relative_location[1] + math.ceil(10 * self.size)], self.color,
                math.ceil(1 + 1 * self.size))
        cv.line(photo, [relative_location[0], relative_location[1] + math.ceil(3 * self.size)],
                [relative_location[0] + math.ceil(10 * self.size), relative_location[1]],
                self.color, math.ceil(1 + 1 * self.size))
        cv.line(photo, [relative_location[0], relative_location[1] + math.ceil(3 * self.size)],
                [relative_location[0] - math.ceil(10 * self.size), relative_location[1]], self.color,
                math.ceil(1 + 1 * self.size))
        cv.line(photo, [relative_location[0], relative_location[1] + math.ceil(10 * self.size)],
                [relative_location[0] + math.ceil(7 * self.size),
                 relative_location[1] + math.ceil(20 * self.size)],
                self.color, math.ceil(1 + 1 * self.size))
        cv.line(photo, [relative_location[0], relative_location[1] + math.ceil(10 * self.size)],
                [relative_location[0] - math.ceil(7 * self.size),
                 relative_location[1] + math.ceil(20 * self.size)],
                self.color, math.ceil(1 + 1 * self.size))

    def draw_face(self, photo, relative_location: list):
        """
        Draws the zombie's face on the photo.

        Parameters
        ----------
        photo : np.ndarray
            The photo frame to draw on.
        relative_location : list
            The relative location of the zombie.
        """
        # eyes
        cv.circle(photo,
                  [relative_location[0] + math.ceil(5 * self.size), relative_location[1] - math.ceil(10 * self.size)],
                  math.ceil(0.2 * self.size), [0, 0, 0], -1)
        cv.circle(photo,
                  [relative_location[0] - math.ceil(5 * self.size), relative_location[1] - math.ceil(10 * self.size)],
                  math.ceil(0.2 * self.size), [0, 0, 0], -1)
