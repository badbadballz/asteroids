import pygame
import random
from circleshape import CircleShape
from constants import *


extra_boom = 10
default = (255, 125, 0)

#make this more general
class Explosion (CircleShape):
    
    def __init__(self, x, y, radius, colour=default, width=0, prog=200, collision_on=False, dp=0):
        super().__init__(x, y, 1)
        self.final_radius = radius + extra_boom
        self.colour = colour
        self.width = width     
        self.propagation = prog  
        self.collision_on = collision_on
        self.dp = dp # damage it causes
        #self.wave_width = 5 + radius // 5
        #self.time = radius * 5

    def draw(self, screen):
        #print(propagation)
        pygame.draw.circle(screen, self.colour , self.position, self.radius, self.width) #self.wave_width)
        

    def update(self, dt):
        if self.radius <= self.final_radius:
             self.radius += dt * self.propagation
        else:
            self.kill()
        
    def check_end(self): # not used
        return  self.radius >= self.final_radius
    

