# used arcade code from https://realpython.com/arcade-python-game-framework/ 

import arcade as a
from Constants import *

class SubmarineSprite(a.Sprite):
    """A submarine sprite class. Child of a.Sprite (a is arcade).
    """
    # some of the __init__ and the super __init__ was auto generated
    def __init__(self, filename: str = None, scale: float = 1):
        super().__init__(filename, scale)
        self.did_move = True
        self.selected_move = ""
        self.is_move_selected = False
        self.torpedo_position = None
        self.is_destroyed = False
    
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