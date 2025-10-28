import pygame
import random
from circleshape import CircleShape
from constants import *

propagation = 200
extra_boom = 10
colour = (255, 125, 0)

class Explosion (CircleShape):
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, 1)
        self.final_radius = radius + extra_boom
        #self.wave_width = 5 + radius // 5
        #self.time = radius * 5

    def draw(self, screen):
        #print(propagation)
        pygame.draw.circle(screen, colour , self.position, self.radius, 0) #self.wave_width)
        

    def update(self, dt):
        if self.radius <= self.final_radius:
             self.radius += dt * propagation
        else:
            self.kill()
        
    def check_end(self): 
        return  self.radius >= self.final_radius
