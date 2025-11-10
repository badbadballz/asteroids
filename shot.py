import pygame
from circleshape import CircleShape
from constants import *
from explosion import Explosion

class Shot(CircleShape):
    
     def __init__(self, x, y, radius, life, dp, explode_damage=False, explode_dp=0, max=False):
         super().__init__(x, y, radius)
         self.life = life
         self.dp = dp
         self.explode_damage = explode_damage
         self.explode_dp = explode_dp
         self.max = max

     def draw (self, screen):
         if self.max:
            #print("drawing max shot")
            pygame.draw.circle(screen, max_colour, self.position, self.radius, 0) 
         else:
            pygame.draw.circle(screen, "yellow", self.position, self.radius, 0) #yellow

     def update(self, dt):
         if self.life < 0:
             self.kill()
             return
         self.life  -= dt
         self.position += self.velocity 
        
     def damage(self, dp): #damage done to itself
         pass

         #(self, x, y, radius, colour=default, collision_on=False, dp=0, implode=False):
     def explode(self):
        if self.explode_damage:
            if self.max:
                ex = Explosion(self.position.x, self.position.y, self.radius * 12, max_colour, collision_on=True, dp=self.explode_dp)
            else:
                ex = Explosion(self.position.x, self.position.y, self.radius * 8, "yellow", collision_on=True, dp=self.explode_dp)
            ex.width = 10
        else:
            _ = Explosion(self.position.x, self.position.y, self.radius + 5, "yellow")
        self.kill()
        
        