import pygame
import random
from constants import *
from player import Player
#from asteroid import Asteroid
from asteroidfield import AsteroidField
#from shot import Shot
from explosion import Explosion
from powerup import Powerup

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
        

    def __reset_state(self):
        self.reset = False
        self.game_over = False
        self.dead = False
        #self.dead_timer = 0
        self.health_counter = PLAYER_HEALTH
        self.life_counter = PLAYER_LIFE
        self.time_counter = 0
        self.score_counter = 0
        self.bomb_counter = PLAYER_BOMB_COUNT
        self.level_counter = 0

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
        _ = AsteroidField()

    def respawn(self): # boom could be seen over powerups
        respawn_boom_final_radius = 200
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.update_player_info(player)
        #self.health_counter = PLAYER_HEALTH
        #self.bomb_counter = PLAYER_BOMB_COUNT
        self.dead = False
        respawn_boom = Explosion(player.position.x, player.position.y, respawn_boom_final_radius, "black")
        respawn_boom.radius = player.radius + 10
        respawn_boom.width = 10
        respawn_boom.propagation = 200 #150
        respawn_boom.collision_on = True
        respawn_boom.dp = RESPAWN_BOOM
        respawn_boom.no_score = True
        return player
    
    #working on this
    def spawn_powerup(self, ast):
        if len(self.powerups) <= MAX_PU_NUM:
            chance = BASE_AST_PU_CHANCE + ast.radius - ASTEROID_MIN_RADIUS #smallest ast = base chance
            roll = random.randint(1, 100)
            #print(f"chance {chance} / 100, roll: {roll}")
            if roll <= chance:
                [pu_type] = random.choices(PU, PU_WEIGHTS)
                angle = random.uniform(-100, 100)
                velocity = ast.velocity.rotate(angle) * PU_SPLIT_ACC
                pu = Powerup(ast.position.x, ast.position.y, pu_type)
                pu.velocity = velocity


    def reward_score(self, obj, type=None):
        if type == None:
            base_score = 1
        #function to calculate the score from the thing
            if obj.radius <= ASTEROID_MIN_RADIUS:
                self.score_counter += base_score
            else:
                self.score_counter += obj.radius // 10 
        
        
    