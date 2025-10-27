import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    
     def __init__(self, x, y):
         super().__init__(x, y, SHOT_RADIUS)
          #super().velocity = PLAYER_SHOOT_SPEED
         self.life = SHOT_LIFE

     def draw (self, screen):
         pygame.draw.circle(screen, "yellow", self.position, self.radius, 0)

     def update(self, dt):
         if self.life < 0:
             self.kill()
             return
         self.life  -= dt
         self.position += self.velocity 
        
        