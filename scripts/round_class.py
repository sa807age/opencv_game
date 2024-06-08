import copy
import cv2 as cv
import keyboard as kb
import random

import numpy as np

from scripts.cut_scenes import you_won_animation, you_lose_animation
from scripts.weapons import Weapon
from scripts.enemies import Enemies
from scripts.time_and_score import TimeCountdown


class Round:
    def __init__(self, image, sniper_max_ammo, launcher_ammo, sniper_zoom, time, round_music, horizon_line,
                 soldier_spawn_rate, headers):
        self.original_image = image
        self.image_size = (self.original_image.shape[:2])
        self.aim = [self.original_image.shape[0] // 2, self.original_image.shape[1] // 2]
        self.enemies = Enemies(self.aim)
        self.particles = None
        self.breath = 0
        self.scope_y_movement = 1
        self.weapon = Weapon(sniper_max_ammo, launcher_ammo, sniper_zoom, self.aim, self.enemies.enemies_list)
        self.timer = TimeCountdown(time)
        self.round_music = round_music
        self.horizon_line = horizon_line
        self.soldier_spawn_rate = soldier_spawn_rate
        self.headers = headers

    def move_aim(self, pixels_to_move):
        if kb.is_pressed("w"):
            self.aim[1] -= pixels_to_move if self.aim[1] > 410 else 0
        if kb.is_pressed("s"):
            self.aim[1] += pixels_to_move if self.aim[1] < self.image_size[0] - 410 else 0
        if kb.is_pressed("d"):
            self.aim[0] += pixels_to_move if self.aim[0] < self.image_size[1] - 620 else 0
        if kb.is_pressed("a"):
            self.aim[0] -= pixels_to_move if self.aim[0] > 620 else 0

    def move_aim_breath(self):
        if self.breath > 100:
            self.scope_y_movement = -1
        if self.breath < 0:
            self.scope_y_movement = 1

        if self.image_size[0] - 410 > self.aim[1] > 410:
            self.aim[1] += random.randrange(0, 2) * self.scope_y_movement

        scope_x_movement = random.randrange(1, 6)
        if scope_x_movement == 4:
            self.aim[0] += 1 if self.aim[0] < self.image_size[1] - 620 else 0
        if scope_x_movement == 5:
            self.aim[0] -= 1 if self.aim[0] > 620 else 0

        self.breath += self.scope_y_movement

    def load_frame(self):
        if self.weapon.current_weapon == 'sniper':
            self.move_aim_breath()
            self.move_aim(5 // self.weapon.sniper_zoom)
        else:
            self.move_aim(5)
        frame = copy.deepcopy(self.original_image[self.aim[1] - 400:self.aim[1] + 400,
                              self.aim[0] - 600:self.aim[0] + 600, :])
        if random.randrange(0, int(1 / self.soldier_spawn_rate)) == 0:
            self.enemies.add_soldier([random.randrange(600, self.original_image.shape[1] - 600),
                                      random.randrange(self.horizon_line - 100, self.horizon_line + 100)])
        you_lose = self.enemies.update_frame(frame)
        if you_lose:
            if you_lose_animation(frame):
                return False
            quit()
        frame = self.weapon.update_frame(frame)
        you_won = self.timer.display_time(frame)
        if you_won:
            if you_won_animation(frame):
                return True
            quit()
        for enemy in self.enemies.enemies_list:
            enemy.show_arrow(frame)

        return frame

    def start_round(self):
        index = 0
        if self.round_music:
            self.round_music.play()
        while True:
            if kb.is_pressed('esc'):
                quit()
            frame = self.load_frame()
            if frame is True:
                return True
            if frame is False:
                return False
            if index < 200:
                header_position = (frame.shape[1] // 2, frame.shape[0] // 2)
                cv.putText(frame, self.headers[0], (header_position[0] - 150, header_position[1] - 200), 5, 3,
                           (150, 150, 150), 3)
                cv.putText(frame, self.headers[1], (header_position[0] - 150, header_position[1] - 100), 5, 2,
                           (100, 100, 100), 3)
                index += 1

            cv.imshow('game', frame)
            cv.waitKey(5)
