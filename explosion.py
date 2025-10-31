import pygame
import random
from circleshape import CircleShape
from constants import *


default = (255, 125, 0)
starting_radius = 1

#make this more general
class Explosion (CircleShape):
    
    def __init__(self, x, y, radius, colour=default):
        super().__init__(x, y, starting_radius)
        self.final_radius = radius 
        self.colour = colour
        self.width = 0     
        self.propagation = 200 
        self.collision_on = False
        self.dp = 0 # damage it causes
        self.is_respawn_boom = False
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
        self.position += self.velocity 
        
    def check_end(self): # not used
        return  self.radius >= self.final_radius
    

