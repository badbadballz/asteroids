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

        self.spoke_vectors = self.generate_asteroid()
    
    def generate_asteroid(self):
        min_angle = 30
        max_angle = 80
        min_sides = 6
        max_sides = 7
        sum_angles = 0
        sides = 0
        s_vectors = [0] #[pygame.Vector2(0, 1) * self.radius] # datum spoke
        
        while True:
            angle = random.randint(min_angle, max_angle)
            sum_angles += angle
            if sum_angles <= 360 and sides <= max_sides:
                s_vectors.append(sum_angles)
                sides += 1
            else:
                if (sides < min_sides 
                    or sides > max_sides):
                    return self.generate_asteroid()
                else:
                    return [pygame.Vector2(0, 1).rotate(s_angles)* self.radius for s_angles in s_vectors]
            

    def draw (self, screen):
        if Draw_on:
            pygame.draw.circle(screen, "red", self.position, self.radius, 1)
        pointy_shape = [self.position + spoke.rotate(self.rotation) for spoke  in self.spoke_vectors]
        pygame.draw.polygon(screen, "grey50", pointy_shape, 3)

        
        
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
    
            angle_1 = random.uniform(20, 50) #20, 50
            angle_2 = -1 * random.uniform(20, 50)
            velocity_1 = self.velocity.rotate(angle_1)
            velocity_2 = self.velocity.rotate(angle_2)
            direction_1 = velocity_1.normalize()
            direction_2 = velocity_2.normalize()

            smaller_radius = self.radius - ASTEROID_MIN_RADIUS
            ast_1_pos = self.position + direction_1 * self.radius #why self.radius?
            ast_2_pos = self.position + direction_2 * self.radius

            ast_1 = Asteroid(ast_1_pos.x, ast_1_pos.y, smaller_radius)
            ast_1.velocity = velocity_1 * ASTEROID_SPLIT_ACC
            ast_1.rotate_speed = self.rotate_speed * ASTEROID_SPLIT_ACC 
            
            ast_2 = Asteroid(ast_2_pos.x, ast_2_pos.y, smaller_radius)
            ast_2.velocity = velocity_2 * ASTEROID_SPLIT_ACC
            ast_2.rotate_speed = self.rotate_speed * ASTEROID_SPLIT_ACC
            
            self.explode()
            return score * (smaller_radius // 10)
        