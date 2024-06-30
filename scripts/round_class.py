import copy
import time
import random

import numpy as np
import cv2 as cv
import keyboard as kb

from scripts.aim import Aim
from scripts.utils import put_round_text, probability
from scripts.cut_scenes import you_won_animation, you_lose_animation
from scripts.weapons import Weapon
from scripts.zombies import Zombie
from scripts.time_and_score import TimeCountdown


class Round:
    def __init__(self, image, sniper_max_ammo, launcher_ammo, sniper_zoom, time, round_music, horizon_line,
                 spawn_chance, headers):
        self.original_image = image
        self.aim = Aim(image.shape)
        self.weapon = Weapon(sniper_max_ammo, launcher_ammo, sniper_zoom, self.aim)
        self.timer = TimeCountdown(time)
        self.round_music = round_music
        self.headers = headers
        self.horizon_line = horizon_line
        self.spawn_chance = spawn_chance

    def load_frame(self) -> [np.array, bool]:
        """
        create a not frame from current round data, when round is over, return true if won and false if not
        Returns
        -------
        """
        # move the aim location from input, also apply breathing movement when in sniper mode
        aim_move_speed = 5
        if self.weapon.current_weapon == 'sniper':
            self.aim.move_aim_breath()
            aim_move_speed = 5 // self.weapon.sniper_zoom
        self.aim.move_aim(aim_move_speed)
        # create a blank frame from image and aim location
        frame = copy.deepcopy(self.original_image[self.aim.y - 400:self.aim.y + 400,
                              self.aim.x - 600:self.aim.x + 600, :])
        # maybe add zombie
        if probability(self.spawn_chance):
            location = [random.randrange(600, self.original_image.shape[1] - 600),
                        self.horizon_line + random.randrange(-50, 50)]
            Zombie.add_zombie(location)
        # check if zombies got to player
        you_lose = Zombie.draw_zombies(frame, self.aim)
        if you_lose:
            you_lose_animation(frame)
            return False
        frame = self.weapon.update_frame(frame)
        times_up = self.timer.display_time(frame)
        if times_up:
            you_won_animation(frame)
            return True
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
                Zombie.kill_all()
                return frame
            cv.imshow('game', frame)
            cv.waitKey(5)

    def play_round(self):
        result = False
        while not result:
            result = self.start_round()


