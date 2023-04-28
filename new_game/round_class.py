import copy
import cv2 as cv
import keyboard as kb
import random
from new_game.weapons import Weapon
from new_game.enemies import Enemies


class Round:
    def __init__(self, image, sniper_max_ammo, launcher_ammo, sniper_zoom):
        self.original_image = image
        self.image_size = (self.original_image.shape[:2])
        self.aim = [self.original_image.shape[0]//2, self.original_image.shape[1]//2]
        self.enemies = Enemies(self.aim)
        self.particles = None
        self.breath = 0
        self.scope_y_movement = 1
        self.weapon = Weapon(sniper_max_ammo, launcher_ammo, sniper_zoom, self.aim, self.enemies.enemies_list)

    def move_aim(self, pixels_to_move):
        if kb.is_pressed("w"):
            self.aim[1] -= pixels_to_move if self.aim[1] > 510 else 0
        if kb.is_pressed("s"):
            self.aim[1] += pixels_to_move if self.aim[1] < self.image_size[0] - 510 else 0
        if kb.is_pressed("d"):
            self.aim[0] += pixels_to_move if self.aim[0] < self.image_size[1] - 510 else 0
        if kb.is_pressed("a"):
            self.aim[0] -= pixels_to_move if self.aim[0] > 510 else 0

    def move_aim_breath(self):
        if self.breath > 100:
            self.scope_y_movement = -1
        if self.breath < 0:
            self.scope_y_movement = 1

        self.aim[1] += random.randrange(0, 2) * self.scope_y_movement

        scope_x_movement = random.randrange(1, 6)
        if scope_x_movement == 4:
            self.aim[0] += 1
        if scope_x_movement == 5:
            self.aim[0] -= 1

        self.breath += self.scope_y_movement

    def start_round(self):
        health = 5
        while True:
            if kb.is_pressed('c'):
                break
            if self.weapon.current_weapon == 'sniper':
                self.move_aim_breath()
                self.move_aim(10//self.weapon.sniper_zoom)
            else:
                self.move_aim(10)
            frame = copy.copy(self.original_image[self.aim[1]-500:self.aim[1]+500, self.aim[0]-500:self.aim[0]+500, :])
            if random.randrange(0, 400) == 0:
                self.enemies.add_soldier([self.original_image.shape[0]//2, self.original_image.shape[1]//2])
            health_down = self.enemies.update_frame(frame)
            if health_down:
                health -= 1
            frame = self.weapon.update_frame(frame)
            cv.imshow('game', frame)
            cv.waitKey(5)
