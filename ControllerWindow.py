import arcade as a
from Constants import *

class ControllerWindow(a.Window):
    def __init__(self):
        self.screen_width = SCREEN_WIDTH // 4
        self.screen_height = SCREEN_HEIGHT // 2
        super().__init__(self.screen_width, self.screen_height, SCREEN_TITLE + " Control Panel")
        self.all_sprites = a.SpriteList()

        self.north_button = a.Sprite("assets/north.png", SCALING)
        self.north_button.center_x = self.screen_width / 2
        self.north_button.center_y = ( self.screen_height / 5 ) * 3
        self.all_sprites.append(self.north_button)

        self.south_button = a.Sprite("assets/south.png", SCALING)
        self.north_button.center_x = self.screen_width / 2
        self.north_button.center_y = ( self.screen_height / 5 ) * 1
        self.all_sprites.append(self.north_button)

        self.east_button = a.Sprite("assets/east.png", SCALING)
        self.north_button.center_x = ( self.screen_width / 4 ) * 3
        self.north_button.center_y = ( self.screen_height / 5 ) * 2
        self.all_sprites.append(self.north_button)

        self.west_button = a.Sprite("assets/west.png", SCALING)
        self.north_button.center_x = ( self.screen_width / 4 ) * 1
        self.north_button.center_y = ( self.screen_height / 5 ) * 2
        self.all_sprites.append(self.north_button)

        self.nuclear_1 = a.Sprite("assets/nuclear_inactive.png", SCALING)
        self.north_button.center_x = ( self.screen_width / 4 ) * 1
        self.north_button.center_y = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.north_button)

        self.nuclear_2 = a.Sprite("assets/nuclear_inactive.png", SCALING)
        self.north_button.center_x = ( self.screen_width / 4 ) * 2
        self.north_button.center_y = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.north_button)

        self.nuclear_3 = a.Sprite("assets/nuclear_inactive.png", SCALING)
        self.north_button.center_x = ( self.screen_width / 4 ) * 3
        self.north_button.center_y = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.north_button)

        self.heart_1 = a.Sprite("assets/heart_full.png", SCALING)
        self.north_button.center_x = ( self.screen_width / 4 ) * 2
        self.north_button.center_y = ( self.screen_height / 5 ) * 5
        self.all_sprites.append(self.north_button)

        self.heart_2 = a.Sprite("assets/heart_full.png", SCALING)
        self.north_button.center_x = ( self.screen_width / 4 ) * 3
        self.north_button.center_y = ( self.screen_height / 5 ) * 5
        self.all_sprites.append(self.north_button)

    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        pass