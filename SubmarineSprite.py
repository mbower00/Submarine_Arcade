import arcade as a
from Constants import *

class SubmarineSprite(a.Sprite):
    # some of the __init__ and the super __init__ was auto generated
    def __init__(self, filename: str = None, scale: float = 1):
        super().__init__(filename, scale)
        self.did_move = True
        self.selected_move = ""
        self.is_move_selected = False
        self.torpedo_position = None
        self.is_destroyed = False
    
    def update_animation(self, delta_time: float = 1 / 60):
        return super().update_animation(delta_time)
    
    def update(self):
        super().update()

        # correct off screen positioning
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.left < 0:
            self.left = 0

        # set velocity back to 0
        self.change_y = 0
        self.change_x = 0