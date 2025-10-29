import pygame
from circleshape import CircleShape
from constants import *
from explosion import Explosion

class Shot(CircleShape):
    
     def __init__(self, x, y):
         super().__init__(x, y, SHOT_RADIUS)
         self.life = SHOT_LIFE
         self.dp = SHOT_DAMAGE

     def draw (self, screen):
         pygame.draw.circle(screen, "yellow", self.position, self.radius, 0)

     def update(self, dt):
         if self.life < 0:
             self.kill()
             return
         self.life  -= dt
         self.position += self.velocity 
        
     def damage(self, dp):
         pass

     def explode(self):
        _ = Explosion(self.position.x, self.position.y, self.radius)
        self.kill()
        
        