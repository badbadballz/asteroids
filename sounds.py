import pygame
from enum import Enum

class Sound_type(Enum):
    EXPLODE = 0
    EXHAUST = 1
    SHOOT = 2

class Sounds():
    def __init__(self):
        self.explode_sound = pygame.mixer.Sound("sounds/456272__soundfxstudio__distance-explosion-sound.wav")
        self.exhaust_sound = pygame.mixer.Sound("sounds/146770__qubodup__rocket-boost-engine-loop.wav")
        self.shoot_sound = pygame.mixer.Sound("sounds/362458__jalastram__shooting_sounds_008.wav")
    

    def play_sound(self, type):
        match type:
            case Sound_type.EXPLODE:
                def wrapper():
                    if self.explode_sound.get_num_channels() < 5:
                        self.explode_sound.play(maxtime=2000)
                        self.explode_sound.set_volume(0.1)
                return wrapper

            case Sound_type.EXHAUST:
                def wrapper():
                    if self.exhaust_sound.get_num_channels() < 1:
                        self.exhaust_sound.play(maxtime=200)
                        self.exhaust_sound.set_volume(0.2)
                return wrapper
            case Sound_type.SHOOT:
                def wrapper():
                    self.shoot_sound.play(maxtime=200)
                    self.shoot_sound.set_volume(0.05)
                return wrapper
            case _:
                return