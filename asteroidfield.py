import pygame
import random
from asteroid import Asteroid
from powerup import Powerup
from constants import *
#from sounds import Sound_obj_type



class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self, gs):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.PU_spawn_timer = 0.0
        self.gs = gs

        self.spawn_rate = ASTEROID_SPAWN_RATE
        self.PU_spawn_rate = PU_SPAWN_RATE
        self.num_ast = AST_LIMIT
        self.min_ast_vel = 40
        self.max_ast_vel = 100
        self.ast_armor = 0

        #self.explode_sound = pygame.mixer.Sound("sounds/456272__soundfxstudio__distance-explosion-sound.wav")
        #print(f"af: {self.explode_sound}")

    def spawn(self, radius, position, velocity, rotate_speed):
        roll_armor_ast = random.randint(1,10)
        sound_function = self.gs.game_sounds.return_sound_function(Obj_type.AST)
        if roll_armor_ast <= CHANCE_ARMOR_AST:
            asteroid = Asteroid(position.x, position.y, radius, sound_function, self.ast_armor)
        else:
            asteroid = Asteroid(position.x, position.y, radius, sound_function)
        asteroid.velocity = velocity 
        asteroid.rotate_speed = rotate_speed

    def spawn_pu(self, position, velocity):
        pu = Powerup(position.x, position.y, "S")
        pu.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        self.PU_spawn_timer += dt
        
        if self.spawn_timer > self.spawn_rate and self.gs.check_num_ast() < self.num_ast: # difficulty /spawn, armor, boss asteroid
            edge = random.choice(self.edges)
            speed = random.randint(self.min_ast_vel, self.max_ast_vel)
            velocity = edge[0] * speed 
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            rotate_speed = ASTEROID_BASE_ROTATE_SPEED * 1 / kind * random.randint(-ASTEROID_ROTATE_SPEED_RANDOM, ASTEROID_ROTATE_SPEED_RANDOM)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity * dt, rotate_speed * dt)
            self.spawn_timer = 0
        
        if self.PU_spawn_timer > self.PU_spawn_rate:
            self.PU_spawn_timer = 0
            roll = random.randint(1, CHANCE_TO_SPAWN_PU_NO_PU)
            #print(f"roll for PU = {roll}")
            if self.gs.check_num_powerups() == 0 and roll == 1:
                edge = random.choice(self.edges)
                speed = random.randint(self.min_ast_vel, self.max_ast_vel)
                velocity = edge[0] * speed 
                velocity = velocity.rotate(random.randint(-30, 30))
                position = edge[1](random.uniform(0, 1))
                self.spawn_pu(position, velocity * dt)
            
            
#(ast spawn rate, 0 ast modifier, 0 boss ast) (min start time, min level)
    def increase_difficulty(self, d_rate, ast_armor=0, boss=0):
        self.spawn_rate = max(self.spawn_rate / d_rate, 1)
        self.min_ast_vel = min(int(self.min_ast_vel * d_rate), 200)
        self.max_ast_vel = min(int(self.max_ast_vel * d_rate), 500)
        self.num_ast = round(self.num_ast * d_rate)
        self.ast_armor = ast_armor
        #print(f"new sr: {self.spawn_rate}, min: {self.min_ast_vel}, max: {self.max_ast_vel}, num_ast: {self.num_ast}, armor: {self.ast_armor}")

#difficulty level: 18
#new sr: 1, min: 200, max: 500
#difficulty level: 19
#new sr: 1, min: 200, max: 500

#difficulty level: 18
#new sr: 1, min: 200, max: 500, num_ast: 32