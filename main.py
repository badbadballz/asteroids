import sys
import pygame
import math
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion
from powerup import Powerup
from game_state import Game_state


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
        #(_, font_y) = game_font.size(str(gs.health_counter)) 
        health = game_font.render(str (f"H: {c_health_counter}"), False, "lime")
        screen.blit(health, (0 , SCREEN_HEIGHT - gs.font_y))

        bomb = game_font.render(str(gs.bomb_counter), False, "white")
        screen.blit(bomb, (0, SCREEN_HEIGHT - gs.font_y * 2))

        life = game_font.render(str(gs.life_counter), False, "white")
        screen.blit(life, (0, 0))



def draw_gameover(screen, game_font, gs):
        f_time_counter = math.floor(gs.time_counter)
        text1 = "Game Over"
        text2 = f"Score: {f_time_counter + gs.score_counter}"
        (over_x1, over_y1) = game_font.size(text1)
        (over_x2, over_y2) = game_font.size(text2)
        over_text1 = game_font.render(str(text1), False, "white")
        screen.blit(over_text1, ((SCREEN_WIDTH / 2 - over_x1 / 2, SCREEN_HEIGHT / 2 - over_y1 / 2)))
        over_text2 = game_font.render(str(text2), False, "white")
        screen.blit(over_text2, ((SCREEN_WIDTH / 2 - over_x2 / 2, SCREEN_HEIGHT / 2 + over_y2 / 2)))

def main():

    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print("W, A, S, D to move, SPACE to shoot, TAB to bomb")
    print("Press R to Restart after Game Over")
    print("Press C to Continue after Game Over")
    
    pygame.init()
    pygame.font.init() 
    game_font = pygame.font.SysFont('arial', 30)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    gs = Game_state()
    (_, gs.font_y) = game_font.size(str("0")) 
   
    Player.containers = (gs.updatable, gs.drawable)
    Asteroid.containers = (gs.asteroids, gs.updatable, gs.drawable)
    AsteroidField.containers = (gs.updatable)
    Shot.containers = (gs.shots, gs.updatable, gs.drawable)
    Explosion.containers = (gs.explosions, gs.updatable, gs.drawable)
    Powerup.containers = (gs.powerups, gs.updatable, gs.drawable)

    gs.new_game()
    player = gs.respawn() # consider new game and respawning @ same method

    #test = Powerup(200, 200, "H") # letters not centered


    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
          
        gs.updatable.update(dt)
        
        if Collisions_on: 
            for ast in gs.asteroids:
                if not gs.dead and Player_collisions_on and player.check_collision(ast):
                    #if  gs.health_counter > 0: 
                    gs.dead = player.damage(COLLISION_DP * dt)
                        #print (f"health_counter: {health_counter}")
                       
                    ast.damage(COLLISION_DP * dt, "explode")
                    #if player.health <= 0: #gs.health_counter <= 0:, possible issue of called killed player to get .health?
                    if gs.dead == True:
                        respawn_time = gs.time_counter + PLAYER_RESPAWN_LAG 
                for shot in gs.shots:
                    if shot.check_collision(ast):
                        shot.explode()
                        gs.score_counter += ast.damage(shot.dp, "explode", gs.reward_powerup) 
                for explosion in gs.explosions:
                    if explosion.collision_on and explosion.check_collision(ast): # explosions only kill asteroids
                        sc = ast.damage(explosion.dp * dt, "explode", gs.reward_powerup)
                        if not explosion.no_score:
                             gs.score_counter += sc
                for other_ast in gs.asteroids:
                    if ast is other_ast:
                        continue
                    else:
                        if ast.check_collision(other_ast):
                            ast.damage(COLLISION_DP * dt)
                            other_ast.damage(COLLISION_DP * dt)
        if not gs.dead:
            for pu in gs.powerups:
                #print(len(gs.powerups))
                if player.check_collision(pu):
                    pu.reward(player, gs)
                    pu.explode() #make inverse explosion


        gs.update_player_info(player)             
                     
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
                if keys[pygame.K_c]:
                    player = gs.respawn()
                    gs.life_counter = PLAYER_LIFE
                    gs.game_over = False
               
            elif gs.life_counter > 0 and gs.time_counter > respawn_time:
                player = gs.respawn()
                if not Infinite_lives:
                    gs.life_counter -= 1

         # maybe just moving the clock before flip() was the key to getting rid of the line artifacts? nope...
        if not gs.game_over:
            gs.time_counter += dt 
        
        pygame.display.flip()   

        dt = clock.tick(120) / 1000
        
        if gs.reset:
            gs.new_game()
            player = gs.respawn()
       
            
            
if __name__ == "__main__":
    main()
