import arcade as a
from Constants import *

class ControllerWindow(a.Window):
    def __init__(self):
        self.screen_width = SCREEN_WIDTH // 2
        self.screen_height = ( SCREEN_HEIGHT // 3 ) * 2
        super().__init__(self.screen_width, self.screen_height, "Control Panel")

        a.set_background_color(a.color_from_hex_string(PALETTE_BLUE.upper()))

        self.all_sprites = a.SpriteList()

        self.north_button = a.Sprite("assets/north.png", SCALING)
        self.north_button.center_x = self.screen_width / 2
        self.north_button.top = ( self.screen_height / 5 ) * 3
        self.all_sprites.append(self.north_button)

        self.south_button = a.Sprite("assets/south.png", SCALING)
        self.south_button.center_x = self.screen_width / 2
        self.south_button.top = ( self.screen_height / 5 ) * 1
        self.all_sprites.append(self.south_button)

        self.east_button = a.Sprite("assets/east.png", SCALING)
        self.east_button.center_x = ( self.screen_width / 4 ) * 3
        self.east_button.top = ( self.screen_height / 5 ) * 2
        self.all_sprites.append(self.east_button)

        self.west_button = a.Sprite("assets/west.png", SCALING)
        self.west_button.center_x = ( self.screen_width / 4 ) * 1
        self.west_button.top = ( self.screen_height / 5 ) * 2
        self.all_sprites.append(self.west_button)

        self.nuclear_1 = a.Sprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_1.center_x = ( self.screen_width / 4 ) * 1
        self.nuclear_1.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_1)

        self.nuclear_2 = a.Sprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_2.center_x = ( self.screen_width / 4 ) * 2
        self.nuclear_2.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_2)

        self.nuclear_3 = a.Sprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_3.center_x = ( self.screen_width / 4 ) * 3
        self.nuclear_3.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_3)

        self.heart_1 = a.Sprite("assets/heart_full.png", SCALING)
        self.heart_1.center_x = ( self.screen_width / 6 ) * 2
        self.heart_1.top = ( self.screen_height / 5 ) * 5 - 10
        self.all_sprites.append(self.heart_1)

        self.heart_2 = a.Sprite("assets/heart_full.png", SCALING)
        self.heart_2.center_x = ( self.screen_width / 6 ) * 4
        self.heart_2.top = ( self.screen_height / 5 ) * 5 - 10
        self.all_sprites.append(self.heart_2)

    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        pass

    def on_draw(self):
        a.start_render()
        self.all_sprites.draw()