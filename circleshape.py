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
    
    def out_of_bounds(self): 
        buffer = self.radius * 2 
        lower_left = ( -(self.radius) + buffer, SCREEN_HEIGHT + self.radius - buffer) #pygame.Vector2()
        upper_right = (SCREEN_WIDTH + self.radius - buffer, -(self.radius) + buffer)#pygame.Vector2()
        
        pos = self.position

        if (pos.x < lower_left[0] or pos.x > upper_right[0]
            or pos.y < upper_right[1] or pos.y > lower_left[1]):
            return True
        else:
            return False    
    
    def flip_around_screen(self):
        buffer_exit = 0#self.radius # 4 seems to stop weird line artfacts
        buffer_entry = 0#self.radius # 2
    
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
                

       