import cv2 as cv
import time
from copy import copy
import keyboard

from scripts.sounds import SoundManager


def welcome_screen():
    def show_selection(selection, text_number):
        return [100, 100, 200] if selection == text_number else [0, 0, 100]

    video = cv.VideoCapture('media/videos/bunker.mp4')
    SoundManager.opening_sound.play()
    SoundManager.zombies_sound.play()
    frame = None
    for _ in range(100):
        if keyboard.is_pressed('q'):
            SoundManager.mixer.stop()
            return None
        image_read_correctly, frame = video.read()
        cv.imshow('game', frame)
        cv.waitKey(24)

    cv.putText(frame, 'Zombies Mayhem', (150, 200), 3, 3, (0, 120, 70), 3)
    cv.imshow('game', frame)
    cv.waitKey(1)
    time.sleep(1)
    select = 1

    while True:
        frame_copy = copy(frame)
        if keyboard.is_pressed('space'):
            SoundManager.click2.play()
            if select == 1:
                SoundManager.opening_sound.fadeout(1000)
                cv.waitKey(200)
                break
            elif select == 2:
                cv.putText(frame_copy, 'fuck off', (200, 450), 1, 1, (0, 0, 100), thickness=3)
            else:
                quit()

        if keyboard.is_pressed('w'):
            SoundManager.click2.play()
            select -= 1 if select > 1 else 0

        if keyboard.is_pressed('s'):
            SoundManager.click2.play()
            select += 1 if select < 3 else 0

        cv.putText(frame_copy, 'Play', (200, 300), 3, 2, show_selection(select, 1), thickness=4)
        cv.putText(frame_copy, 'Settings', (200, 400), 3, 2, show_selection(select, 2), thickness=3)
        cv.putText(frame_copy, 'Quit', (200, 500), 3, 2, show_selection(select, 3), thickness=3)

        cv.imshow('game', frame_copy)
        cv.waitKey(100)


def you_won_animation(frame):
    def show_selection(selection, text_number):
        return [0, 255, 0] if selection == text_number else [0, 150, 0]

    SoundManager.mixer.stop()
    SoundManager.you_win.play()
    cv.putText(frame, 'YOU WON', (200, 200), 1, 5, (100, 255, 100), 10)
    cv.imshow('game', frame)
    cv.waitKey(20)
    time.sleep(1)
    select = 1
    while True:
        frame_copy = copy(frame)
        if keyboard.is_pressed('space'):
            SoundManager.click2.play()
            if select == 1:
                return
            elif select == 2:
                quit()

        if keyboard.is_pressed('w'):
            SoundManager.click2.play()
            select -= 1 if select > 1 else 0

        if keyboard.is_pressed('s'):
            SoundManager.click2.play()
            select += 1 if select < 2 else 0

        cv.putText(frame_copy, 'Continue', (200, 400), 3, 2, show_selection(select, 1), thickness=4)
        cv.putText(frame_copy, 'Quit (like a bitch)', (200, 500), 3, 2, show_selection(select, 2), thickness=3)

        cv.imshow('game', frame_copy)
        cv.waitKey(200)


def you_lose_animation(frame):
    def show_selection(selection, text_number):
        return [0, 0, 255] if selection == text_number else [0, 0, 150]
    SoundManager.mixer.stop()
    SoundManager.death_sound1.play()
    cv.putText(frame, 'YOU DIED', (200, 200), 1, 5, (100, 100, 255), 10)
    cv.imshow('game', frame)
    cv.waitKey(20)
    time.sleep(1)
    select = 1
    while True:
        frame_copy = copy(frame)
        if keyboard.is_pressed('space'):
            SoundManager.click2.play()
            if select == 1:
                return
            elif select == 2:
                quit()

        if keyboard.is_pressed('w'):
            SoundManager.click2.play()
            select -= 1 if select > 1 else 0

        if keyboard.is_pressed('s'):
            SoundManager.click2.play()
            select += 1 if select < 2 else 0

        cv.putText(frame_copy, 'Try Again', (200, 400), 3, 2, show_selection(select, 1), thickness=4)
        cv.putText(frame_copy, 'Quit (like a bitch)', (200, 500), 3, 2, show_selection(select, 2), thickness=3)

        cv.imshow('game', frame_copy)
        cv.waitKey(200)
