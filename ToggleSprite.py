# used arcade code from https://realpython.com/arcade-python-game-framework/ 

import arcade as a

class ToggleSprite(a.Sprite):
    """A sprite with an is_active member variable that can toggled.
    """
    def __init__(self, file_name, scale):
        """ToggleSprite constructor. Sets the is_active member variable to False

        Args:
            file_name (_type_): sprite image file
            scale (_type_): scaling of the image
        """
        super().__init__(file_name, scale)
        self.is_active = False