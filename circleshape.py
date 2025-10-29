import pygame
from constants import * 

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        #oh ... Player.containers("")
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def check_collision(self, circleshape):
        distance_between = self.position.distance_to(circleshape.position)
        return (self.radius + circleshape.radius) > distance_between
    
    def out_of_bounds(self): # not used
        lower_left = pygame.Vector2()
        upper_right = pygame.Vector2()
        
        lower_left.xy = -(self.radius), SCREEN_HEIGHT + self.radius
        upper_right.xy = SCREEN_WIDTH + self.radius, -(self.radius)

        pos = self.position

        if (pos.x < lower_left.x or pos.x > upper_right.x 
            or pos.y < upper_right.y or pos.y > lower_left.y):
            return True
        else:
            return False    
    
    def flip_around_screen(self):
        buffer_exit = 7 # 10 seems to stop weird line artfacts
        buffer_entry = 1 # 5
    
        if self.position.x < 0 - self.radius - buffer_exit:
            self.position.x = SCREEN_WIDTH + self.radius + buffer_entry
            return
        if self.position.x > SCREEN_WIDTH + self.radius + buffer_exit:
            self.position.x = 0 - self.radius - buffer_entry
            return
        if self.position.y < 0 - self.radius - buffer_exit:
            self.position.y = SCREEN_HEIGHT + self.radius + buffer_entry
            return
        if self.position.y > SCREEN_HEIGHT + self.radius + buffer_exit:
            self.position.y = 0 - self.radius - buffer_entry
            return
                

       