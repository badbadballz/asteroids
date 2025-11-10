import pygame
import math
from circleshape import CircleShape
from shot import Shot
from explosion import Explosion
from constants import *

#lvl 10, bomb suck pu, lvl 20, explosive shot,  lvl max/30, blue mediumblue, dodgerblue

bomb_dp = 100 #1000
bomb_radius = 100 #200
bomb_colour = "orangered" #"mediumblue" #"yellow"
bomb_wave_width = 10 #10
bomb_prog = 300 #300


min_cooldown = 0.05
d_cooldown = 0.01
d_life = 0.05
d_dp = 2
d_radius = 1
max_radius = 6
d_speed = 20

#starting_level = 30 

# Player lvl: 0, cooldown: 0.3, life: 0.9, dp: 10, rad: 3 speed: 351
# Player lvl: 30, cooldown: 0.05, life: 1.65, dp: 70, rad: 6 speed: 651 / exploding shot dp may be too low!

class Gun(): #odd speed, even life
    def __init__(self, player):
        self.player = player
        l = self.player.level / 2
        self.shot_timer = 0
        self.shot_cooldown = max(PLAYER_SHOOT_COOLDOWN - (d_cooldown * self.player.level), min_cooldown) #for testing
        self.shot_life = SHOT_LIFE  + (d_life * math.floor(l))#self.player.level)
        self.shot_dp = SHOT_DAMAGE + (d_dp * self.player.level)
        self.shot_radius = SHOT_RADIUS + min(self.player.level // 10, 3)
        self.shot_speed = PLAYER_SHOOT_SPEED + (d_speed * math.ceil(l) + 1)#self.player.level)
    
        #print(f"Player lvl: {self.player.level}, cooldown: {self.shot_cooldown}, life: {self.shot_life}, dp: {self.shot_dp}, rad: {self.shot_radius} speed: {self.shot_speed}")

    def fire(self, dt):
        if self.shot_timer <= 0:
            # create a new bullet (shot) object
            forward = pygame.Vector2(0, 1).rotate(self.player.rotation) 
            a = self.player.position - forward * self.player.radius #top of the triangle
            #(self, x, y, radius, life, dp, explode_damage=False, explode_dp=0):
            if self.player.level >= MAX_LEVEL: # lvl 30 / max / check if this scales down after death
                #print("max!")
                max_shot_dp = self.shot_dp * 1.2
                max_explode_dp = max_shot_dp
                max_shot_cooldown = self.shot_cooldown / 1.1
                bullet = Shot(a.x, a.y, self.shot_radius, self.shot_life, max_shot_dp, explode_damage=True, explode_dp=max_explode_dp , max=True)
                self.shot_timer = max_shot_cooldown
            elif self.player.level >= 20: # level 20 upgrade explosive shot
                bullet = Shot(a.x, a.y, self.shot_radius, self.shot_life, self.shot_dp, explode_damage=True, explode_dp=self.shot_dp)
                self.shot_timer = self.shot_cooldown
            else:
                #print("No power")
                bullet = Shot(a.x, a.y, self.shot_radius, self.shot_life, self.shot_dp)
                self.shot_timer = self.shot_cooldown
            #print(f"{self.velocity} {self.velocity.rotate(self.rotation)} {forward} {forward * PLAYER_SHOOT_SPEED}")
            bullet.velocity = self.player.velocity + (self.shot_speed * forward * -dt)
            
            
            

    def upgrade(self):
        
        if self.shot_cooldown > min_cooldown: # limit!
             self.shot_cooldown -= d_cooldown 
        if self.player.level % 2 == 0:
             self.shot_life += d_life
        elif self.player.level % 2 == 1:
             self.shot_speed += d_speed 
        self.shot_dp += d_dp 
        if self.shot_radius < max_radius and self.player.level % 10 == 0:
            self.shot_radius += 1 
            
                  
     
        #print(f"Player lvl: {self.player.level}, cooldown: {self.shot_cooldown}, life: {self.shot_life}, dp: {self.shot_dp}, rad: {self.shot_radius} speed: {self.shot_speed}")

class Player(CircleShape):

    def __init__(self, x, y, level=0): # changed to start at level 1
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.rotate_speed = 0
        self.shot_cooldown = 0 #shot cooldown timer
        self.bomb_cooldown = 0
        self.health = PLAYER_HEALTH
        self.bomb_count = PLAYER_BOMB_COUNT
        self.level = level
        #print(f"new player with level:{self.level}")
        self.gun = Gun(self)
       

# in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position - forward * self.radius
        b = self.position + forward * self.radius - right
        c = self.position + forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        line = min(5, 2 + int((self.health - PLAYER_HEALTH) // 10))
        pygame.draw.polygon(screen, "white", self.triangle(), line)
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

    def damage(self, dp, rewardfunction):
        self.health -= dp
        if self.health <= 0:
             self.level -= rewardfunction(self, "player") # minus the level, gives corresponding powerups in death
             #print(f"player l after death = - {level}")
             #self.level -= int(deduct_lvl)
             self.explode()
             return True # dead
        else:
            return False
        
    def explode(self): #release Ss
         extra_boom = 20
         _ = Explosion(self.position.x, self.position.y, self.radius + extra_boom, "yellow", True, 1000)#bomb_dp) 
         self.kill()


    def move(self, dt):

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_SPEED * dt

    def rotate(self, dt):
        #self.rotation += PLAYER_TURN_SPEED * dt
        self.rotate_speed += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        if self.gun.shot_timer >= 0:
            self.gun.shot_timer -= dt 
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
        self.gun.fire(dt)
        
    def bomb(self):
        d_radius = 10
        d_dp = 10

        if self.bomb_cooldown <= 0 and self.bomb_count > 0:
            if self.level >= MAX_LEVEL:
                bomb = Explosion(self.position.x, self.position.y, self.radius + bomb_radius + (d_radius * self.level) * 1.1, max_bomb_colour, True, bomb_dp + (d_dp * self.level))
            else:
                bomb = Explosion(self.position.x, self.position.y, self.radius + bomb_radius + (d_radius * self.level), bomb_colour, True, bomb_dp + (d_dp * self.level))
            bomb.width = bomb_wave_width
            bomb.propagation = bomb_prog
            
            bomb.velocity = self.velocity
            if not Infinite_bombs:
                self.bomb_count -= 1
            self.bomb_cooldown = PLAYER_BOMB_COOLDOWN

    def level_up(self): # max level 30
        if self.level < MAX_LEVEL:
            self.level += 1
            self.gun.upgrade()
    
    def increase_health(self): #max health 100
        d_health = 5
        if self.health < MAX_HEALTH:
            self.health += d_health

    def increase_bomb(self): #max bomb 10
        if self.bomb_count < MAX_BOMB:
            self.bomb_count += 1


                      
 
