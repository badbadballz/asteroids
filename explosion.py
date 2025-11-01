import pygame
import random
from circleshape import CircleShape
from constants import *


default = "orange"
starting_radius = 1

#make this more general / implosion
class Explosion (CircleShape):
    
    def __init__(self, x, y, radius, colour=default, collision_on=False, dp=0, implode=False):
        super().__init__(x, y, starting_radius)
        self.final_radius = radius 
        self.colour = colour
        self.width = 0     
        self.propagation = 200 
        self.collision_on = collision_on
        self.dp = dp # damage it causes
        self.no_score = False
        #self.wave_width = 5 + radius // 5
        #self.time = radius * 5
        self.implode = implode

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
    

