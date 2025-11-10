import pygame
import random
from constants import * 
from circleshape import CircleShape
from explosion import Explosion, Implosion

class Powerup(CircleShape):

    pu_types = { "H": "lime",
                 "S": "yellow",
                 "B": "orangered",
                 "L": "white" } 

    def __init__(self, x, y, type="H"):
        self.buffer = 20  # easier to pick up
        self.type = type
        self.font_size = 25
        self.pu_font = pygame.font.SysFont('arial', self.font_size)
        self.pu = self.pu_font.render(self.type, False, self.pu_types[self.type])
        (self.font_x, self.font_y) = self.pu_font.size(self.type) 
        super().__init__(x , y, 0.8 * self.font_size + self.buffer)
        self.life = random.randint(PU_MIN_TIME, PU_MAX_TIME)

    def update(self, dt):
        if self.life <= 0:
             self.explode()
             return
        self.life  -= dt
        self.position += self.velocity # * dt


    def draw(self, screen):
        pygame.draw.circle(screen, self.pu_types[self.type], self.position, self.radius - self.buffer, 3)
        screen.blit(self.pu, (self.position.x - self.font_x / 2, self.position.y - self.font_y / 2))

    def explode(self):
        _ = Explosion(self.position.x, self.position.y, self.radius - self.buffer, self.pu_types[self.type])
        self.kill()

    def implode(self):
        _ = Implosion(self.position.x, self.position.y, self.radius - self.buffer, self.pu_types[self.type])
        self.kill()

    def reward(self, player, gs):
        pu_score = 10

        match self.type:
            case "H":
                #print("H")
                #player.health += 5
                player.increase_health()
                gs.score_counter += pu_score #should call reward_score

            case "S":
                #print("S")
                #player.gun.upgrade()
                #player.level += 1
                #player.gun.upgrade()
                player.level_up()
                gs.score_counter += pu_score

            case "B":
                #print("B")
                #player.bomb_count += 1
                player.increase_bomb()
                gs.score_counter += pu_score

            case "L":
                #print("L")
                gs.life_counter += 1
                gs.score_counter += pu_score
                 
            case _:
                return