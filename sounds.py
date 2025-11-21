import pygame
from enum import Enum
from constants import Obj_type, Action_type

# make this more general for easier to add new sounds and for new objects

class Sounds():
    def __init__(self):
        self.explode_sound = pygame.mixer.Sound("sounds/456272__soundfxstudio__distance-explosion-sound.wav")
        self.exhaust_sound = pygame.mixer.Sound("sounds/146770__qubodup__rocket-boost-engine-loop.wav")
        self.shoot_sound = pygame.mixer.Sound("sounds/362455__jalastram__shooting_sounds_003.wav")
        raw_array = pygame.mixer.Sound("sounds/825297__heosound__distant-cannon-or-gunshot.wav").get_raw()
        #print(f"raw_array: {len(raw_array)}")
        raw_array = raw_array[730000:] #1337408
        self.bump_sound = pygame.mixer.Sound(buffer=raw_array)
        self.pu_sound = pygame.mixer.Sound("sounds/531176__ryusa__synth-chiptune-8-bit-ui-interface-item-use-health-power-up.wav")
                
    # time elapse since last sound played can be done? / flasher object?!?
    def return_sound_function(self, type):
        match type:
            case Obj_type.AST:
                def wrapper(s_type):
                    match s_type:
                        case Action_type.EXPLODE:
                            def i_wrapper(volume=0):
                                if self.explode_sound.get_num_channels() < 5:
                                    self.explode_sound.play(maxtime=3000)
                                    self.explode_sound.set_volume(0.1 + volume)
                            return i_wrapper
                        case Action_type.AST_BUMP:
                            def i_wrapper(volume=0):
                                if self.bump_sound.get_num_channels() < 5:
                                    self.bump_sound.play(maxtime=3000)
                                    self.bump_sound.set_volume(0.2 + volume)
                            return i_wrapper
                        case _:
                            return
                return wrapper
            case Obj_type.PLAYER:
                def wrapper(s_type):
                    match s_type:
                        case Action_type.EXHAUST:
                            def i_wrapper(volume=0):
                                if self.exhaust_sound.get_num_channels() < 1:
                                    self.exhaust_sound.play(maxtime=250)
                                    self.exhaust_sound.set_volume(0.2 + volume) 
                            return i_wrapper
                        case Action_type.SHOOT:
                            def i_wrapper(volume=0):
                                self.shoot_sound.play(maxtime=250)
                                self.shoot_sound.set_volume(0.05 + volume)
                            return i_wrapper
                        case Action_type.PICK_UP_PU:
                            def i_wrapper(volume=0):
                                if self.pu_sound.get_num_channels() < 3:
                                    self.pu_sound.play(maxtime=900)
                                    self.pu_sound.set_volume(0.2 + volume) 
                            return i_wrapper
                        case _:
                            return
                return wrapper
            case _:
                return            

    # this can be further made better, to return a tuple? of functions for player / ast
    def play_sound(self, type):
        match type:
            
            case 1:
               
                    #self.bump_sound.play()
                
                if self.pu_sound.get_num_channels() < 1:
                    self.pu_sound.play(maxtime=900)
                    self.pu_sound.set_volume(0.3) 
               
            case _:
                return 