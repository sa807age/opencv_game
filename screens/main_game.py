import random
import time
from copy import copy
import math

import cv2 as cv
import keyboard as kb
from scripts.init_values import initialize_all
from scripts.soldiers import Soldiers
from scripts.game_mechanics import move_aim, shoot_missile, scope_zoom_animation, \
     toggle_night_vision, shoot_bullet, create_sniper_scope_image, move_aim_breath, draw_launcher_scope
from scripts import sounds
from scripts.utils import waste_time, kill_with_mouse


def main_game():
    # setting up initial variables
    original_image, aim, poop, ammo_in_mag, soldier_spawn_chance = initialize_all()
    mode = 'launcher'
    night_vision = False
    breath = 50
    scope_y_movement = 1
    do_animation = True
    soldiers = Soldiers()
    zoom = False
    ammo = 5
    starting_time = time.time()
    # cheat for killing with mouse
    cv.setMouseCallback('game', kill_with_mouse, soldiers)
    # game music
    sounds.game_music.play()

    while True:
        if random.randrange(0, 40) == 20:
            soldiers.add_soldier((random.randrange(50, 400), random.randrange(350, 450)))
        # creating temp image to not draw on the original
        frame = copy(original_image)
        # exit the game
        if kb.is_pressed("c"):
            quit()
        # scope movement
        aim = move_aim(aim, mode)

        if kb.is_pressed("r"):
            cv.waitKey(100)
            sounds.reloading.play()
            if zoom:
                scope_zoom_animation('out', frame, aim, soldiers)
            ammo_to_reload = 5 - ammo
            for i in range(ammo_to_reload):
                waste_time(frame, soldiers, 0.7)
                sounds.click1.play()
            if mode == 'sniper':
                do_animation = True
            ammo = 5

        if mode == 'launcher':
            # shoot missile
            if kb.is_pressed("space"):
                shoot_missile(frame, aim, soldiers)
            if kb.is_pressed("q"):
                mode = 'sniper'
                do_animation = True
            # scope
            soldiers.display_all_soldiers(frame)
            draw_launcher_scope(frame, aim)

        elif mode == 'sniper':
            if do_animation:
                scope_zoom_animation('in', frame, aim, soldiers)
                zoom = True
                do_animation = False

            if kb.is_pressed("space"):
                if ammo > 0:
                    shoot_bullet(frame, aim, soldiers)
                    ammo -= 1
                else:
                    sounds.no_ammo.play()
                    cv.waitKey(100)

            if kb.is_pressed("e"):
                night_vision = toggle_night_vision(night_vision)
                cv.waitKey(100)

            if kb.is_pressed("q"):
                scope_zoom_animation('out', frame, aim, soldiers)
                zoom = False
                mode = 'launcher'
                continue

            soldiers.display_all_soldiers(frame)
            frame = create_sniper_scope_image(frame, aim, 2)
            aim, breath, scope_y_movement = move_aim_breath(aim, breath, scope_y_movement)

        cv.imshow("game", frame)
        cv.waitKey(20)


if __name__ == '__main__':
    main_game()
