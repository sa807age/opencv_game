from screens.main_game import main_game
from screens.cut_scenes import welcome_screen, cut_scene_1, tutorial


class ScreenAPI:
    def __init__(self):
        welcome_screen()
        tutorial()
        cut_scene_1()

    @staticmethod
    def start_round(image):
        main_game(image, ammo_amount=5)
