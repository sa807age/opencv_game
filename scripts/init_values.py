# this file contains the initial values for the game
import cv2 as cv
import os


def initialize_all():
    cv.namedWindow('game')
    images_path = r'media/photos' if os.path.exists(r'media/photos') else r'../media/photos'
    selected_image = 'artworks-ulR2yrpsx0S6d5Ra-nXZ09Q-t500x500.jpg'
    original_image = cv.imread(os.path.join(images_path, selected_image))

    aim = [original_image.shape[0]//2, original_image.shape[1]//2]
    soldiers_list = []
    ammo_in_mag = 5

    soldier_spawn_chance = 5

    return original_image, aim, soldiers_list, ammo_in_mag, soldier_spawn_chance
