import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.spoke_angles = [0] #inital datum spoke
        self.rotate_speed = 0
        self.rotation = 0

        self.generate_asteroid()

    #def __eq__(self, ast):
    #    return self.id == ast.id

       
    def generate_asteroid(self):
        min_angle = 30
        max_angle = 80
        sum_angles = 0
        
        while True:
            angle = random.randint(min_angle, max_angle)
            sum_angles += angle
            if sum_angles <= 360:
                self.spoke_angles.append(angle)
            else:
                break
        print(f"{self.spoke_angles}, {sum(self.spoke_angles)}, spokes = {len(self.spoke_angles)}")


    def draw (self, screen):
        if Draw_on:
            pygame.draw.circle(screen, "red", self.position, self.radius, 1)
         
        pygame.draw.polygon(screen, "brown", self.pointy_shape(screen), 2)

    def pointy_shape(self, screen):
        points = []
        sum_of_angles = 0
        
        for i in range(len(self.spoke_angles)):
            spoke = pygame.Vector2(0, 1).rotate(self.rotation  + self.spoke_angles[i] + sum_of_angles)
            point = self.position + spoke * self.radius
            if Draw_on:
                pygame.draw.circle(screen, "yellow", point, 2, 0)
            points.append(point)
            sum_of_angles += self.spoke_angles[i]
        
        return points
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotate_speed * dt

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
            ast1.rotate_speed = self.rotate_speed * ASTEROID_SPLIT_ACC 
            ast2 = Asteroid(self.position.x, self.position.y, new_radius)
            ast2.velocity = velocity2 * ASTEROID_SPLIT_ACC
            ast2.rotate_speed = self.rotate_speed * ASTEROID_SPLIT_ACC
            return score * (new_radius // 10)