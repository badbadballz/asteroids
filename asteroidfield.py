import pygame
import random
from asteroid import Asteroid
from constants import *



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
        self.gs = gs

    def spawn(self, radius, position, velocity, rotate_speed):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        asteroid.rotate_speed = rotate_speed

    def spawn_pu(self, radius, position, velocity, rotate_speed):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity
        asteroid.rotate_speed = rotate_speed  
        

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE: # difficulty /spawn, armor, boss asteroid
             
                
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed 
            velocity = velocity.rotate(random.randint(-30, 30))
            #position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            rotate_speed = ASTEROID_BASE_ROTATE_SPEED * 1 / kind * random.randint(-ASTEROID_ROTATE_SPEED_RANDOM, ASTEROID_ROTATE_SPEED_RANDOM)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity * dt, rotate_speed * dt)


#(ast spawn rate, 0 ast modifier, 0 boss ast, min start time, min level)
    def increase_difficulty(self, spawn_rate, ast_armor, boss):
        pass