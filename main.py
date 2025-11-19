#import sys
import pygame
import math
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion, Implosion
from powerup import Powerup
from game_state import Game_state
from logger import log_state


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

        bomb = game_font.render(str(f"B: {gs.bomb_counter}"), False, "orangered")
        screen.blit(bomb, (0, SCREEN_HEIGHT - gs.font_y * 2))

        if gs.level_counter >= MAX_LEVEL:
             level = game_font.render(("S: MAX!"), False, max_colour) 
        else:    
            level = game_font.render(str(f"S: {gs.level_counter}"), False, "yellow")
        screen.blit(level, (0, SCREEN_HEIGHT - gs.font_y * 3))

        life = game_font.render(str(f"L: {gs.life_counter}"), False, "white")
        screen.blit(life, (0, 0))



def draw_gameover(screen, game_font, gs):
        f_time_counter = math.floor(gs.time_counter)
        text1 = "Game Over"
        f_time = f"Time: {f_time_counter}"
        diff = f"Difficulity: {gs.difficulty}"
        p_level = f"Level: {gs.level_counter}"
        text2 = f"Score: {(f_time_counter + gs.score_counter + gs.level_counter) * (1 + gs.difficulty)}" # havent done final score yet
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
    #pygame.mixer.pre_init(44100,32,1, 1024)

    pygame.init()
    pygame.font.init() 
    pygame.mixer.init()
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
    Implosion.containers = (gs.updatable, gs.drawable)
    Powerup.containers = (gs.powerups, gs.updatable, gs.drawable)
    
    player = gs.new_game()
  
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        log_state()

        gs.updatable.update(dt)
        
        if Collisions_on: 
            for ast in gs.asteroids:
                if not gs.dead and Player_collisions_on and (not gs.is_invulnerable()) and player.check_collision(ast):
                    gs.dead = player.damage(COLLISION_DP * dt, gs.spawn_powerup)
                        #print (f"health_counter: {health_counter}")   
                    ast.damage(COLLISION_DP * dt, "explode")
                    if gs.dead == True:
                        respawn_time = gs.time_counter + PLAYER_RESPAWN_LAG
                        gs.reset_d_interval() # reset the timer for increasing difficulty
                for shot in gs.shots:
                    if shot.check_collision(ast):
                        shot.explode()
                        #gs.score_counter += 
                        ast.damage(shot.dp, "explode", gs.spawn_powerup, gs.reward_score) 
                for explosion in gs.explosions:
                    if explosion.collision_on and explosion.check_collision(ast): # explosions only kill asteroids
                        if not explosion.no_score:
                            #print("damage from ex, score")
                            ast.damage(explosion.dp * dt, "explode", gs.spawn_powerup, gs.reward_score)
                        else:
                            ast.damage(explosion.dp * dt, "explode", gs.spawn_powerup)
                             #gs.score_counter += 0
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
                    pu.implode() #make inverse explosion


        gs.update_player_info(player)   
                    
        screen.fill(0)
        
       
        for sp in gs.drawable:
            sp.flip_around_screen()
            sp.draw(screen)
       
        
        draw_score(screen, game_font, gs)
        k = pygame.key.get_pressed()
        if k[pygame.K_x]:
            gs.game_sounds.play_sound(6)
            print("playing sound")

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

        if not gs.game_over:
            gs.time_counter += dt # increment timer
            gs.calculate_difficulty()
            #print(gs.time_counter)

        pygame.display.flip()   

        dt = clock.tick(120) / 1000
        

        if gs.reset:
            player = gs.new_game()
                    
            
if __name__ == "__main__":
    main()
