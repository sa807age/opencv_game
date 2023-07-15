import time
import cv2 as cv

from scripts.round_class import Round
from scripts.cut_scenes import welcome_screen
from scripts.sounds import game_music1, game_music2, game_music3, game_music4

welcome_screen()
# tutorial()


round_img_path = 'media/photos/pexels-kyle-dolan-3808853.jpg'
round_img = cv.imread(round_img_path)
while True:
    time.sleep(0.3)
    if Round(image=round_img, sniper_max_ammo=5, launcher_ammo=1, sniper_zoom=2, time=60, round_music=game_music1,
             horizon_line=2600, soldier_spawn_rate=1/200, headers=['Round 1', "Let's go"]).start_round():
        break

round_img_path = 'media/photos/pexels-tyler-lastovich-808465.jpg'
round_img = cv.imread(round_img_path)
while True:
    time.sleep(0.3)
    if Round(image=round_img, sniper_max_ammo=5, launcher_ammo=1, sniper_zoom=5, time=60, round_music=game_music3,
             horizon_line=2000, soldier_spawn_rate=1/200, headers=['Round 2', 'Wrong scope :(']).start_round():
        break

round_img_path = 'media/photos/pexels-david-bartus-1166209.jpg'
round_img = cv.imread(round_img_path)
while True:
    time.sleep(0.3)
    if Round(image=round_img, sniper_max_ammo=1, launcher_ammo=2, sniper_zoom=3, time=60, round_music=game_music4,
             horizon_line=2500, soldier_spawn_rate=1/200, headers=['Round 3', 'No magazine!']).start_round():
        break


round_img_path = 'media/photos/pexels-yew-hui-tan-17388779.jpg'
round_img = cv.imread(round_img_path)
while True:
    time.sleep(0.3)
    if Round(image=round_img, sniper_max_ammo=1000, launcher_ammo=3, sniper_zoom=1, time=120, round_music=game_music2,
             horizon_line=1800, soldier_spawn_rate=1/50 , headers=['Last Round', 'Seiko Mode']).start_round():
        break
