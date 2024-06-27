import cv2 as cv
import keyboard as kb
import time
import textwrap
import random

from scripts.round_class import Round
from scripts.sounds import game_music1, first_speech, last_speech


def display_text(image, text):
    font = cv.FONT_HERSHEY_SIMPLEX

    wrapped_text = textwrap.wrap(text, width=60)
    font_size = 1
    font_thickness = 2

    for i, line in enumerate(wrapped_text):
        textsize = cv.getTextSize(line, font, font_size, font_thickness)[0]

        gap = textsize[1] + 15

        y = int(650+textsize[1]) + i * gap
        x = int((image.shape[1] - textsize[0]) / 2)

        text_w, text_h = textsize
        cv.rectangle(image, (x - 3, y+8), (x+3+text_w, y-text_h-6), (0, 0, 0), -1)
        cv.putText(image, line, (x, y), font,
                   font_size,
                   (255, 255, 255),
                   font_thickness,
                   lineType=cv.LINE_AA)


def play_tutorial():
    round_img_path = 'media/photos/first_round.jpg'
    round_img = cv.imread(round_img_path)
    tutorial_round = Round(image=round_img, sniper_max_ammo=5, launcher_ammo=3, sniper_zoom=2, time=-1,
                           round_music=game_music1, y_location=2600, soldier_spawn_rate=1 / 1000000000,
                           headers=['Tutorial', ''])
    # adjustment time phase
    for _ in range(200):
        if kb.is_pressed('esc'):
            quit()
        frame = tutorial_round.load_frame()
        cv.imshow('game', frame)
        cv.waitKey(5)
    starting_time = time.time()
    first_speech.play()
    while True:
        if kb.is_pressed('esc'):
            quit()
        frame = tutorial_round.load_frame()
        time_from_start = round(time.time() - starting_time, 1)
        show_first_speech(time_from_start, frame)
        cv.imshow('game', frame)
        cv.waitKey(5)
        if time_from_start == 27:
            break
    starting_time = time.time()
    while True:
        if kb.is_pressed('esc'):
            quit()
        frame = tutorial_round.load_frame()
        time_from_start = round(time.time() - starting_time, 1)
        cv.putText(frame, 'Use the keys:', (350, 100), 3, 2, (0, 0, 0), 3)
        cv.putText(frame, 'A, S, W, D', (410, 200), 3, 2, (0, 0, 0), 3)
        cv.putText(frame, 'to move around', (350, 300), 3, 2, (0, 0, 0), 3)

        cv.imshow('game', frame)
        cv.waitKey(5)
        if time_from_start == 5:
            break
    tutorial_round.enemies.add_soldier([800, 2600])
    while True:
        if kb.is_pressed('esc'):
            quit()
        frame = tutorial_round.load_frame()
        cv.putText(frame, 'Zombie Incoming', (350, 100), 3, 2, (0, 0, 0), 3)
        cv.putText(frame, 'find it!', (500, 200), 3, 2, (0, 0, 0), 3)
        cv.imshow('game', frame)
        cv.waitKey(5)
        zombie_bbox = tutorial_round.enemies.enemies_list[0].bbox
        if (zombie_bbox[0] < tutorial_round.aim.x < zombie_bbox[0] + zombie_bbox[2] and
                zombie_bbox[1] < tutorial_round.aim.y < zombie_bbox[1] + zombie_bbox[3]):
            break
    frame = tutorial_round.load_frame()
    cv.putText(frame, 'Press Q to use Scope', (300, 100), 3, 2, (0, 0, 0), 3)
    while True:
        cv.imshow('game', frame)
        cv.waitKey(5)
        if kb.is_pressed('q'):
            break
    for _ in range(100):
        frame = tutorial_round.load_frame()
        cv.imshow('game', frame)
        cv.waitKey(5)
    while True:
        frame = tutorial_round.load_frame()
        cv.imshow('game', frame)
        cv.waitKey(5)
        if (zombie_bbox[0] < tutorial_round.aim.x < zombie_bbox[0] + zombie_bbox[2] and
                zombie_bbox[1] < tutorial_round.aim.y < zombie_bbox[1] + zombie_bbox[3]):
            break
    frame = tutorial_round.load_frame()
    cv.putText(frame, 'Press Space to Shoot', (250, 100), 3, 2, (255, 255, 255), 3)
    while True:
        cv.imshow('game', frame)
        cv.waitKey(5)
        if kb.is_pressed('space'):
            break
    for _ in range(300):
        frame = tutorial_round.load_frame()
        cv.imshow('game', frame)
        cv.waitKey(5)
    for _ in range(300):
        if tutorial_round.weapon.current_weapon == 'launcher':
            break
        frame = tutorial_round.load_frame()
        cv.putText(frame, 'Press Q to exit Scope', (300, 100), 3, 2, (255, 255, 255), 3)
        cv.imshow('game', frame)
        cv.waitKey(5)
    for _ in range(100):
        frame = tutorial_round.load_frame()
        tutorial_round.enemies.add_soldier([random.randrange(600, tutorial_round.original_image.shape[1] - 600),
                                            random.randrange(tutorial_round.horizon_line - 100,
                                            tutorial_round.horizon_line + 100)])
        cv.imshow('game', frame)
        cv.waitKey(5)
    while True:
        if kb.is_pressed('esc'):
            quit()
        frame = tutorial_round.load_frame()
        cv.putText(frame, 'Press G to use RPG', (300, 100), 3, 2, (0, 0, 0), 3)
        cv.imshow('game', frame)
        cv.waitKey(5)
        if kb.is_pressed('g'):
            break
    for _ in range(500):
        frame = tutorial_round.load_frame()
        cv.imshow('game', frame)
        cv.waitKey(5)
    tutorial_round.weapon.sniper_ammo = 0
    while True:
        if kb.is_pressed('esc'):
            quit()
        frame = tutorial_round.load_frame()
        cv.putText(frame, 'OOPS, you are out of ammo', (150, 100), 3, 2, (0, 0, 0), 3)
        cv.putText(frame, 'Press R to reload', (200, 200), 3, 2, (0, 0, 0), 3)
        cv.imshow('game', frame)
        cv.waitKey(5)
        if kb.is_pressed('r'):
            break
    for _ in range(500):
        frame = tutorial_round.load_frame()
        cv.imshow('game', frame)
        cv.waitKey(5)
    starting_time = time.time()
    last_speech.play()
    while True:
        if kb.is_pressed('esc'):
            quit()
        frame = tutorial_round.load_frame()
        time_from_start = round(time.time() - starting_time, 1)
        show_last_speech(time_from_start, frame)
        cv.imshow('game', frame)
        cv.waitKey(5)
        if time_from_start == 27:
            break


def show_first_speech(time_from_start, frame):
    if 0 < time_from_start < 1.5:
        display_text(frame, 'Welcome, soldier.')
    if 1.5 < time_from_start < 8.5:
        display_text(frame, ' In the face of this relentless zombie onslaught, your survival depends on your ability to'
                            ' wield your weapons effectively. ')
    if 8.5 < time_from_start < 14:
        display_text(frame, "Today, we'll quickly run through the basics to ensure you can dispatch those undead "
                            "with precision. ")
    if 14 < time_from_start < 18.8:
        display_text(frame, "Pay close attention, follow your training, and remember... every shot counts.")
    if 18.8 < time_from_start < 21.7:
        display_text(frame, "Let's gear up and get you ready to face the horde.")
    if 21.7 < time_from_start < 23.2:
        display_text(frame, "Are you ready, soldier?")
    if 23.2 < time_from_start < 26:
        display_text(frame, "Let's do this.")


def show_last_speech(time_from_start, frame):
    if 0 < time_from_start < 2:
        display_text(frame, "Soldier, we are counting on you.")
    if 2 < time_from_start < 7:
        display_text(frame, "The undead hordes are swarming towards our base, and you're our best shot at holding "
                            "them back.")
    if 7 < time_from_start < 14.5:
        display_text(frame, "Your mission is clear: head into the thick of it, take down as many as you can, "
                            "and secure the safety of our people. ")
    if 14.5 < time_from_start < 17.3:
        display_text(frame, "The fate of the base rests on your shoulders.")
    if 17.3 < time_from_start < 20:
        display_text(frame, "Good luck, and may you come back in one piece.")
    if 20 < time_from_start < 22:
        display_text(frame, "Dismissed!")

