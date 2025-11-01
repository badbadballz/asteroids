import pygame
from circleshape import CircleShape
from shot import Shot
from explosion import Explosion
from constants import *

bomb_dp = 1000
bomb_radius = 200
bomb_colour = "orangered" #"mediumblue" #"yellow"
bomb_wave_width = 10
bomb_prog = 300


class Player(CircleShape):

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.rotate_speed = 0
        self.shot_cooldown = 0 #shot cooldown timer
        self.bomb_cooldown = 0
        self.health = PLAYER_HEALTH
        self.bomb_count = PLAYER_BOMB_COUNT
        self.shotpu = 0

# in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position - forward * self.radius
        b = self.position + forward * self.radius - right
        c = self.position + forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        if Draw_on:
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            a = self.position + forward * self.radius / 3
            b = self.position - forward * self.radius / 2
            pygame.draw.circle(screen, "red", a, self.radius / 3, 1) #3.8
            pygame.draw.circle(screen, "red", b, self.radius / 2, 1)
        
    def check_collision(self, circleshape):

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        a = self.position + forward * self.radius / 3
        b = self.position - forward * self.radius / 2
        a_radius = self.radius / 3
        b_radius = self.radius / 2

        distance_between_a = a.distance_to(circleshape.position)
        distance_between_b = b.distance_to(circleshape.position)
        
        return ((a_radius + circleshape.radius) > distance_between_a or
                (b_radius + circleshape.radius) > distance_between_b)

    def damage(self, dp):
        self.health -= dp
        if self.health <= 0:
             self.explode()
             return True # dead
        else:
            return False
        
    def explode(self):
         extra_boom = 15
         _ = Explosion(self.position.x, self.position.y, self.radius + extra_boom, "yellow", True, bomb_dp) 
         self.kill()


    def move(self, dt):

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_SPEED * dt

    def rotate(self, dt):
        #self.rotation += PLAYER_TURN_SPEED * dt
        self.rotate_speed += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        if self.shot_cooldown >= 0:
            self.shot_cooldown -= dt 
        if self.bomb_cooldown >= 0:
            self.bomb_cooldown -= dt
        
        self.position += self.velocity
        self.rotation += self.rotate_speed
        
        #print(f"{self.position} {self.out_of_bounds()}")

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            # left
            self.rotate(-dt)
        if keys[pygame.K_d]:
            # right
            self.rotate(dt)
        if keys[pygame.K_w]:
            #forward
            self.move(-dt)
        if keys[pygame.K_s]:
            #backward
            self.move(dt)
        if keys[pygame.K_SPACE]:
            #shoot
            self.shoot(dt)
        if keys[pygame.K_TAB]:
            #bomb
            self.bomb()
        
    def shoot(self, dt):
        if self.shot_cooldown <= 0:
            # create a new bullet (shot) object
            forward = pygame.Vector2(0, 1).rotate(self.rotation) 
            a = self.position - forward * self.radius #top of the triangle
            bullet = Shot(a.x, a.y)
            #print(f"{self.velocity} {self.velocity.rotate(self.rotation)} {forward} {forward * PLAYER_SHOOT_SPEED}")
            bullet.velocity = self.velocity + (PLAYER_SHOOT_SPEED * forward * -dt)
            
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN

    def bomb(self): # add player velocity
        # needs a buffer to stop spam
        if self.bomb_cooldown <= 0 and self.bomb_count > 0:
            forward = pygame.Vector2(0, 1).rotate(self.rotation) 
            
            bomb = Explosion(self.position.x, self.position.y, self.radius + bomb_radius, bomb_colour, True, bomb_dp)
            bomb.width = bomb_wave_width
            bomb.propagation = bomb_prog
            #bomb.collision_on = True
            #bomb.dp = bomb_dp
            bomb.velocity = self.velocity
            if not Infinite_bombs:
                self.bomb_count -= 1
            self.bomb_cooldown = PLAYER_BOMB_COOLDOWN



                      
 
