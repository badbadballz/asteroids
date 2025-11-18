import pygame
import random
from constants import *
from player import Player
#from asteroid import Asteroid
from asteroidfield import AsteroidField
#from shot import Shot
from explosion import Explosion
from powerup import Powerup
from sounds import Sounds, Sound_type

class Game_state():

    def __init__(self):
        self.__reset_state()

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.font_y = 0
        self.game_sounds = Sounds()

    def __reset_state(self):
        self.reset = False
        self.game_over = False
        self.dead = False
        self.health_counter = PLAYER_HEALTH
        self.life_counter = PLAYER_LIFE
        self.time_counter = 0
        self.score_counter = 0
        self.bomb_counter = PLAYER_BOMB_COUNT
        self.level_counter = 0
        
        self.difficulty = 0
        self.d_interval = D_TIME_INTERVAL

        self.invulnerable_counter = 0

    def __empty_groups(self):
        self.updatable.empty()
        self.drawable.empty()
        self.asteroids.empty()
        self.shots.empty()

    def update_player_info(self, player):
        self.health_counter = player.health
        self.bomb_counter = player.bomb_count
        self.level_counter = player.level
        

    def new_game(self):
        self.__empty_groups()
        self.__reset_state()
        self.af = AsteroidField(self)
        exhaust_sound_function =  self.game_sounds.play_sound(Sound_type.EXHAUST)
        shoot_sound_function =  self.game_sounds.play_sound(Sound_type.SHOOT)
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, exhaust_sound_function, shoot_sound_function)
        return player

    def respawn(self): 
        exhaust_sound_function =  self.game_sounds.play_sound(Sound_type.EXHAUST)
        shoot_sound_function =  self.game_sounds.play_sound(Sound_type.SHOOT)
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, exhaust_sound_function, shoot_sound_function, self.level_counter)
       
        self.update_player_info(player)
        self.dead = False
        #player.bomb()
        #self.d_interval = self.time_counter + TIME_INTERVAL # reset difficulty progression
        
        respawn_boom_final_radius = 200
        respawn_boom = Explosion(player.position.x, player.position.y, respawn_boom_final_radius, "black")
        respawn_boom.radius = 190
        respawn_boom.width = 10
        respawn_boom.propagation = 1000 #150
        respawn_boom.collision_on = True
        respawn_boom.dp = RESPAWN_BOOM
        respawn_boom.no_score = True
        self.invulnerable_counter = self.time_counter + INVULNERABLE_TIME 
        return player
    
    def is_invulnerable(self):
        #print(f"Checking Invulnerable! {self.invulnerable_counter} : {self.time_counter}") 
        return self.invulnerable_counter > self.time_counter
       

    def check_num_ast(self):
        #print(f"num ast currently = {len(self.asteroids)}")
        return len(self.asteroids)

    #method to return number of pu in the area
    def check_num_powerups(self):
        #print(f"num pu currently = {len(self.powerups)}")
        return len(self.powerups)

    def spawn_powerup(self, obj, mode="ast"):
        match mode:
            case "ast":
             #print(f"ast, num pu currently = {len(self.powerups)}")
             if self.check_num_powerups() < MAX_PU_NUM:
                
                chance = BASE_AST_PU_CHANCE + obj.radius - ASTEROID_MIN_RADIUS #smallest ast = base chance
                roll = random.randint(1, 100)
                #print(f"chance {chance} / 100, roll: {roll}")
                if roll <= chance:
                    self.__make_powerup(obj)
                    
            case "player":
                match obj.level:
                    case l if l > 5 and l <= 10:
                       #print("level 6 - 10") # 1
                       return self.__make_powerup(obj, "player", 1)
                    case l if l > 10 and l <= 20:
                       #print("level 11 - 20") # 2
                       return self.__make_powerup(obj, "player", 2)
                    case l if l > 20 and l <= 25:
                       #print("level 21 - 25") # 3
                       return self.__make_powerup(obj, "player", 3)
                    case l if l > 25:
                       #print("level > 25") # 4
                       return self.__make_powerup(obj, "player", 4)
                    case _:
                       #print("whatever")
                       return self.__make_powerup(obj, "player", 0)

    def __make_powerup(self, obj, mode="ast", number=0):
        #print("make powerup ast")
        match mode:
            case "ast":
                [pu_type] = random.choices(PU, PU_WEIGHTS)
                angle = random.uniform(-100, 100)
                velocity = obj.velocity.rotate(angle) * PU_SPLIT_ACC 
                pu = Powerup(obj.position.x, obj.position.y, pu_type)
                pu.velocity = velocity
                #print(f"give {pu_type}, velocity: {velocity}")
            case "player":
                if number <= 0:
                    return 0
                # refine this pu generation
                if obj.velocity.magnitude() < 0.4:
                    for n in range(number):
                        angle = random.uniform(0, 360)
                        v_random = random.uniform(0.4, 0.5)
                        velocity = pygame.Vector2(1,0).rotate(angle) * v_random
                        pu = Powerup(obj.position.x, obj.position.y, "S")
                        pu.velocity = velocity
                        #print(f"give S, {n}, velocity: {velocity}, mag: {velocity.magnitude()}")
                        n += 1

                else:
                    for n in range(number):
                        angle = random.uniform(-15, 15)
                        v_random = random.uniform(1, PU_SPLIT_ACC)
                        velocity = obj.velocity.rotate(angle) * v_random 
                        pu = Powerup(obj.position.x, obj.position.y, "S")
                        pu.velocity = velocity
                        #print(f"give S, {n}, velocity: {velocity}, mag: {velocity.magnitude()}")
                        n += 1
                #print(f"number: {number}")
                return number
            case _:
                return 0

    def reward_score(self, obj, type=None):
        if type == None:
            base_score = 1
        #function to calculate the score from the thing
            if obj.radius <= ASTEROID_MIN_RADIUS:
                self.score_counter += base_score
            else:
                self.score_counter += obj.radius // 10 

    #(ast spawn rate, 0 ast modifier, 0 boss ast, min start time, min level)
        
        
    def calculate_difficulty(self): # stopping/ how to calculate difficulty when player is respawning???
        
        
        if (self.d_interval - self.time_counter) <= 0 and self.difficulty < MAX_DIFF_LEVEL:
                
                    self.difficulty += 1
                    #print(f"difficulty level: {self.difficulty}")
                    ast_armor = self.level_counter // 10 # armor scales every 10 levels
                    self.af.increase_difficulty(1.1, ast_armor)   #1.1 difficulty scale
                    self.reset_d_interval()

         #or (player_level > 0 and player_level % level_interval == 0): issue with multiple S at same time

    def reset_d_interval(self):
        self.d_interval = self.time_counter + D_TIME_INTERVAL