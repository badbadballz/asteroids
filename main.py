import sys 
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
#from circleshape import CircleShape

def main():
    
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
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

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    #updatable.add(player)
    #drawable.add(player)
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        #player.update(dt)
        updatable.update(dt)
        
        if Collisions_on:
            for ast in asteroids:
                if player.check_collision(ast):
                    print("Game over!")
                    sys.exit()
                for shot in shots:
                    if shot.check_collision(ast):
                        shot.kill()
                        ast.split()

       # if Bullet_collisions_on:
        #    for ast in asteroids:



        screen.fill(0)
        
        #player.draw(screen)
        for sp in drawable:
            sp.draw(screen)
        #drawable.draw(screen)
        #why the s loop works but drawable.draw(screen) doesn't?
        #updatable.draw(screen)


        pygame.display.flip()
        dt = clock.tick(60) / 1000 # how fast is this???
    
    


if __name__ == "__main__":
    main()
