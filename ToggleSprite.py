import arcade as a

class ToggleSprite(a.Sprite):
    def __init__(self, file_name, scale):
        super().__init__(file_name, scale)
        self.is_active = False