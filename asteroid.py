import pygame
import random
from circleshape import CircleShape
from constants import *
from explosion import Explosion


class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotate_speed = 0
        self.rotation = 0
        self.life = self.radius * 1
        self.splited = False

        self.spoke_angles = self.generate_asteroid()

       
    def generate_asteroid(self):
        s_angles = [0]
        min_angle = 30
        max_angle = 80
        min_sides = 6
        max_sides = 7
        sum_angles = 0
        sides = 0
        
        while True:
            angle = random.randint(min_angle, max_angle)
            sum_angles += angle
            if sum_angles <= 360:
                s_angles.append(angle)
                sides += 1
            else:
                if (sides < min_sides 
                    or sides > max_sides):
                    return self.generate_asteroid()
                else:
                    return s_angles
        #print(f"{self.spoke_angles}, {sum(self.spoke_angles)}, spokes = {len(self.spoke_angles)}")


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

    #write a damage() method
    def damage(self, dp):
        self.life -= dp
        if self.life <= 0:
            return self.split()
        return 0

    def explode(self):
         _ = Explosion(self.position.x, self.position.y, self.radius) 
         self.kill()

        # more expandable way of logging score/ damage done is need in the future!
    def split(self):
        
        if self.splited: # This is needed to stop splitting after .kill() is called
            return 0
        self.splited = True
        score = 1
                          
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.explode()
            return score
        else:
            #print(f"parent: {self.velocity}")
            angle_1 = random.uniform(20, 50) #20, 50
            #print(f"angle_1: {angle_1}")
            angle_2 = -1 * random.uniform(20, 50)
            #print(f"angle_2: {angle_2}")
            velocity_1 = self.velocity.rotate(angle_1)
            velocity_2 = self.velocity.rotate(angle_2)
            direction_1 = velocity_1.normalize()
            #print(f"direction_1: {direction_1}")
            direction_2 = velocity_2.normalize()
            #print(f"direction_2: {direction_2}")

            smaller_radius = self.radius - ASTEROID_MIN_RADIUS
            ast_1_pos = self.position + direction_1 * self.radius #why self.radius?
            #print(f"ast_1_pos: {ast_1_pos}")
            ast_2_pos = self.position + direction_2 * self.radius
            #print(f"ast_2_pos: {ast_2_pos}")
            ast_1 = Asteroid(ast_1_pos.x, ast_1_pos.y, smaller_radius)
            ast_1.velocity = velocity_1 * ASTEROID_SPLIT_ACC
            ast_1.rotate_speed = self.rotate_speed * ASTEROID_SPLIT_ACC 
            
            ast_2 = Asteroid(ast_2_pos.x, ast_2_pos.y, smaller_radius)
            ast_2.velocity = velocity_2 * ASTEROID_SPLIT_ACC
            ast_2.rotate_speed = self.rotate_speed * ASTEROID_SPLIT_ACC
            
            self.explode()
            return score * (smaller_radius // 10)