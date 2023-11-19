import math
import os
import random
from operator import add

import cv2 as cv
import numpy as np

from scripts import sounds
from scripts.utils import check_rectangles_collision, rotate_vector

soldiers_death_sounds = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sounds',
                                        'death_sounds'))


class Enemy:
    def __init__(self, location, aim):
        self.frames_lived = 1
        self.aim = aim
        self.location = location
        self.relative_location = [600 - self.aim[0] + self.location[0], 400 - self.aim[1] + self.location[1]]
        self.arrow_color = (0, 0, 255)
        self.death_sound = None

    def update_relative_location(self):
        self.relative_location = [600 - self.aim[0] + self.location[0], 400 - self.aim[1] + self.location[1]]

    def kill(self, enemies_list: list):
        self.death_sound.play()
        enemies_list.remove(self)
        del self

    def show_arrow(self, frame):
        if not (600 > self.location[0] - self.aim[0] > -600 and 400 > self.location[1] - self.aim[1] > -400):
            direction_vector = np.array([self.location[0] - self.aim[0], self.location[1] - self.aim[1]])
            vector_size = np.linalg.norm(direction_vector)
            normalized_vector = (direction_vector/vector_size)
            arrow_point = [int((normalized_vector[0] * 550) + 600), int((normalized_vector[1] * 350) + 400)]
            rotated_vector1 = rotate_vector(normalized_vector, 135) * (1/math.sqrt(vector_size)) * 2000
            rotated_vector2 = rotate_vector(normalized_vector, -135) * (1/math.sqrt(vector_size)) * 2000
            cv.line(frame, arrow_point, [int(arrow_point[0]) + int(rotated_vector1[0]),
                                         int(arrow_point[1]) + int(rotated_vector1[1])],
                    self.arrow_color, 10)
            cv.line(frame, arrow_point, [int(arrow_point[0]) + int(rotated_vector2[0]),
                                         int(arrow_point[1]) + int(rotated_vector2[1])],
                    self.arrow_color, 10)


class Soldier(Enemy):
    def __init__(self, location, aim):
        super().__init__(location, aim)
        self.color = [random.randrange(0, 50), random.randrange(0, 255), random.randrange(0, 50)]
        self.size = (self.frames_lived**2) * 0.00001
        self.bbox = [math.ceil(self.location[0] - 10 * self.size),
                     math.ceil(self.location[1] - 20 * self.size),
                     math.ceil(20*self.size), math.ceil(40*self.size)]
        self.death_sound = sounds.death_sounds[random.randrange(0, 8)]
        self.arrow_color = (0, 255, 0)

    def update(self):
        if random.randrange(0, 5) == 4:
            self.location[0] += random.randrange(-1, 2)
            self.location[1] += random.randrange(-1, 2)
            self.location[1] += 1
        self.update_relative_location()
        self.frames_lived += 1
        self.size = (self.frames_lived**2) * 0.00001
        self.bbox = [math.ceil(self.location[0] - 10 * self.size),
                     math.ceil(self.location[1] - 20 * self.size),
                     math.ceil(20 * self.size), math.ceil(40 * self.size)]
        self.arrow_color = (0, int(255*(1600-self.frames_lived)/1600), int(255*self.frames_lived/1600))

    def draw_on_image(self, photo):
        cv.circle(photo, [int(self.relative_location[0]), int(self.relative_location[1] - math.ceil(10 * self.size))],
                  math.ceil(10*self.size), self.color, -1)
        # face
        cv.circle(photo, [self.relative_location[0] + math.ceil(5 * self.size),
                          self.relative_location[1] - math.ceil(10 * self.size)],
                  math.ceil(0.2*self.size), 0, -1)
        cv.circle(photo, [self.relative_location[0] - math.ceil(5 * self.size),
                          self.relative_location[1] - math.ceil(10 * self.size)],
                  math.ceil(0.2*self.size), 0, -1)
        # body
        cv.line(photo, [self.relative_location[0], self.relative_location[1]],
                [self.relative_location[0], self.relative_location[1] + math.ceil(10 * self.size)],
                self.color, math.ceil(1 + 1 * self.size))
        cv.line(photo, [self.relative_location[0], self.relative_location[1] + math.ceil(3 * self.size)],
                [self.relative_location[0] + math.ceil(10 * self.size), self.relative_location[1]],
                self.color, math.ceil(1 + 1 * self.size))
        cv.line(photo, [self.relative_location[0], self.relative_location[1] + math.ceil(3 * self.size)],
                [self.relative_location[0] - math.ceil(10 * self.size), self.relative_location[1]], self.color,
                math.ceil(1 + 1 * self.size))
        cv.line(photo, [self.relative_location[0], self.relative_location[1] + math.ceil(10 * self.size)],
                [self.relative_location[0] + math.ceil(7 * self.size),
                 self.relative_location[1] + math.ceil(20 * self.size)],
                self.color, math.ceil(1+1*self.size))
        cv.line(photo, [self.relative_location[0], self.relative_location[1] + math.ceil(10 * self.size)],
                [self.relative_location[0] - math.ceil(7 * self.size),
                 self.relative_location[1] + math.ceil(20 * self.size)],
                self.color, math.ceil(1+1*self.size))

        # bbox
        if self.frames_lived > 1400:
            cv.line(photo, [self.relative_location[0] - math.ceil(6 * self.size),
                            self.relative_location[1] - math.ceil(12.5 * self.size)],
                    [self.relative_location[0] - math.ceil(3.5 * self.size),
                     self.relative_location[1] - math.ceil(11.5 * self.size)], 0,
                    math.ceil(0.5 * self.size))

            cv.line(photo, [self.relative_location[0] + math.ceil(6 * self.size),
                            self.relative_location[1] - math.ceil(12.5 * self.size)],
                    [self.relative_location[0] + math.ceil(3.5 * self.size),
                     self.relative_location[1] - math.ceil(11.5 * self.size)], 0,
                    math.ceil(0.5 * self.size))

            cv.circle(photo, [self.relative_location[0], self.relative_location[1] - math.ceil(5 * self.size)],
                      math.ceil(2.5 * self.size), 0, -1)


class Enemies:
    def __init__(self, aim):
        self.enemies_list = []
        self.soldier_spawn_chance = 0
        self.aim = aim

    def add_soldier(self, location):
        self.enemies_list.append(Soldier([location[0], location[1]], self.aim))

    def update_frame(self, frame):
        health_down = False
        for enemy in self.enemies_list[::-1]:
            enemy.draw_on_image(frame)
            enemy.update()
            if isinstance(enemy, Soldier) and enemy.frames_lived == 1400:
                sounds.screaming.play()
            if isinstance(enemy, Soldier) and enemy.frames_lived > 1700:
                if enemy.frames_lived % 300 == 0:
                    health_down = True
        return health_down


