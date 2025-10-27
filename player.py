import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.rotate_speed = 0
        self.shot_cooldown = 0 #shot cooldown timer

# in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    #thats why, I've defined my own draw method???
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    #why dt needed, what exactly is dt??
    def move(self, dt):

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_SPEED * dt

    def rotate(self, dt):
        #self.rotation += PLAYER_TURN_SPEED * dt
        self.rotate_speed += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.shot_cooldown -= dt
        self.position += self.velocity
        self.rotation += self.rotate_speed
        
        #print(f"{self.position} {self.check_bounds()}")
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            # left
            self.rotate(-dt)
        if keys[pygame.K_d]:
            # right
            self.rotate(dt)
        if keys[pygame.K_w]:
            #forward
            self.move(dt)
        if keys[pygame.K_s]:
            #backward
            self.move(-dt)
        
        if keys[pygame.K_SPACE]:
            #shoot
            self.shoot(dt)
        
    def shoot(self, dt):
        if self.shot_cooldown <= 0:
            # create a new bullet (shot) object
            forward = pygame.Vector2(0, 1).rotate(self.rotation) 
            a = self.position + forward * self.radius #top of the triangle
            bullet = Shot(a.x, a.y)
            #print(f"{self.velocity} {self.velocity.rotate(self.rotation)} {forward} {forward * PLAYER_SHOOT_SPEED}")
            bullet.velocity = self.velocity + (PLAYER_SHOOT_SPEED * forward * dt)
            
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN

# self.position + self vector2 coordinates to get new position

                      
    
