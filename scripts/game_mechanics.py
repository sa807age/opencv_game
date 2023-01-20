import random
import time
from copy import copy
import os

import cv2 as cv
import keyboard as kb
from cv2 import LINE_AA

from scripts import sounds
from scripts.image_manipulation import resize_image, translate_image, create_blank_image
from scripts.particles import create_particles, display_all_particles, delete_all_particles

sounds_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sounds'))


def move_aim(aim, mode):
    pixels = 10 if mode == 'launcher' else 5
    if kb.is_pressed("s"):
        aim[1] += pixels
    if kb.is_pressed("w"):
        aim[1] -= pixels
    if kb.is_pressed("a"):
        aim[0] -= pixels
    if kb.is_pressed("d"):
        aim[0] += pixels
    return aim


def move_aim_breath(aim, breath, scope_y_movement):
    if breath > 100:
        scope_y_movement = -1
    if breath < 0:
        scope_y_movement = 1

    aim[1] += random.randrange(0, 2) * scope_y_movement

    scope_x_movement = random.randrange(1, 6)
    if scope_x_movement == 4:
        aim[0] += 1
    if scope_x_movement == 5:
        aim[0] -= 1

    breath += scope_y_movement * 2
    return aim, breath, scope_y_movement


def scope_zoom_animation(zoom, image, scope_aim, soldiers):
    zoom_dict = {'in': (1, 21, 1), 'out': (20, -1, -1)}
    blank_image = create_blank_image((image.shape[0], image.shape[1]))
    sounds.click1.play()
    cv.waitKey(50)
    # zooming in
    for i in range(*zoom_dict[zoom]):
        frame = resize_image(image, 1)
        soldiers.display_all_soldiers(frame)
        resized_frame = resize_image(frame, 1 + i * 0.05)
        resized_and_moved_frame = translate_image(resized_frame, (frame.shape[0] / 2 - scope_aim[0] * 2) * i * 0.05,
                                                  (frame.shape[1] / 2 - scope_aim[1] * 2) * i * 0.05,
                                                  (frame.shape[1], frame.shape[0]))
        mask = cv.circle(blank_image, (250, 250), 100, 255, -1)
        scope_image = cv.bitwise_and(resized_and_moved_frame, resized_and_moved_frame, mask=mask)

        cv.line(scope_image, (150, 250), (350, 250), 0, 1, cv.LINE_AA)
        cv.line(scope_image, (250, 150), (250, 350), 0, 1, cv.LINE_AA)

        cv.imshow("game", resized_and_moved_frame)

        cv.waitKey(5)


def create_sniper_scope_image(image, scope_aim, zoom):
    blank_image = create_blank_image((image.shape[0], image.shape[1]))
    resized_image = resize_image(image, zoom)
    resized_and_moved_image = translate_image(resized_image, image.shape[0] / zoom - scope_aim[0] * zoom,
                                              image.shape[1] / zoom - scope_aim[1] * zoom,
                                              (image.shape[1], image.shape[0]))
    sniper_mask = cv.circle(blank_image, (250, 250), 100, 255, -1)
    image_with_scope = cv.bitwise_and(resized_and_moved_image, resized_and_moved_image, mask=sniper_mask)
    cv.line(image_with_scope, (150, 250), (350, 250), 0, 1, cv.LINE_AA)
    cv.line(image_with_scope, (250, 150), (250, 350), 0, 1, cv.LINE_AA)
    return image_with_scope


def shoot_missile(image, location, soldiers):
    sounds.explosion.play()
    missile_width = 100
    missile_height_from_ground = 200
    for i in range(20):
        frame = resize_image(image, 1)
        cv.circle(frame, (location[0], location[1] + missile_height_from_ground), missile_width, (100, 100, 100),
                  cv.FILLED)
        soldiers.display_all_soldiers(frame)
        cv.imshow("game", frame)
        cv.waitKey(10)
        missile_width -= 5
        missile_height_from_ground -= 10
    all_particles = create_particles([], 500, location)
    for i in range(100):
        frame = resize_image(image, 1)
        bomb_bbox = [int(location[0] - i * 0.4), int(location[1] - i * 0.4), i, i]
        soldiers.try_to_kill(bomb_bbox)
        soldiers.display_all_soldiers(frame)
        display_all_particles(all_particles, frame)
        cv.rectangle(frame, [int(location[0]-i*0.4), int(location[1]-i*0.4)],
                            [int(location[0]+i*0.4), int(location[1]+i*0.4)], 0, 1)
        cv.imshow("game", frame)
        cv.waitKey(10)
    delete_all_particles(all_particles)


def shoot_bullet(image, scope_aim, soldiers):
    sounds.sniper_shot.play()
    soldiers.try_to_kill(scope_aim)
    for i in range(3):
        frame = copy(image)
        scope_aim[1] -= 20
        soldiers.display_all_soldiers(frame)
        scope_image = create_sniper_scope_image(frame, scope_aim, 2)
        cv.imshow("game", scope_image)
        cv.waitKey(5)

    for i in range(20):
        frame = copy(image)
        scope_aim[1] += 3
        soldiers.display_all_soldiers(frame)
        scope_image = create_sniper_scope_image(frame, scope_aim, 2)
        cv.imshow("game", scope_image)
        cv.waitKey(5)


def toggle_night_vision(night_vision):
    sounds.click2.play()
    if night_vision is True:
        night_vision = False
    else:
        sounds.night_vision.play()
        night_vision = True
    return night_vision


def draw_launcher_scope(image, location):
    cv.circle(image, location, 30, (0, 255, 0), 1)
    cv.line(image, (location[0] - 10, location[1]), (location[0] + 10, location[1]), (0, 0, 255), 1, LINE_AA)
    cv.line(image, (location[0], location[1] - 10), (location[0], location[1] + 10), (0, 0, 255), 1, LINE_AA)
