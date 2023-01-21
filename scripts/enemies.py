import random
import os
import cv2 as cv
import math
from scripts import sounds
from operator import add
from screens.cut_scenes import game_over
from scripts.utils import check_rectangles_collision


soldiers_death_sounds = sounds_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sounds',
                                                                     'death_sounds'))


class Soldier:
    def __init__(self, location):
        self.frames_lived = 1
        self.x_location = int(location[0])
        self.y_location = int(location[1])
        self.color = [random.randrange(0, 50), random.randrange(0, 255), random.randrange(0, 50)]
        self.size = (self.frames_lived*0.005)**2
        self.bbox = [math.ceil(self.x_location-10*self.size), math.ceil(self.y_location-20*self.size),
                     math.ceil(20*self.size), math.ceil(40*self.size)]

    def update(self):
        self.x_location += random.randrange(-1, 2)
        self.y_location += random.randrange(-1, 2)
        if random.randrange(0, 5) == 4:
            if self.frames_lived < 300:
                self.y_location += 1
            else:
                self.y_location -= 1
        self.frames_lived += 1
        self.size = (self.frames_lived * 0.005) ** 2
        self.bbox = [math.ceil(self.x_location - 10 * self.size),
                     math.ceil(self.y_location - 20 * self.size),
                     math.ceil(20 * self.size), math.ceil(40 * self.size)]

    def draw_on_image(self, photo):
        # head
        cv.circle(photo, [self.x_location, self.y_location - math.ceil(10*self.size)],
                  math.ceil(10*self.size), self.color, -1)
        # face
        cv.circle(photo, [self.x_location + math.ceil(5*self.size), self.y_location - math.ceil(10*self.size)],
                  math.ceil(0.2*self.size), 0, -1)
        cv.circle(photo, [self.x_location - math.ceil(5*self.size), self.y_location - math.ceil(10*self.size)],
                  math.ceil(0.2*self.size), 0, -1)
        # body
        cv.line(photo, [self.x_location, self.y_location],
                [self.x_location, self.y_location + math.ceil(10*self.size)], self.color, math.ceil(1+1*self.size))
        cv.line(photo, [self.x_location, self.y_location + math.ceil(3*self.size)],
                [self.x_location + math.ceil(10*self.size), self.y_location], self.color, math.ceil(1+1*self.size))
        cv.line(photo, [self.x_location, self.y_location + math.ceil(3*self.size)],
                [self.x_location - math.ceil(10*self.size), self.y_location], self.color, math.ceil(1+1*self.size))
        cv.line(photo, [self.x_location, self.y_location + math.ceil(10*self.size)],
                [self.x_location + math.ceil(7*self.size), self.y_location + math.ceil(20*self.size)],
                self.color, math.ceil(1+1*self.size))
        cv.line(photo, [self.x_location, self.y_location + math.ceil(10*self.size)],
                [self.x_location - math.ceil(7*self.size), self.y_location + math.ceil(20*self.size)],
                self.color, math.ceil(1+1*self.size))
        # gun
        cv.line(photo, [self.x_location - math.ceil(10*self.size), self.y_location],
                [self.x_location - math.ceil(10*self.size), self.y_location], (0, 0, 0), math.ceil(1+1*self.size))
        # bbox
        if self.frames_lived > 550:
            cv.rectangle(photo, self.bbox[0:2], list(map(add, self.bbox[0:2], self.bbox[2:4])), 0, 1)

            cv.line(photo, [self.x_location - math.ceil(6 * self.size), self.y_location - math.ceil(12.5 * self.size)],
                    [self.x_location - math.ceil(3.5 * self.size), self.y_location - math.ceil(11.5 * self.size)], 0,
                    math.ceil(0.5 * self.size))

            cv.line(photo, [self.x_location + math.ceil(6 * self.size), self.y_location - math.ceil(12.5 * self.size)],
                    [self.x_location + math.ceil(3.5 * self.size), self.y_location - math.ceil(11.5 * self.size)], 0,
                    math.ceil(0.5 * self.size))

            cv.circle(photo, [self.x_location, self.y_location - math.ceil(5 * self.size)],
                      math.ceil(2.5 * self.size), 0, -1)

    def kill(self, soldiers_list: list):
        sounds.death_sounds[random.randrange(0, 8)].play()
        soldiers_list.remove(self)
        del self


class Enemies:
    def __init__(self):
        self.soldiers_list = []
        self.soldier_spawn_chance = 0

    def add_soldier(self, location):
        self.soldiers_list.append(Soldier([location[0], location[1]]))

    def display_all_soldiers(self, image):
        end_game = False
        for soldier in self.soldiers_list[::-1]:
            soldier.draw_on_image(image)
            soldier.update()

            if soldier.frames_lived == 550:
                sounds.screaming.play()
            if soldier.frames_lived == 650:
                end_game = True
        if end_game:
            game_over(image)

    def try_to_kill(self, point_or_bbox):
        if len(point_or_bbox) == 2:
            for soldier in self.soldiers_list:
                if soldier.bbox[0] < point_or_bbox[0] < soldier.bbox[0] + soldier.bbox[2] and soldier.bbox[1] <\
                        point_or_bbox[1] < soldier.bbox[1] + soldier.bbox[3]:
                    soldier.kill(self.soldiers_list)
                    break
        else:
            for soldier in self.soldiers_list:
                if check_rectangles_collision(soldier.bbox, point_or_bbox):
                    soldier.kill(self.soldiers_list)
                    break
