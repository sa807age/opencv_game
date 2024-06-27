import random

import keyboard as kb
import numpy as np
import cv2 as cv

from scripts.zombies import Zombie
from scripts.utils import draw_image_on_image
from scripts import sounds


bullet_path = 'media/photos/bullet.png'
bullet_icon = cv.resize(cv.imread(bullet_path, -1), (50, 50))
missile_path = 'media/photos/missile.png'
missile_icon = cv.resize(cv.imread(missile_path, -1), (70, 70))


class Weapon:
    def __init__(self, sniper_max_ammo, launcher_ammo, sniper_zoom, aim):
        self.current_weapon = 'launcher'
        self.sniper_max_ammo = sniper_max_ammo
        self.sniper_ammo = sniper_max_ammo
        self.launcher_ammo = launcher_ammo
        self.animation_index = None
        self.status = 'launcher'
        self.sniper_zoom = sniper_zoom
        self.aim = aim

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
        self.draw_ammo(frame)
        return frame

    def create_scope_image(self, frame):
        frame = frame[int(400-(400/self.sniper_zoom)):int(400+(400/self.sniper_zoom)),
                      int(600-(600/self.sniper_zoom)):int(600+(600/self.sniper_zoom)), :]
        frame = cv.resize(frame, (1200, 800))
        blank_image = np.zeros((800, 1200), dtype=np.uint8)
        sniper_mask = cv.circle(blank_image, (600, 400), 300, [255, 255, 255], -1)
        image_with_scope = cv.bitwise_and(frame, frame, mask=sniper_mask)
        cv.line(image_with_scope, (550, 400), (650, 400), (0, 0, 255), 1, cv.LINE_AA)
        cv.line(image_with_scope, (600, 350), (600, 450), (0, 0, 255), 1, cv.LINE_AA)
        cv.line(image_with_scope, (560, 460), (640, 460), (0, 255, 0), 1, cv.LINE_AA)
        cv.line(image_with_scope, (570, 490), (630, 490), (0, 255, 0), 1, cv.LINE_AA)
        cv.line(image_with_scope, (580, 520), (620, 520), (0, 255, 0), 1, cv.LINE_AA)

        return image_with_scope

    def scope_zoom_in(self, frame):
        if self.animation_index is None:
            self.animation_index = 1
            sounds.click1.play()
        zoom_amount = 1 + (self.animation_index - 1) * 0.1
        resized_and_moved_image = frame[int(400-(400/zoom_amount)):int(400+(400/zoom_amount)),
                                        int(600-(600/zoom_amount)):int(600+(600/zoom_amount)), :]
        resized_and_moved_image = cv.resize(resized_and_moved_image, (1200, 800))
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
        resized_and_moved_image = frame[int(400-(400/zoom_amount)):int(400+(400/zoom_amount)),
                                        int(600-(600/zoom_amount)):int(600+(600/zoom_amount)), :]
        resized_and_moved_image = cv.resize(resized_and_moved_image, (1200, 800))
        if self.animation_index == 0:
            self.status = 'launcher'
            self.current_weapon = 'launcher' if self.current_weapon == 'sniper' else 'reloading'
            self.animation_index = None
        else:
            self.animation_index -= 1
        return resized_and_moved_image

    @staticmethod
    def draw_launcher_scope(frame):
        cv.circle(frame, (600, 400), 30, (0, 255, 0), 1)
        cv.line(frame, (590, 400), (610, 400),
                (0, 0, 255), 1, cv.LINE_AA)
        cv.line(frame, (600, 390), (600, 410),
                (0, 0, 255), 1, cv.LINE_AA)
        return frame

    def shoot_bullet_animation(self):
        if self.animation_index is None:
            self.animation_index = 1
        elif self.animation_index < 4:
            self.aim.y -= 20
            self.aim.x += random.randrange(-20, 20)
        else:
            self.aim.y += 3
        if self.animation_index == 24:
            if self.current_weapon == 'launcher':
                self.status = 'launcher'
            elif self.current_weapon == 'sniper':
                self.status = 'scope'
            self.animation_index = None
        else:
            self.animation_index += 1

    def shoot_missile_animation(self):
        if self.animation_index is None:
            self.animation_index = 1
        elif self.animation_index < 15:
            self.aim.y -= 30 - self.animation_index*2
        else:
            pass
        if self.animation_index == 50:
            self.status = 'boom'
            self.animation_index = None
        else:
            self.animation_index += 1

    def shoot_bullet(self):
        for zombie in Zombie.zombies:
            bbox = zombie.get_bbox()
            if bbox[0] < self.aim.x < bbox[0] + bbox[2] and bbox[1] < self.aim.y < bbox[1] + bbox[3]:
                zombie.kill()
                return

    def reload(self):
        if self.animation_index is None:
            self.animation_index = 1
        if self.animation_index % 75 == 0:
            sounds.click2.play()
            self.sniper_ammo += 1
            self.animation_index += 1
        else:
            if self.sniper_ammo == self.sniper_max_ammo and self.animation_index % 74 == 0:
                self.current_weapon = 'launcher'
                self.status = 'launcher'
                self.animation_index = None
            else:
                self.animation_index += 1

    def cooldown(self):
        if self.animation_index is None:
            self.animation_index = 1
        self.animation_index += 1
        if self.animation_index == 20:
            self.animation_index = None
            if self.current_weapon == 'sniper':
                self.status = 'scope'
            elif self.current_weapon == 'launcher':
                self.status = 'launcher'

    def update_sniper(self, frame):
        if self.status == 'scope':
            if kb.is_pressed('q'):
                self.status = 'zoom_out'
            if kb.is_pressed('r'):
                if self.sniper_ammo < 100:
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
            # create bomb object
        elif self.status == 'launcher':
            if kb.is_pressed('q'):
                self.current_weapon = 'sniper'
                self.status = 'zoom_in'
            if kb.is_pressed('space'):
                if self.sniper_ammo > 0:
                    self.sniper_ammo -= 1
                    sounds.sniper_shot.play()
                    self.shoot_bullet()
                    self.status = 'shot_animation'
            if kb.is_pressed('g'):
                if not self.launcher_ammo:
                    sounds.no_ammo.play()
                    self.status = 'cooldown'
                else:
                    self.launcher_ammo -= 1
                    sounds.rocket.play()
                    self.status = 'missile_animation'
            if kb.is_pressed('r'):
                if self.sniper_ammo < 100:
                    sounds.reloading.play()
                    self.current_weapon = 'reloading'
        elif self.status == 'boom':
            frame = self.update_explosion()
        elif self.status == 'cooldown':
            self.cooldown()
        elif self.status == 'shot_animation':
            self.shoot_bullet_animation()
        frame = self.draw_launcher_scope(frame)
        return frame

    def draw_ammo(self, frame):
        location = 1150
        for _ in range(self.launcher_ammo):
            draw_image_on_image(frame, missile_icon, (location, 80))
            location -= 30
        location = 1150
        if self.sniper_ammo > 100:
            cv.putText(frame, 'infinite ammo!!!', (location-250, 30), 4, 1, (0, 100, 0), 2)
            return None
        for _ in range(self.sniper_ammo):
            draw_image_on_image(frame, bullet_icon, (location, 30))
            location -= 30

    def update_explosion(self):
        if self.animation_index is None:
            self.animation_index = 1
            Zombie.kill_all()
        brightness = 250-self.animation_index*3
        if self.animation_index % 30 < 15:
            pixel = [brightness, brightness, 255]
        else:
            pixel = [0, 0, 0]
        image = np.full((800, 1200, 3), pixel, dtype=np.uint8)
        self.animation_index += 1
        if self.animation_index == 80:
            self.status = 'launcher'
            self.animation_index = None
        return image

