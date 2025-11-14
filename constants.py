SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ASTEROID_MIN_RADIUS = 20 # 20
ASTEROID_KINDS = 4 # 3
ASTEROID_SPAWN_RATE = 5 # seconds # 5
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_SPLIT_ACC = 1.2
ASTEROID_BASE_ROTATE_SPEED = 50 
ASTEROID_ROTATE_SPEED_RANDOM = 5
AST_LIMIT = 5
BASE_ARMOR = 9
CHANCE_ARMOR_AST = 2 # 2 /10 chance

PLAYER_RADIUS = 20 #20
PLAYER_TURN_SPEED = 3 #4
PLAYER_SPEED = 2.5 #5
PLAYER_SHOOT_SPEED = 350 
PLAYER_SHOOT_COOLDOWN = 0.3
PLAYER_BOMB_COOLDOWN = 0.8
PLAYER_BOMB_COUNT = 2
PLAYER_HEALTH = 10
PLAYER_LIFE = 1
PLAYER_RESPAWN_LAG = 2
INVULNERABLE_TIME  = 3 # after respawn

SHOT_RADIUS = 3
SHOT_LIFE = 0.9
SHOT_DAMAGE = 10

COLLISION_DP = 20
RESPAWN_BOOM = 99999

PU_MAX_TIME = 30
PU_MIN_TIME = 15
PU_SPLIT_ACC = 1.3
PU = ["H", "S", "B", "L"]
PU_WEIGHTS = [40,35,15,10] # H, S, B, L
BASE_AST_PU_CHANCE = 10
MAX_PU_NUM = 3  
CHANCE_TO_SPAWN_PU_NO_PU = 3 # 1 in N chance to spawn "S" PU when no other PU on screen
PU_SPAWN_RATE = 5

Infinite_lives = False
Infinite_bombs = True
Collisions_on = True
Player_collisions_on = False
Draw_on = False
#Bullet_collisions_on = True


MAX_HEALTH = 100
#max_level = 30
MAX_LEVEL = 30
MAX_BOMB = 10

max_colour = "lightblue"
max_bomb_colour = "mediumblue"

#(ast spawn rate, 0 ast modifier, 0 boss ast)    (min start time, min level)
difficulty_event = {    0 : (ASTEROID_SPAWN_RATE, 0, 0, 0, 0),
                        1 : (ASTEROID_SPAWN_RATE, 0, 0, 0, 0)
                    }

MAX_DIFF_LEVEL = 18
D_TIME_INTERVAL = 70 #60
level_interval = 5
