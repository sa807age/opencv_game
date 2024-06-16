import cv2 as cv

from scripts.round_class import Round
from scripts.cut_scenes import welcome_screen
from scripts.sounds import game_music1, game_music2, game_music3, game_music4
from scripts.tutorial import play_tutorial

welcome_screen()
play_tutorial()


round_img_path = 'media/photos/first_round.jpg'
round_img = cv.imread(round_img_path)
Round(image=round_img, sniper_max_ammo=5, launcher_ammo=1, sniper_zoom=2, time=5, round_music=game_music1,
      horizon_line=2600, soldier_spawn_rate=1/200, headers=['Round 1', "Let's go"]).play_round()


round_img_path = 'media/photos/second_round.jpg'
round_img = cv.imread(round_img_path)
Round(image=round_img, sniper_max_ammo=5, launcher_ammo=1, sniper_zoom=5, time=45, round_music=game_music3,
      horizon_line=1500, soldier_spawn_rate=1/200, headers=['Round 2', 'Wrong scope :(']).play_round()

round_img_path = 'media/photos/third_round.jpg'
round_img = cv.imread(round_img_path)
Round(image=round_img, sniper_max_ammo=1, launcher_ammo=2, sniper_zoom=3, time=45, round_music=game_music4,
      horizon_line=2500, soldier_spawn_rate=1/200, headers=['Round 3', 'No magazine!']).play_round()


round_img_path = 'media/photos/forth_round.jpg'
round_img = cv.imread(round_img_path)
Round(image=round_img, sniper_max_ammo=1000, launcher_ammo=3, sniper_zoom=1, time=120, round_music=game_music2,
      horizon_line=1800, soldier_spawn_rate=1/50, headers=['Last Round', 'Seiko Mode']).play_round()
