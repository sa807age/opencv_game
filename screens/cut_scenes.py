import cv2 as cv
import time
from copy import copy
import keyboard

from scripts import sounds
from scripts.sounds import click2, opening_sound


def show_selection(selection, text_number):
    return [100, 100, 200] if selection == text_number else [0, 0, 100]


def welcome_screen():
    video = cv.VideoCapture('media/videos/bunker.mp4')
    opening_sound.play()
    frame = None
    for _ in range(100):
        image_read_correctly, frame = video.read()
        cv.imshow('game', frame)
        cv.waitKey(24)

    cv.putText(frame, 'Shoot to live', (200, 200), 3, 3, (0, 0, 70), 3)
    cv.imshow('game', frame)
    cv.waitKey(1)
    time.sleep(1)
    select = 1

    while True:
        frame_copy = copy(frame)
        if keyboard.is_pressed('space'):
            click2.play()
            if select == 1:
                opening_sound.fadeout(1000)
                cv.waitKey(200)
                break
            elif select == 2:
                cv.putText(frame_copy, 'fuck off', (200, 450), 1, 1, (0, 0, 100), thickness=3)
            else:
                quit()

        if keyboard.is_pressed('w'):
            click2.play()
            select -= 1 if select > 1 else 0

        if keyboard.is_pressed('s'):
            click2.play()
            select += 1 if select < 3 else 0

        cv.putText(frame_copy, 'Play', (200, 300), 3, 2, show_selection(select, 1), thickness=4)
        cv.putText(frame_copy, 'Settings', (200, 400), 3, 2, show_selection(select, 2), thickness=3)
        cv.putText(frame_copy, 'Quit', (200, 500), 3, 2, show_selection(select, 3), thickness=3)

        cv.imshow('game', frame_copy)
        cv.waitKey(200)


def cut_scene_1():
    pass


def tutorial():
    pass


def you_won():
    pass


def game_over(img):
    sounds.mixer.stop()
    sounds.death_sound1.play()
    cv.putText(img, 'You died', (int(img.shape[0] / 5), int(img.shape[1] / 2)), 1, 5, (0, 0, 255), 4)
    cv.imshow('game', img)
    cv.waitKey(20)
    time.sleep(1)
    cv.putText(img, 'press any button to exit', (int(img.shape[0] / 5), int(img.shape[1] / 2) + 50), 5, 1,
               0, 1)
    cv.imshow('game', img)
    cv.waitKey(0)
    quit()
