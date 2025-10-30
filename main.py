import sys
import pygame
import math

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion

def main():
    time_counter = 0
    score_counter = 0 # score for game
    life_counter = PLAYER_LIFE   
    game_over = False

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    
    pygame.font.init() 
    game_font = pygame.font.SysFont('arial', 30)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # wtf???
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    health_counter = player.health
  
    (_, health_y) = game_font.size(str(health_counter)) 
    
    _ = AsteroidField()
    
    dead_timer = 0
    dead = False
    reset = False
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        
        if Collisions_on: 
            for ast in asteroids:
                if player.check_collision(ast) and Player_collisions_on:
                    if  health_counter > 0:
                        health_counter = player.damage(COLLISION_DP * dt)
                        #print (f"health_counter: {health_counter}")
                        ast.damage(COLLISION_DP * dt)
                    else:
                        dead = True    
                            
                for shot in shots:
                    if shot.check_collision(ast):
                        shot.explode()
                        score_counter += ast.damage(shot.dp) 
                for other_ast in asteroids:
                    if ast is other_ast:
                        continue
                    else:
                        if ast.check_collision(other_ast):
                            ast.damage(COLLISION_DP * dt)
                            other_ast.damage(COLLISION_DP * dt)
                           
        screen.fill(0)
    
        for sp in drawable:
            sp.flip_around_screen()
            sp.draw(screen)

        (score_x, _) = game_font.size(str(score_counter)) #is it efficent to run this all the time?
        score = game_font.render(str(score_counter), False, "white")
        screen.blit(score, (SCREEN_WIDTH - score_x ,0))

        f_time_counter = math.floor(time_counter)
        (timer_x, _) = game_font.size(str(f_time_counter)) 
        timer = game_font.render(str(f_time_counter), False, "white")
        screen.blit(timer, ((SCREEN_WIDTH / 2) - (timer_x / 2) ,0))

        c_health_counter = math.ceil(health_counter) 
        health = game_font.render(str(c_health_counter), False, "white")
        screen.blit(health, (0 , SCREEN_HEIGHT - health_y))

        life = game_font.render(str(life_counter), False, "white")
        screen.blit(life, (0, 0))

        if dead:
            if life_counter <= 0:
                game_over = True
                keys = pygame.key.get_pressed()
                
                f_time_counter = math.floor(time_counter)
                text1 = "Game Over"
                text2 = f"Score: {f_time_counter + score_counter}"
                (over_x1, over_y1) = game_font.size(str(text1))
                (over_x2, over_y2) = game_font.size(str(text2))
                over_text1 = game_font.render(str(text1), False, "white")
                screen.blit(over_text1, ((SCREEN_WIDTH / 2 - over_x1 / 2, SCREEN_HEIGHT / 2 - over_y1 / 2)))
                over_text2 = game_font.render(str(text2), False, "white")
                screen.blit(over_text2, ((SCREEN_WIDTH / 2 - over_x2 / 2, SCREEN_HEIGHT / 2 + over_y2 / 2)))

                if keys[pygame.K_r]:
                    #print("reset")
                    reset = True


            elif dead_timer < 3:
                dead_timer += dt
                #print(f"dead @ {dead_timer}")
               
            elif life_counter > 0:
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                health_counter = player.health 
                dead_timer = 0
                dead = False
                if not Infinite_lives:
                    life_counter -= 1

        pygame.display.flip()   

        dt = clock.tick(60) / 1000 
        if not game_over:
            time_counter += dt 

        if reset:
            updatable.empty()
            drawable.empty()
            asteroids.empty()
            shots.empty()

            _ = AsteroidField()
            player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            
            health_counter = player.health
            life_counter = PLAYER_LIFE
            reset = False
            game_over = False
            dead = False
            dead_timer = 0
            time_counter = 0
            score_counter = 0
            
            


if __name__ == "__main__":
    main()
