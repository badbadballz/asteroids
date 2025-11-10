import pygame
import random
from circleshape import CircleShape
from constants import *


default = "orange"
starting_radius = 1

class Explosion (CircleShape):
    
    def __init__(self, x, y, radius, colour=default, collision_on=False, dp=0):
        super().__init__(x, y, starting_radius)
        self.final_radius = radius 
        self.colour = colour
        self.width = 0     
        self.propagation = 200 
        self.collision_on = collision_on
        self.dp = dp # damage it causes
        self.no_score = False


    def draw(self, screen):
        pygame.draw.circle(screen, self.colour , self.position, self.radius, self.width) 
        

    def update(self, dt):
        if self.radius <= self.final_radius:
             self.radius += dt * self.propagation
        else:
            self.kill()
        self.position += self.velocity 
    
class Implosion (CircleShape):
    
    def __init__(self, x, y, radius, colour=default):
        super().__init__(x, y, radius)
        self.final_radius = 1
        self.colour = colour
        self.width = 0     
        self.propagation = 200 

    def draw(self, screen):

        pygame.draw.circle(screen, self.colour , self.position, self.radius, self.width) #self.wave_width)
        

    def update(self, dt):
        if self.radius >= self.final_radius:
             self.radius -= dt * self.propagation
        else:
            self.kill()
        self.position += self.velocity 

