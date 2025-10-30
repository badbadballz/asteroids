import sys
import pygame
import math

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion


class Game_state():
    def __init__(self):
        self.__reset_state()

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

    def __reset_state(self):
        self.reset = False
        self.game_over = False
        self.dead = False
        self.dead_timer = 0
        self.health_counter = PLAYER_HEALTH
        self.life_counter = PLAYER_LIFE
        self.time_counter = 0
        self.score_counter = 0

    def __empty_groups(self):
        self.updatable.empty()
        self.drawable.empty()
        self.asteroids.empty()
        self.shots.empty()

    def new_game(self):
        self.__empty_groups()
        self.__reset_state()
        _ = AsteroidField()

    def respawn(self):
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.health_counter = PLAYER_HEALTH
        self.dead_timer = 0
        self.dead = False
        return player

def draw_score(screen, game_font, gs):
        #only need to get font sizes once for health counter

        (score_x, _) = game_font.size(str(gs.score_counter)) #is it efficent to run this all the time?
        score = game_font.render(str(gs.score_counter), False, "white")
        screen.blit(score, (SCREEN_WIDTH - score_x ,0))

        f_time_counter = math.floor(gs.time_counter)
        (timer_x, _) = game_font.size(str(f_time_counter)) 
        timer = game_font.render(str(f_time_counter), False, "white")
        screen.blit(timer, ((SCREEN_WIDTH / 2) - (timer_x / 2) ,0))

        c_health_counter = math.ceil(gs.health_counter) 
        (_, health_y) = game_font.size(str(gs.health_counter)) 
        health = game_font.render(str(c_health_counter), False, "white")
        screen.blit(health, (0 , SCREEN_HEIGHT - health_y))

        life = game_font.render(str(gs.life_counter), False, "white")
        screen.blit(life, (0, 0))

def draw_gameover(screen, game_font, gs):
        f_time_counter = math.floor(gs.time_counter)
        text1 = "Game Over"
        text2 = f"Score: {f_time_counter + gs.score_counter}"
        (over_x1, over_y1) = game_font.size(str(text1))
        (over_x2, over_y2) = game_font.size(str(text2))
        over_text1 = game_font.render(str(text1), False, "white")
        screen.blit(over_text1, ((SCREEN_WIDTH / 2 - over_x1 / 2, SCREEN_HEIGHT / 2 - over_y1 / 2)))
        over_text2 = game_font.render(str(text2), False, "white")
        screen.blit(over_text2, ((SCREEN_WIDTH / 2 - over_x2 / 2, SCREEN_HEIGHT / 2 + over_y2 / 2)))

def main():

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()
    pygame.font.init() 
    game_font = pygame.font.SysFont('arial', 30)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    gs = Game_state()
   
    Player.containers = (gs.updatable, gs.drawable)
    Asteroid.containers = (gs.asteroids, gs.updatable, gs.drawable)
    AsteroidField.containers = (gs.updatable)
    Shot.containers = (gs.shots, gs.updatable, gs.drawable)
    Explosion.containers = (gs.updatable, gs.drawable)

    gs.new_game()
    player = gs.respawn()

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        gs.updatable.update(dt)
        
        if Collisions_on: 
            for ast in gs.asteroids:
                if not gs.dead and Player_collisions_on and player.check_collision(ast):
                    if  gs.health_counter > 0: 
                        gs.health_counter = player.damage(COLLISION_DP * dt)
                        #print (f"health_counter: {health_counter}")
                        ast.damage(COLLISION_DP * dt)
                    else:
                        gs.dead = True    
                            
                for shot in gs.shots:
                    if shot.check_collision(ast):
                        shot.explode()
                        gs.score_counter += ast.damage(shot.dp) 
                for other_ast in gs.asteroids:
                    if ast is other_ast:
                        continue
                    else:
                        if ast.check_collision(other_ast):
                            ast.damage(COLLISION_DP * dt)
                            other_ast.damage(COLLISION_DP * dt)
                           
        screen.fill(0)
    
        for sp in gs.drawable:
            sp.flip_around_screen()
            sp.draw(screen)

        draw_score(screen, game_font, gs)

        if gs.dead:
            if gs.game_over or gs.life_counter <= 0:
                gs.game_over = True
                draw_gameover(screen, game_font, gs)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:  
                    gs.reset = True

            elif gs.dead_timer < 3:
                gs.dead_timer += dt
               
            elif gs.life_counter > 0:
                player = gs.respawn()
                if not Infinite_lives:
                    gs.life_counter -= 1

        pygame.display.flip()   

        dt = clock.tick(60) / 1000 
        if not gs.game_over:
            gs.time_counter += dt 

        if gs.reset:
            gs.new_game()
            player = gs.respawn()
            
            
if __name__ == "__main__":
    main()
