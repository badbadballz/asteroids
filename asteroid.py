import pygame
import random
from circleshape import CircleShape
from constants import *

min_spokes = 8
max_spokes = 10
ast_spokes = 9

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.spoke_angles = []
        self.rotate_speed = 0
        self.rotation = 0
        sum_angles = 0
        #for i in range(ast_spokes - 1):
        while True:
            angle = random.randint(30, 90) #40
            sum_angles += angle
            if sum_angles <= 360:
                self.spoke_angles.append(angle)
            else:
                break
        print(f"{self.spoke_angles}, {sum(self.spoke_angles)}")


    def draw (self, screen):
        points = []
        if Draw_on:
            pygame.draw.circle(screen, "red", self.position, self.radius, 1)
        
        spoke = pygame.Vector2(0, 1).rotate(self.rotation)
        pos = self.position + spoke * self.radius
        pygame.draw.circle(screen, "yellow", pos, 2, 0)
        points.append(pos)
        sum = 0
        for i in range(len(self.spoke_angles)):
            spoke = pygame.Vector2(0, 1).rotate(self.rotation  + self.spoke_angles[i] + sum)
            pos = self.position + spoke * self.radius
            #pygame.draw.circle(screen, "yellow", pos, 2, 0)
            points.append(pos)
            sum += self.spoke_angles[i]
        pygame.draw.polygon(screen, "brown", points, 2)


        
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        score = 1
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return score
        else:
            velocity1 = self.velocity.rotate(random.uniform(20, 50))
            velocity2 = self.velocity.rotate(-1 * random.uniform(20, 50))
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            ast1 = Asteroid(self.position.x, self.position.y, new_radius)
            ast1.velocity = velocity1 * ASTEROID_SPLIT_ACC
            ast2 = Asteroid(self.position.x, self.position.y, new_radius)
            ast2.velocity = velocity2 * ASTEROID_SPLIT_ACC
            return score * (new_radius // 10)