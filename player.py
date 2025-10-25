import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.rotate_speed = 0
        self.timer = 0 #shot cooldown timer

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
        #self.position += self.velocity

    def rotate(self, dt):
        #self.rotation += PLAYER_TURN_SPEED * dt
        self.rotate_speed += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.timer -= dt
        self.position += self.velocity
        self.rotation += self.rotate_speed
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
            self.shoot()
        
    def shoot(self):
        if self.timer <= 0:
            # create a new bullet (shot) object
            forward = pygame.Vector2(0, 1).rotate(self.rotation) 
            a = self.position + forward * self.radius #top of the triangle
            bullet = Shot(a.x, a.y)
            bullet.velocity = forward * PLAYER_SHOOT_SPEED #why no * dt?
            self.timer = PLAYER_SHOOT_COOLDOWN


                      
    
