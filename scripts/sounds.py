from pathlib import Path
import pygame

pygame.init()
pygame.mixer.init()

sounds_folder = Path('media/sounds')


class SoundManager:
    mixer = pygame.mixer
    # music
    game_music1 = pygame.mixer.Sound(sounds_folder / 'music' / 'SilentHill.mp3')
    game_music1.set_volume(0.3)
    game_music2 = pygame.mixer.Sound(sounds_folder / 'music' / 'Final Fantasy X - To Zanarkand Remix.mp3')
    game_music2.set_volume(0.3)
    game_music3 = pygame.mixer.Sound(sounds_folder / 'music' / 'FF9 Battle (Fredrik Miller Trance Mix).mp3')
    game_music3.set_volume(0.3)
    game_music4 = pygame.mixer.Sound(sounds_folder / 'music' / 'Aeriths Theme Remix.mp3')
    game_music4.set_volume(0.7)

    opening_sound = pygame.mixer.Sound(sounds_folder / 'opening_sounds' / 'bunker.mp3')
    zombies_sound = pygame.mixer.Sound(sounds_folder / 'opening_sounds' / 'zombies.mp3')

    first_speech = pygame.mixer.Sound(sounds_folder / 'tutorial_sounds' / 'first_speech.mp3')
    last_speech = pygame.mixer.Sound(sounds_folder / 'tutorial_sounds' / 'last_speech.mp3')

    # sound effects
    click1 = pygame.mixer.Sound(sounds_folder / 'click.mp3')
    click2 = pygame.mixer.Sound(sounds_folder / 'click2.mp3')
    explosion = pygame.mixer.Sound(sounds_folder / 'explosion.mp3')
    night_vision = pygame.mixer.Sound(sounds_folder / 'night.mp3')
    rocket = pygame.mixer.Sound(sounds_folder / 'rocket.mp3')
    rocket.set_volume(0.5)
    sniper_shot = pygame.mixer.Sound(sounds_folder / 'sniper.mp3')
    sniper_shot.set_volume(0.1)
    no_ammo = pygame.mixer.Sound(sounds_folder / 'no_ammo.mp3')
    reloading = pygame.mixer.Sound(sounds_folder / 'reloading.mp3')
    screaming = pygame.mixer.Sound(sounds_folder / 'screaming.mp3')
    you_win = pygame.mixer.Sound(sounds_folder / 'you_win.mp3')

    # death sounds
    death_sound1 = pygame.mixer.Sound(sounds_folder / 'death_sounds' / 'death_sound1.mp3')
    death_sound2 = pygame.mixer.Sound(sounds_folder / 'death_sounds' / 'death_sound2.mp3')

    death_sound3 = pygame.mixer.Sound(sounds_folder / 'death_sounds' / 'death_sound3.mp3')
    death_sound3.set_volume(0.5)

    death_sound4 = pygame.mixer.Sound(sounds_folder / 'death_sounds' / 'death_sound4.mp3')
    death_sound4.set_volume(0.5)

    death_sound5 = pygame.mixer.Sound(sounds_folder / 'death_sounds' / 'death_sound5.mp3')
    death_sound5.set_volume(0.5)

    death_sound6 = pygame.mixer.Sound(sounds_folder / 'death_sounds' / 'death_sound6.mp3')
    death_sound6.set_volume(0.5)

    death_sound7 = pygame.mixer.Sound(sounds_folder / 'death_sounds' / 'death_sound7.mp3')
    death_sound7.set_volume(0.5)

    death_sound8 = pygame.mixer.Sound(sounds_folder / 'death_sounds' / 'death_sound8.mp3')
    death_sound8.set_volume(0.5)

    death_sounds = [death_sound1, death_sound2, death_sound3, death_sound4,
                    death_sound5, death_sound6, death_sound7, death_sound8]
