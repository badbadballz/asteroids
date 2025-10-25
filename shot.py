import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    
     def __init__(self, x, y):
         super().__init__(x, y, SHOT_RADIUS)
          #super().velocity = PLAYER_SHOOT_SPEED

     def draw (self, screen):
         pygame.draw.circle(screen, "yellow", self.position, self.radius, 0)

     def update(self, _):
         self.position += self.velocity  #what is dt for?, no need for dt because velocity has already dt factored in...