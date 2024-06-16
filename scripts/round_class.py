import copy
import time

import numpy as np
import cv2 as cv
import keyboard as kb
import random

from scripts.utils import put_round_text
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
            self.aim[1] -= pixels_to_move if self.aim[1] > 410 else 0
        if kb.is_pressed("s"):
            self.aim[1] += pixels_to_move if self.aim[1] < self.image_size[0] - 410 else 0
        if kb.is_pressed("d"):
            self.aim[0] += pixels_to_move if self.aim[0] < self.image_size[1] - 620 else 0
        if kb.is_pressed("a"):
            self.aim[0] -= pixels_to_move if self.aim[0] > 620 else 0

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
        if self.image_size[0] - 410 > self.aim[1] > 410:
            self.aim[1] += random.randrange(0, 2) * self.scope_y_movement
        # x have a 20 percent chance to move to each side randomly
        scope_x_movement = random.randrange(-1, 4)//3
        if 620 < self.aim[0] < self.image_size[1] - 620:
            self.aim[0] += scope_x_movement
        # increase or decrease breath
        self.breath += self.scope_y_movement

    def load_frame(self) -> np.array | bool:
        """
        create a not frame from current round data, when round is over, return true if won and false if not
        Returns
        -------
        """
        # move the aim location from input, also apply breathing movement when in sniper mode
        aim_move_speed = 5
        if self.weapon.current_weapon == 'sniper':
            self.move_aim_breath()
            aim_move_speed = 5 // self.weapon.sniper_zoom
        self.move_aim(aim_move_speed)
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

    def round_intro(self):
        # start round music
        if self.round_music:
            self.round_music.play()
        counter = time.perf_counter()
        # play the game with text for 4 seconds
        while time.perf_counter()-counter < 4:
            if kb.is_pressed('esc'):
                quit()
            frame = self.load_frame()
            put_round_text(frame, self.headers[0], self.headers[1])
            cv.imshow('game', frame)
            cv.waitKey(5)

    def start_round(self):
        self.round_intro()
        while True:
            if kb.is_pressed('esc'):
                quit()
            frame = self.load_frame()
            # if frame is not np.Array: that means that the game is over
            if isinstance(frame, bool):
                return frame
            cv.imshow('game', frame)
            cv.waitKey(5)

    def play_round(self):
        result = False
        while not result:
            result = self.start_round()


