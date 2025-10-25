import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)


    def draw (self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            velocity1 = self.velocity.rotate(random.uniform(20, 50))
            velocity2 = self.velocity.rotate(-1 * random.uniform(20, 50))
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            ast1 = Asteroid(self.position.x, self.position.y, new_radius)
            ast1.velocity = velocity1 * ASTEROID_SPLIT_ACC
            ast2 = Asteroid(self.position.x, self.position.y, new_radius)
            ast2.velocity = velocity2 * ASTEROID_SPLIT_ACC