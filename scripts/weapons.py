import random

import keyboard as kb
import numpy as np
import cv2 as cv

from scripts import sounds


class Weapon:
    def __init__(self, sniper_max_ammo, launcher_ammo, sniper_zoom, aim, enemies_list):
        self.current_weapon = 'launcher'
        self.sniper_max_ammo = sniper_max_ammo
        self.sniper_ammo = sniper_max_ammo
        self.launcher_ammo = launcher_ammo
        self.animation_index = None
        self.status = 'launcher'
        self.sniper_zoom = sniper_zoom
        self.aim = aim
        self.enemies_list = enemies_list

    def update_frame(self, frame):
        if self.current_weapon == 'sniper':
            frame = self.update_sniper(frame)
        elif self.current_weapon == 'launcher':
            frame = self.update_launcher(frame)
        elif self.current_weapon == 'reloading':
            if self.status == 'scope':
                frame = self.scope_zoom_out(frame)
            elif self.status == 'launcher':
                self.reload()
        return frame

    def create_scope_image(self, frame):
        frame = frame[int(500-(500/self.sniper_zoom)):int(500+(500/self.sniper_zoom)),
                      int(500-(500/self.sniper_zoom)):int(500+(500/self.sniper_zoom)), :]
        frame = cv.resize(frame, (1000, 1000))
        blank_image = np.zeros((1000, 1000), dtype=np.uint8)
        sniper_mask = cv.circle(blank_image, (500, 500), 300, 255, -1)
        image_with_scope = cv.bitwise_and(frame, frame, mask=sniper_mask)
        cv.line(image_with_scope, (300, 500), (700, 500), 0, 1, cv.LINE_AA)
        cv.line(image_with_scope, (500, 300), (500, 700), 0, 1, cv.LINE_AA)
        return image_with_scope

    def scope_zoom_in(self, frame):
        if self.animation_index is None:
            self.animation_index = 1
            sounds.click1.play()
        zoom_amount = 1 + (self.animation_index - 1) * 0.1
        resized_and_moved_image = frame[int(500-(500/zoom_amount)):int(500+(500/zoom_amount)),
                                        int(500-(500/zoom_amount)):int(500+(500/zoom_amount)), :]
        resized_and_moved_image = cv.resize(resized_and_moved_image, (1000, 1000))
        if self.animation_index == 10 * self.sniper_zoom:
            self.status = 'scope'
            self.animation_index = None
        else:
            self.animation_index += 1
        return resized_and_moved_image

    def scope_zoom_out(self, frame):
        if self.animation_index is None:
            self.animation_index = 10 * self.sniper_zoom
            sounds.click1.play()
        zoom_amount = 1 + (self.animation_index - 1) * 0.1
        resized_and_moved_image = frame[int(500-(500/zoom_amount)):int(500+(500/zoom_amount)),
                                        int(500-(500/zoom_amount)):int(500+(500/zoom_amount)), :]
        resized_and_moved_image = cv.resize(resized_and_moved_image, (1000, 1000))
        if self.animation_index == 0:
            self.status = 'launcher'
            self.current_weapon = 'launcher' if self.current_weapon == 'sniper' else 'reloading'
            self.animation_index = None
        else:
            self.animation_index -= 1
        return resized_and_moved_image

    @staticmethod
    def draw_launcher_scope(frame):
        cv.circle(frame, (500, 500), 30, (0, 255, 0), 1)
        cv.line(frame, (490, 500), (510, 500),
                (0, 0, 255), 1, cv.LINE_AA)
        cv.line(frame, (500, 490), (500, 510),
                (0, 0, 255), 1, cv.LINE_AA)
        return frame

    def shoot_bullet_animation(self):
        if self.animation_index is None:
            self.animation_index = 1
        elif self.animation_index < 4:
            self.aim[1] -= 20
            self.aim[0] += random.randrange(-20, 20)
        else:
            self.aim[1] += 3
        if self.animation_index == 24:
            self.status = 'scope'
            self.animation_index = None
        else:
            self.animation_index += 1

    def shoot_missile_animation(self):
        if self.animation_index is None:
            self.animation_index = 1
        elif self.animation_index < 15:
            self.aim[1] -= 30 - self.animation_index*2
        else:
            pass
        if self.animation_index == 50:
            self.status = 'launcher'
            self.animation_index = None
        else:
            self.animation_index += 1

    def shoot_bullet(self):
        for enemy in self.enemies_list:
            if enemy.bbox[0] < self.aim[0] < enemy.bbox[0] + enemy.bbox[2] and enemy.bbox[1] <\
                    self.aim[1] < enemy.bbox[1] + enemy.bbox[3]:
                enemy.kill(self.enemies_list)
                break

    def reload(self):
        if self.animation_index is None:
            self.animation_index = 1
        if self.animation_index % 75 == 0:
            sounds.click1.play()
            self.sniper_ammo += 1
            self.animation_index += 1
        else:
            if self.sniper_ammo == self.sniper_max_ammo:
                self.current_weapon = 'sniper'
                self.status = 'zoom_in'
                self.animation_index = None
            else:
                self.animation_index += 1

    def cooldown(self):
        if self.animation_index is None:
            self.animation_index = 1
        self.animation_index += 1
        if self.animation_index == 20:
            self.status = 'scope'
            self.animation_index = None

    def update_sniper(self, frame):
        if self.status == 'scope':
            if kb.is_pressed('q'):
                self.status = 'zoom_out'
            if kb.is_pressed('r'):
                sounds.reloading.play()
                self.current_weapon = 'reloading'
            if kb.is_pressed('space'):
                if self.sniper_ammo > 0:
                    self.sniper_ammo -= 1
                    sounds.sniper_shot.play()
                    self.shoot_bullet()
                    self.status = 'shot_animation'
                else:
                    sounds.no_ammo.play()
                    self.status = 'cooldown'
            frame = self.create_scope_image(frame)
        elif self.status == 'shot_animation':
            self.shoot_bullet_animation()
            frame = self.create_scope_image(frame)
        elif self.status == 'zoom_in':
            frame = self.scope_zoom_in(frame)
        elif self.status == 'zoom_out':
            frame = self.scope_zoom_out(frame)
        elif self.status == 'cooldown':
            self.cooldown()
            frame = self.create_scope_image(frame)
        return frame

    def update_launcher(self, frame):
        if self.status == 'missile_animation':
            self.shoot_missile_animation()
            frame = self.draw_launcher_scope(frame)
            # create bomb object
        elif self.status == 'launcher':
            if kb.is_pressed('q'):
                self.current_weapon = 'sniper'
                self.status = 'zoom_in'
            if kb.is_pressed('space'):
                sounds.rocket.play()
                self.status = 'missile_animation'
            if kb.is_pressed('r'):
                sounds.reloading.play()
                self.current_weapon = 'reloading'
            frame = self.draw_launcher_scope(frame)
        return frame
