# this file contains the initial values for the game
import cv2 as cv
import os

from scripts.enemies import Enemies


def initialize_image_and_aim(image_name):
    cv.namedWindow('game')
    images_path = r'media/photos' if os.path.exists(r'media/photos') else r'../media/photos'
    selected_image = 'artworks-ulR2yrpsx0S6d5Ra-nXZ09Q-t500x500.jpg'
    original_image = cv.imread(os.path.join(images_path, selected_image))
    aim = [original_image.shape[0]//2, original_image.shape[1]//2]
    return original_image, aim


def init_enemies(soldier_spawn_rate, assassin_spawn_rate):
    return Enemies()
