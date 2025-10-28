import sys 
import pygame
import math
import random
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
#from circleshape import CircleShape

def main():
    time_counter = 0
    score_counter = 0 # score for game

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    
    pygame.font.init() # adding text?
    score_font = pygame.font.SysFont('arial', 30)
    timer_font = pygame.font.SysFont('arial', 30)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    #explosions = pygame.sprite.Group()

    # wtf???
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    
    #e = Explosion(250, 260, 50)
    #e = 1
    #c = 128
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        
        if Collisions_on:
            for ast in asteroids:
                if player.check_collision(ast) and Player_collisions_on:
                    #print("Game over!")
                    #sys.exit()
                    print(f"hit! @ {time_counter}")
                for shot in shots:
                    if shot.check_collision(ast):
                        e = Explosion(shot.position.x, shot.position.y, shot.radius)
                        shot.kill()
                        score_counter += ast.split()
                for other_ast in asteroids:
                    if ast is other_ast:
                        continue
                    else:
                        if ast.check_collision(other_ast) and random.randint(1, ASTEROID_COLLISION_RANDOM) == 1:
                            ast.split()
                            other_ast.split()

       # for e in explosions:
       #     if e.check_end():
       #        e.kill()   

        screen.fill(0)
        

        for sp in drawable:
              
            sp.flip_around_screen()
               #print (f"True {pos}")

            sp.draw(screen)
        #drawable.draw(screen)
        #why the s loop works but drawable.draw(screen) doesn't?
        #e.update(dt)
        #e.draw(screen)   
        
       # if e < 50:
       #     c += 0.5
       #     test = pygame.draw.circle(screen, (255, c, 0), (250,260), e  , 5)
       #     e += dt * 20
       # else:
       #     e = 0
       #     c = 128

        (score_x, _) = score_font.size(str(score_counter)) #is it efficent to run this all the time?
        score = score_font.render(str(score_counter), False, "white")
        screen.blit(score, (SCREEN_WIDTH - score_x ,0))

        f_time_counter = math.floor(time_counter)
        (timer_x, _) = score_font.size(str(f_time_counter)) 
        timer = timer_font.render(str(f_time_counter), False, "white")
        screen.blit(timer, ((SCREEN_WIDTH / 2) - (timer_x / 2) ,0))

        pygame.display.flip()

        dt = clock.tick(60) / 1000 
        time_counter += dt
    
        #print(math.floor(timer))
    


if __name__ == "__main__":
    main()
