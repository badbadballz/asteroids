import pygame
from enum import Enum

# make this more general for easier to add new sounds and for new objects

class Sound_obj_type(Enum):
    AST = 0
    PLAYER = 1

class Sound_type(Enum):
    EXPLODE = 0
    EXHAUST = 1
    SHOOT = 2
    BOMB = 3
    PICK_UP_PU = 4
    PLAYER_COLLISION = 5
    AST_BUMP = 6
    DEATH = 7 

class Sounds():
    def __init__(self):
        self.explode_sound = pygame.mixer.Sound("sounds/456272__soundfxstudio__distance-explosion-sound.wav")
        self.exhaust_sound = pygame.mixer.Sound("sounds/146770__qubodup__rocket-boost-engine-loop.wav")
        self.shoot_sound = pygame.mixer.Sound("sounds/362455__jalastram__shooting_sounds_003.wav")
        raw_array = pygame.mixer.Sound("sounds/825297__heosound__distant-cannon-or-gunshot.wav").get_raw()
        #print(f"raw_array: {len(raw_array)}")
        raw_array = raw_array[730000:] #1337408
        self.bump_sound = pygame.mixer.Sound(buffer=raw_array)
                

    def return_sound_function(self, type):
        match type:
            case Sound_obj_type.AST:
                def wrapper(s_type):
                    match s_type:
                        case Sound_type.EXPLODE:
                            if self.explode_sound.get_num_channels() < 5:
                                self.explode_sound.play(maxtime=3000)
                                self.explode_sound.set_volume(0.1)
                        case Sound_type.AST_BUMP:
                            if self.bump_sound.get_num_channels() < 5:
                                self.bump_sound.play(maxtime=3000)
                                self.bump_sound.set_volume(0.2)
                        case _:
                            return
                return wrapper
            case Sound_obj_type.PLAYER:
                def wrapper(s_type):
                    match s_type:
                        case Sound_type.EXHAUST:
                            if self.exhaust_sound.get_num_channels() < 1:
                                self.exhaust_sound.play(maxtime=250)
                                self.exhaust_sound.set_volume(0.2) 
                        case Sound_type.SHOOT:
                            self.shoot_sound.play(maxtime=250)
                            self.shoot_sound.set_volume(0.05)
                        case _:
                            return
                return wrapper
            case _:
                return            

    # this can be further made better, to return a tuple? of functions for player / ast
    def play_sound(self, type):
        match type:
            case Sound_type.EXPLODE:
                def wrapper():
                    if self.explode_sound.get_num_channels() < 5:
                        self.explode_sound.play(maxtime=3000)
                        self.explode_sound.set_volume(0.1)
                return wrapper

            case Sound_type.EXHAUST:
                def wrapper():
                    if self.exhaust_sound.get_num_channels() < 1:
                        self.exhaust_sound.play(maxtime=250)
                        self.exhaust_sound.set_volume(0.2)
                return wrapper
            case Sound_type.SHOOT:
                def wrapper():
                    self.shoot_sound.play(maxtime=250)
                    self.shoot_sound.set_volume(0.05)
                return wrapper
            case 6:
               
                    #self.bump_sound.play()
                
                if self.bump_sound.get_num_channels() < 1:
                    self.bump_sound.play(maxtime=3000)
                    self.bump_sound.set_volume(0.2)
               
            case _:
                return 