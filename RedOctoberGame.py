from calendar import c
import random
import time
from turtle import right
import arcade as a
import socket as so
import threading as th
from Constants import *
from RadioOpperator import RadioOpperator
from ToggleSprite import ToggleSprite
from SubmarineSprite import SubmarineSprite
import json


class RedOctoberGame(a.Window):
    def __init__(self, ip, enemy_ip):
        self.screen_width = SCREEN_WIDTH + (SCREEN_WIDTH // 2)
        self.screen_height = SCREEN_HEIGHT
        super().__init__(self.screen_width, self.screen_height, SCREEN_TITLE)
        self.all_sprites = a.SpriteList()
        self.island_sprites = a.SpriteList()
        self.white_trail_sprites = a.SpriteList()
        self.red_trail_sprites = a.SpriteList()
        self.ip = ip
        self.enemy_ip = enemy_ip
        self.lock = th.Lock()
        self.radio_opperator = RadioOpperator(self.ip, self.lock)
        self.sending_socket = so.socket()
        self.reactor_tick = 0
        self.is_playing = True
        self.torpedo_tick = 0

    def setup(self):
        a.set_background_color(a.color_from_hex_string(PALETTE_BLUE.upper()))

        self.mark = a.Sprite("assets/mark.png", SCALING)
        self.mark.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
        self.mark.bottom = 0 + 10
        self.all_sprites.append(self.mark)

        self.fire = a.Sprite("assets/fire.png", SCALING)
        self.fire.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
        self.fire.center_y = ( self.screen_height / 6 ) * 2
        self.all_sprites.append(self.fire)

        self.north_button = a.Sprite("assets/north.png", SCALING)
        self.north_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
        self.north_button.top = ( self.screen_height / 6 ) * 3
        self.all_sprites.append(self.north_button)

        self.south_button = a.Sprite("assets/south.png", SCALING)
        self.south_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
        self.south_button.bottom = ( self.screen_height / 6 ) * 1
        self.all_sprites.append(self.south_button)

        self.east_button = a.Sprite("assets/east.png", SCALING)
        self.east_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
        self.east_button.center_y = ( self.screen_height / 6 ) * 2
        self.all_sprites.append(self.east_button)

        self.west_button = a.Sprite("assets/west.png", SCALING)
        self.west_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
        self.west_button.center_y = ( self.screen_height / 6 ) * 2
        self.all_sprites.append(self.west_button)

        self.nuclear_1 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
        self.nuclear_1.top = (( self.screen_height / 6 ) * 5 )
        self.all_sprites.append(self.nuclear_1)

        self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
        self.nuclear_2.top = (( self.screen_height / 6 ) * 5 )
        self.all_sprites.append(self.nuclear_2)

        self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
        self.nuclear_3.top = (( self.screen_height / 6 ) * 5 )
        self.all_sprites.append(self.nuclear_3)
        
        self.torpedo_segment_1 = ToggleSprite("assets/torpedo_segment_1_inactive.png", SCALING)
        self.torpedo_segment_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
        self.torpedo_segment_1.top = (( self.screen_height / 6 ) * 4 )
        self.all_sprites.append(self.torpedo_segment_1)

        self.torpedo_segment_2 = ToggleSprite("assets/torpedo_segment_2_inactive.png", SCALING)
        self.torpedo_segment_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
        self.torpedo_segment_2.top = (( self.screen_height / 6 ) * 4 ) - 2
        self.all_sprites.append(self.torpedo_segment_2)

        self.torpedo_segment_3 = ToggleSprite("assets/torpedo_segment_3_inactive.png", SCALING)
        self.torpedo_segment_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
        self.torpedo_segment_3.top = (( self.screen_height / 6 ) * 4 ) - 2
        self.all_sprites.append(self.torpedo_segment_3)

        self.heart_1 = ToggleSprite("assets/heart_full.png", SCALING)
        self.heart_1.is_active = True
        self.heart_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*2)
        self.heart_1.top = ( self.screen_height / 6 ) * 6 - 10
        self.all_sprites.append(self.heart_1)

        self.heart_2 = ToggleSprite("assets/heart_full.png", SCALING)
        self.heart_2.is_active = True
        self.heart_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*4)
        self.heart_2.top = ( self.screen_height / 6 ) * 6 - 10
        self.all_sprites.append(self.heart_2)

        # island_positions = [14, 10, 15, 11, 24, 20, 1, 27, 2, 24, 16, 12, 16, 7, 16, 9, 16, 30, 15, 10, 20, 7, 24, 19, 12, 24, 30, 7, 24, 30, 3, 16, 22, 3, 10, 6, 24, 30, 10, 11, 19, 6, 16, 30, 8, 1, 23, 23, 27, 23, 30, 1, 4, 27, 13, 18, 9, 26, 16, 15, 29, 13, 28, 25, 27, 23, 5, 1, 6, 30, 28, 29, 23, 2, 21, 27, 24, 7, 14, 27, 11, 2, 6, 15, 11, 3, 13, 13, 19, 30, 10, 17, 25, 19, 3, 13, 28, 6, 11, 28, 3, 7, 14, 27, 26, 29, 24, 10, 15, 28, 5, 5, 18, 4, 16, 4, 7, 23, 12, 12, 8, 13, 3, 8, 9, 5, 10, 17, 1, 8, 15, 22, 24, 22, 17, 19, 23, 4, 2, 6, 5, 27, 12, 29, 20, 24, 12, 16, 8, 30, 17, 6, 28, 5, 16, 15, 16, 15, 11, 18, 23, 9, 29, 12, 1, 4, 6, 27, 9, 2, 23, 15, 23, 30, 1, 3, 13, 8, 24, 18, 3, 10, 6, 18, 17, 23, 19, 3, 10, 6, 15, 29, 1, 28, 29, 10, 24, 11, 26, 10, 19, 11, 3, 25, 28, 20, 30, 7, 11, 4, 26, 15, 10, 25, 4, 22, 3, 14, 30, 20, 14, 6, 3, 8, 6, 27, 16, 7, 17, 1, 20, 10, 13, 30, 10, 26, 12, 30, 11, 26, 30, 1, 16, 15, 21, 1, 20, 26, 30, 16, 3, 2, 7, 12, 10, 29, 16, 20, 22, 10, 26, 20, 11, 5, 21, 11, 29, 25, 8, 6, 26, 21, 2, 26, 16, 14, 21, 9, 25, 14, 5, 20, 22, 1, 26, 9, 8, 11, 13, 5, 3, 28, 27, 18, 25, 18, 10, 14, 13, 22, 29, 12, 26, 8, 9, 9, 13, 11, 6, 16, 1, 16, 6, 16, 7, 1, 29, 12, 16, 28, 12, 4, 27, 10, 18, 21, 8, 15, 21, 30, 24, 14, 26, 8, 29, 20, 13, 23, 15, 30, 8, 3, 21, 2, 6, 12, 15, 25, 30, 29, 30, 13, 2, 1, 30, 3, 1, 16, 22, 29, 30, 21, 3, 14, 5, 2, 21, 4, 6, 23, 4, 16, 17, 26, 27, 1, 27, 3, 29, 5, 1, 26, 9, 7, 22, 7, 6, 13, 16, 4, 26, 5, 23, 15, 20, 30, 16, 14, 1, 15]
        # island_positions = [16, 1, 20, 30, 11, 10, 9, 6, 11, 28, 4, 30, 12, 6, 2, 16, 27, 7, 7, 10, 16, 24, 21, 12, 5, 27, 25, 23, 2, 26, 30, 30, 6, 9, 22, 23, 2, 10, 8, 10, 23, 24, 18, 15, 5, 5, 30, 24, 3, 5, 11, 27, 1, 15, 15, 15, 4, 11, 24, 27, 5, 6, 14, 11, 1, 11, 16, 19, 23, 16, 29, 4, 28, 16, 20, 23, 8, 30, 16, 26, 15, 13, 14, 2, 6, 21, 24, 5, 7, 2, 18, 15, 17, 13, 16, 16, 30, 8, 23, 4, 10, 25, 25, 15, 29, 30, 19, 11, 27, 12, 28, 4, 27, 16, 23, 26, 6, 19, 23, 6, 6, 29, 15, 22, 2, 13, 1, 3, 3, 22, 1, 14, 25, 12, 3, 23, 26, 10, 1, 4, 23, 17, 26, 10, 14, 16, 11, 20, 30, 26, 6, 8, 26, 27, 9, 12, 6, 27, 15, 14, 16, 23, 4, 3, 14, 27, 12, 6, 13, 14, 21, 25, 3, 1, 5, 12, 3, 13, 22, 17, 26, 16, 13, 20, 6, 17, 7, 30, 15, 1, 11, 26, 13, 1, 11, 3, 5, 4, 15, 1, 16, 20, 30, 28, 26, 14, 16, 8, 7, 23, 6, 29, 1, 16, 27, 20, 6, 18, 15, 1, 9, 3, 8, 21, 18, 26, 25, 8, 24, 20, 30, 11, 8, 9, 27, 10, 1, 29, 1, 9, 10, 9, 26, 20, 17, 7, 9, 25, 21, 27, 5, 30, 7, 20, 10, 3, 8, 29, 24, 17, 10, 1, 2, 30, 14, 20, 3, 10, 3, 16, 11, 3, 27, 24, 16, 4, 30, 19, 30, 8, 28, 21, 1, 16, 15, 7, 1, 23, 21, 14, 22, 30, 24, 6, 13, 28, 21, 30, 24, 26, 22, 24, 7, 2, 2, 7, 10, 28, 5, 10, 4, 8, 23, 30, 18, 29, 3, 28, 7, 9, 15, 6, 14, 29, 22, 5, 15, 1, 12, 29, 10, 7, 13, 3, 16, 18, 17, 16, 29, 19, 8, 16, 9, 29, 16, 20, 29, 13, 16, 12, 30, 6, 15, 12, 11, 3, 6, 21, 28, 13, 26, 11, 19, 10, 8, 25, 10, 4, 5, 21, 24, 26, 12, 3, 2, 27, 1, 22, 13, 20, 29, 30, 28, 15, 3, 30, 18, 22, 12, 18, 30, 29, 19, 10, 29, 13, 24, 26, 12, 13]
        island_positions = [28, 10, 5, 1, 30, 15, 28, 24, 30, 9, 5, 3, 7, 23, 30, 26, 16, 18, 4, 30, 8, 23, 13, 25, 6, 9, 29, 30, 5, 13, 10, 23, 16, 6, 9, 9, 16, 4, 12, 16, 11, 6, 23, 13, 1, 15, 30, 3, 3, 22, 7, 15, 8, 27, 15, 12, 7, 27, 28, 28, 21, 24, 15, 21, 2, 17, 22, 23, 9, 8, 17, 11, 27, 25, 16, 29, 29, 6, 23, 3, 6, 30, 10, 27, 2, 1, 25, 5, 18, 15, 20, 7, 2, 11, 27, 28, 24, 20, 26, 1, 8, 18, 1, 26, 6, 30, 1, 26, 16, 3, 26, 2, 21, 8, 14, 28, 24, 1, 4, 20, 20, 20, 22, 10, 4, 3, 12, 21, 27, 30, 7, 30, 30, 5, 8, 3, 16, 13, 16, 14, 18, 10, 20, 30, 7, 1, 10, 8, 29, 4, 2, 22, 3, 26, 21, 27, 26, 25, 4, 17, 30, 2, 12, 10, 14, 16, 29, 15, 16, 23, 10, 30, 22, 17, 4, 6, 16, 11, 11, 10, 1, 3, 21, 16, 16, 6, 3, 26, 10, 30, 6, 23, 16, 1, 11, 11, 3, 12, 5, 18, 10, 20, 8, 9, 15, 11, 17, 27, 26, 14, 2, 24, 26, 18, 16, 29, 13, 13, 8, 14, 7, 16, 19, 8, 25, 15, 15, 7, 23, 21, 16, 29, 20, 19, 3, 15, 29, 15, 8, 29, 28, 11, 6, 26, 12, 26, 24, 29, 17, 13, 1, 24, 9, 24, 22, 16, 14, 16, 7, 30, 13, 29, 9, 4, 26, 20, 12, 1, 15, 30, 14, 2, 14, 21, 20, 11, 19, 10, 30, 12, 5, 29, 22, 12, 10, 2, 29, 23, 18, 6, 15, 18, 7, 29, 3, 27, 24, 6, 26, 3, 13, 28, 13, 21, 4, 14, 14, 16, 6, 23, 1, 26, 27, 19, 6, 1, 16, 12, 8, 5, 7, 27, 1, 15, 26, 1, 3, 14, 11, 10, 10, 30, 4, 27, 13, 23, 25, 24, 4, 25, 23, 10, 27, 6, 30, 15, 3, 28, 9, 30, 11, 6, 13, 20, 30, 24, 3, 1, 1, 19, 16, 12, 19, 12, 5, 6, 22, 2, 5, 1, 20, 16, 27, 22, 23, 24, 19, 5, 13, 12, 24, 15, 10, 16, 6, 13, 30, 28, 5, 21, 9, 17, 3, 11, 8, 10, 11, 29, 7, 25]
        # island_positions = [8, 30, 15, 8, 24, 28, 11, 5, 15, 16, 29, 15, 23, 8, 15, 2, 3, 13, 7, 20, 6, 30, 9, 20, 20, 7, 29, 13, 26, 26, 1, 8, 2, 21, 9, 4, 22, 11, 2, 26, 22, 14, 16, 15, 24, 29, 12, 25, 30, 24, 30, 1, 1, 17, 18, 11, 15, 20, 8, 6, 30, 10, 24, 5, 26, 7, 23, 3, 14, 26, 15, 12, 17, 19, 10, 29, 29, 8, 25, 2, 18, 24, 12, 28, 16, 1, 7, 7, 23, 8, 30, 21, 15, 28, 23, 9, 7, 17, 28, 5, 16, 20, 30, 27, 2, 12, 23, 30, 26, 6, 16, 28, 16, 4, 16, 22, 6, 16, 25, 15, 6, 28, 11, 21, 4, 13, 10, 23, 25, 16, 1, 15, 14, 25, 11, 27, 30, 6, 19, 27, 17, 14, 23, 20, 1, 12, 9, 6, 30, 11, 16, 23, 7, 16, 14, 9, 13, 3, 12, 11, 16, 29, 16, 5, 15, 3, 27, 23, 14, 30, 22, 15, 12, 3, 6, 1, 4, 2, 11, 5, 27, 22, 1, 29, 11, 12, 10, 30, 22, 16, 29, 3, 7, 18, 3, 8, 3, 12, 21, 6, 7, 4, 6, 5, 30, 13, 24, 4, 12, 3, 21, 25, 27, 17, 14, 27, 13, 23, 7, 16, 3, 1, 16, 20, 23, 30, 15, 27, 18, 1, 30, 3, 24, 15, 4, 1, 26, 5, 8, 14, 12, 20, 30, 14, 23, 3, 23, 16, 28, 1, 20, 11, 6, 7, 21, 27, 8, 23, 27, 13, 29, 6, 1, 25, 26, 15, 13, 22, 17, 19, 2, 1, 1, 11, 9, 10, 22, 10, 14, 29, 28, 1, 10, 26, 19, 19, 10, 4, 16, 22, 6, 1, 26, 15, 28, 30, 1, 24, 24, 9, 24, 26, 16, 19, 27, 6, 7, 30, 27, 30, 10, 13, 6, 3, 18, 21, 14, 30, 11, 10, 29, 2, 29, 10, 26, 16, 6, 3, 30, 16, 5, 4, 9, 30, 19, 8, 20, 11, 1, 10, 9, 13, 2, 20, 13, 12, 4, 3, 26, 13, 10, 16, 16, 4, 8, 13, 5, 6, 26, 10, 3, 13, 21, 28, 18, 21, 9, 26, 10, 3, 11, 18, 5, 18, 29, 24, 3, 15, 30, 5, 25, 21, 24, 10, 29, 24, 27, 2, 8, 20, 16, 26, 12, 5, 10, 29, 17, 10, 6, 27]
        # island_positions = [23, 29, 27, 30, 21, 30, 27, 7, 26, 29, 16, 21, 3, 28, 30, 3, 6, 3, 25, 10, 10, 1, 6, 12, 3, 30, 17, 6, 28, 8, 2, 6, 23, 16, 8, 18, 3, 22, 12, 26, 21, 7, 9, 7, 23, 5, 17, 4, 6, 1, 30, 7, 8, 27, 8, 17, 8, 24, 12, 16, 17, 9, 12, 9, 21, 25, 20, 1, 23, 10, 2, 26, 4, 5, 8, 23, 23, 30, 7, 26, 24, 20, 10, 30, 25, 5, 4, 30, 7, 3, 22, 15, 16, 13, 26, 23, 16, 12, 24, 20, 16, 30, 8, 8, 3, 4, 1, 27, 28, 18, 1, 22, 15, 10, 6, 20, 9, 14, 30, 2, 13, 9, 2, 26, 16, 26, 5, 28, 26, 1, 28, 12, 3, 30, 26, 10, 22, 20, 10, 7, 12, 27, 29, 15, 23, 16, 18, 15, 8, 10, 4, 21, 6, 2, 10, 16, 28, 20, 10, 11, 5, 1, 13, 8, 3, 20, 10, 28, 29, 5, 20, 25, 13, 8, 13, 14, 12, 7, 6, 24, 24, 16, 26, 6, 29, 30, 26, 16, 1, 12, 30, 29, 25, 3, 27, 24, 15, 11, 16, 16, 1, 25, 30, 30, 19, 29, 7, 3, 2, 19, 30, 16, 7, 1, 29, 16, 15, 11, 13, 8, 11, 14, 21, 22, 1, 10, 18, 4, 29, 16, 20, 15, 14, 19, 2, 23, 30, 18, 21, 5, 3, 11, 24, 16, 20, 22, 19, 2, 15, 28, 9, 30, 10, 13, 27, 27, 5, 27, 29, 15, 30, 3, 30, 9, 4, 18, 3, 6, 3, 22, 29, 10, 1, 29, 12, 10, 23, 6, 15, 19, 1, 15, 29, 11, 28, 18, 1, 18, 17, 15, 15, 13, 4, 16, 11, 29, 26, 28, 27, 17, 16, 11, 24, 8, 24, 3, 27, 27, 24, 3, 16, 4, 15, 14, 3, 6, 13, 21, 4, 19, 7, 13, 21, 14, 20, 2, 9, 2, 22, 25, 1, 15, 16, 11, 10, 1, 27, 27, 30, 4, 29, 6, 5, 15, 6, 12, 6, 11, 24, 24, 5, 16, 14, 20, 11, 16, 26, 14, 23, 13, 5, 22, 13, 30, 23, 17, 15, 14, 5, 12, 23, 25, 1, 21, 6, 30, 19, 13, 14, 14, 13, 26, 10, 10, 23, 24, 1, 1, 11, 7, 16, 26, 11, 9, 12, 26, 9, 6, 6, 11]
        # island_positions = [25, 27, 13, 10, 8, 1, 12, 29, 29, 30, 27, 3, 27, 24, 12, 14, 5, 9, 25, 12, 19, 30, 20, 20, 15, 30, 22, 5, 10, 13, 18, 21, 3, 17, 14, 3, 21, 26, 10, 23, 29, 20, 28, 25, 1, 11, 17, 19, 15, 1, 23, 23, 1, 24, 4, 26, 3, 10, 16, 27, 14, 13, 19, 12, 14, 23, 25, 1, 5, 16, 10, 22, 14, 27, 4, 4, 16, 15, 21, 16, 25, 12, 20, 13, 3, 30, 30, 5, 2, 5, 26, 18, 23, 29, 17, 30, 13, 26, 16, 30, 24, 23, 6, 14, 8, 25, 6, 23, 15, 24, 6, 26, 9, 16, 22, 1, 19, 24, 16, 13, 8, 15, 6, 2, 15, 3, 2, 10, 10, 9, 27, 18, 6, 30, 10, 4, 7, 7, 28, 3, 3, 6, 23, 29, 29, 29, 5, 13, 3, 16, 1, 21, 30, 1, 25, 7, 21, 7, 10, 20, 6, 16, 12, 6, 4, 11, 30, 22, 27, 12, 21, 7, 26, 22, 16, 23, 27, 3, 18, 8, 29, 9, 5, 3, 9, 10, 30, 11, 28, 1, 15, 7, 27, 26, 16, 6, 26, 23, 17, 26, 15, 15, 9, 10, 7, 11, 30, 1, 5, 29, 8, 11, 19, 30, 26, 30, 5, 30, 29, 15, 4, 29, 8, 19, 8, 15, 3, 1, 1, 16, 15, 27, 2, 30, 1, 14, 9, 23, 1, 8, 10, 28, 22, 9, 11, 24, 15, 8, 29, 12, 5, 16, 1, 4, 4, 28, 2, 24, 18, 16, 15, 28, 4, 26, 6, 7, 24, 6, 13, 26, 8, 24, 6, 14, 1, 8, 3, 17, 30, 3, 15, 12, 10, 20, 27, 16, 17, 28, 11, 6, 3, 1, 12, 30, 13, 29, 16, 30, 6, 10, 7, 30, 7, 8, 10, 11, 2, 20, 28, 20, 1, 29, 5, 26, 23, 8, 24, 13, 6, 9, 11, 30, 10, 16, 24, 20, 26, 28, 7, 6, 11, 10, 27, 16, 24, 13, 21, 21, 3, 13, 2, 18, 16, 7, 26, 15, 5, 12, 20, 26, 18, 21, 14, 16, 16, 19, 22, 3, 25, 2, 27, 30, 14, 4, 23, 3, 22, 22, 6, 2, 11, 11, 2, 15, 13, 16, 12, 23, 14, 24, 1, 17, 16, 4, 28, 18, 29, 11, 9, 16, 13, 20, 21, 27, 30, 20, 6, 11, 10, 12]
        # island_positions = [22, 12, 8, 5, 13, 2, 6, 10, 10, 7, 15, 26, 29, 29, 30, 5, 10, 3, 27, 24, 19, 6, 12, 3, 23, 16, 30, 11, 16, 15, 26, 10, 9, 21, 12, 20, 13, 9, 6, 20, 4, 2, 11, 30, 3, 24, 24, 1, 30, 6, 4, 18, 27, 25, 15, 29, 20, 11, 10, 7, 6, 30, 5, 17, 16, 16, 14, 5, 1, 5, 24, 3, 15, 16, 2, 14, 18, 1, 3, 5, 13, 5, 1, 26, 5, 7, 6, 8, 10, 30, 8, 14, 6, 26, 23, 17, 9, 3, 16, 22, 26, 1, 20, 3, 14, 11, 16, 4, 7, 24, 23, 21, 22, 26, 1, 11, 30, 20, 13, 11, 24, 29, 29, 24, 1, 19, 13, 20, 6, 2, 3, 8, 29, 16, 27, 28, 6, 26, 20, 19, 15, 28, 27, 16, 3, 8, 30, 19, 21, 21, 14, 1, 10, 10, 4, 1, 1, 13, 27, 6, 12, 19, 1, 18, 25, 18, 12, 1, 14, 3, 7, 30, 6, 16, 6, 16, 27, 15, 13, 30, 24, 13, 9, 15, 15, 14, 16, 17, 21, 12, 23, 3, 21, 15, 8, 14, 2, 29, 12, 4, 16, 18, 29, 6, 29, 1, 3, 24, 26, 2, 6, 14, 26, 7, 16, 6, 23, 20, 22, 25, 8, 16, 5, 30, 22, 18, 15, 13, 27, 3, 20, 23, 9, 23, 11, 17, 30, 29, 5, 25, 24, 23, 28, 29, 30, 15, 24, 21, 25, 9, 9, 12, 28, 20, 1, 30, 27, 26, 11, 14, 30, 27, 8, 23, 21, 3, 13, 10, 20, 8, 7, 15, 10, 10, 27, 9, 26, 7, 13, 17, 29, 21, 3, 26, 15, 11, 6, 8, 16, 4, 12, 16, 1, 5, 27, 30, 30, 26, 12, 16, 30, 23, 22, 2, 11, 6, 16, 19, 11, 28, 15, 23, 1, 11, 2, 26, 1, 4, 21, 8, 23, 6, 15, 16, 18, 7, 22, 25, 14, 24, 4, 4, 29, 13, 30, 7, 13, 27, 12, 29, 30, 30, 15, 7, 8, 15, 10, 22, 23, 16, 3, 10, 20, 27, 28, 23, 12, 12, 3, 5, 11, 11, 8, 25, 10, 3, 26, 4, 28, 7, 9, 2, 27, 10, 28, 22, 30, 16, 9, 16, 29, 28, 24, 25, 10, 30, 17, 19, 10, 18, 17, 4, 1, 2, 13, 1, 16, 28, 10, 26]
        # island_positions = [25, 1, 30, 20, 22, 13, 23, 20, 1, 3, 23, 28, 29, 12, 3, 30, 4, 29, 16, 16, 10, 25, 7, 26, 18, 14, 13, 26, 12, 13, 3, 15, 16, 3, 15, 10, 12, 11, 4, 18, 29, 24, 5, 16, 22, 30, 26, 13, 6, 26, 8, 29, 6, 9, 26, 18, 12, 19, 4, 27, 24, 6, 8, 15, 30, 15, 25, 10, 30, 1, 30, 15, 21, 8, 11, 14, 30, 3, 2, 23, 30, 19, 5, 6, 10, 27, 5, 6, 16, 2, 28, 23, 1, 20, 24, 21, 23, 5, 12, 30, 16, 9, 5, 16, 23, 30, 16, 24, 16, 30, 13, 12, 11, 11, 6, 11, 6, 9, 21, 22, 2, 3, 5, 6, 24, 30, 11, 27, 20, 7, 16, 7, 20, 14, 1, 16, 13, 20, 8, 7, 1, 20, 5, 3, 18, 6, 23, 21, 3, 7, 9, 27, 26, 15, 3, 13, 8, 9, 7, 13, 3, 28, 27, 21, 22, 20, 11, 15, 16, 29, 14, 27, 29, 10, 1, 10, 16, 4, 30, 16, 7, 22, 30, 29, 15, 23, 21, 23, 14, 14, 10, 11, 7, 14, 12, 5, 3, 30, 4, 6, 5, 13, 17, 23, 13, 30, 6, 19, 21, 8, 30, 9, 4, 22, 27, 7, 20, 30, 20, 7, 27, 11, 9, 2, 16, 8, 18, 29, 14, 2, 16, 24, 26, 24, 6, 29, 21, 27, 1, 3, 12, 10, 30, 10, 30, 27, 23, 11, 6, 28, 16, 15, 5, 8, 26, 17, 1, 19, 24, 3, 11, 6, 3, 2, 1, 10, 25, 22, 2, 10, 16, 17, 2, 24, 26, 3, 18, 1, 19, 16, 26, 29, 25, 8, 27, 9, 8, 19, 22, 10, 28, 11, 30, 12, 29, 24, 20, 1, 10, 14, 27, 28, 26, 8, 1, 23, 10, 19, 2, 4, 15, 21, 3, 16, 16, 9, 16, 14, 28, 13, 1, 22, 26, 25, 6, 10, 13, 23, 28, 11, 29, 15, 30, 17, 8, 15, 26, 5, 13, 26, 26, 6, 13, 15, 4, 1, 27, 11, 21, 16, 16, 12, 30, 17, 29, 12, 3, 18, 28, 24, 24, 29, 15, 5, 14, 4, 10, 6, 1, 17, 3, 4, 1, 25, 9, 27, 8, 15, 28, 15, 29, 10, 18, 7, 1, 7, 15, 1, 23, 2, 24, 6, 10, 26, 12, 4, 25, 12, 20, 17]
        # island_positions = [22, 14, 19, 15, 12, 1, 1, 3, 28, 12, 6, 7, 29, 22, 11, 8, 10, 30, 13, 24, 2, 9, 13, 4, 23, 16, 28, 16, 9, 23, 17, 1, 2, 28, 12, 14, 20, 16, 16, 6, 18, 27, 28, 20, 13, 5, 21, 10, 10, 11, 24, 23, 30, 23, 9, 18, 13, 15, 4, 17, 25, 27, 10, 27, 22, 8, 29, 26, 3, 26, 8, 21, 21, 16, 10, 16, 8, 16, 6, 14, 26, 3, 6, 29, 4, 9, 30, 22, 3, 27, 20, 16, 12, 30, 4, 4, 21, 16, 3, 13, 1, 22, 12, 26, 26, 18, 6, 1, 3, 18, 7, 8, 7, 14, 23, 15, 22, 27, 2, 16, 20, 5, 15, 21, 10, 8, 23, 5, 12, 30, 22, 11, 24, 21, 21, 2, 14, 23, 10, 6, 15, 30, 16, 4, 28, 11, 14, 15, 5, 20, 16, 1, 27, 13, 8, 3, 17, 17, 11, 28, 15, 11, 18, 6, 6, 29, 21, 29, 25, 10, 16, 4, 15, 4, 23, 1, 3, 23, 5, 13, 16, 16, 1, 24, 17, 13, 7, 16, 14, 21, 3, 15, 19, 3, 23, 12, 8, 20, 30, 15, 18, 27, 11, 9, 15, 1, 4, 9, 24, 25, 5, 10, 16, 8, 2, 6, 1, 20, 19, 18, 24, 3, 10, 16, 30, 26, 16, 12, 20, 16, 11, 3, 3, 1, 29, 30, 1, 8, 11, 5, 23, 2, 6, 26, 6, 4, 1, 24, 13, 1, 19, 30, 11, 25, 25, 15, 10, 27, 10, 11, 15, 12, 20, 19, 5, 1, 20, 19, 10, 15, 19, 29, 7, 8, 1, 30, 6, 27, 11, 24, 15, 5, 10, 10, 13, 16, 12, 16, 13, 27, 3, 28, 4, 25, 2, 29, 23, 2, 5, 30, 25, 26, 28, 10, 14, 12, 26, 29, 3, 24, 22, 26, 1, 14, 14, 30, 12, 15, 16, 6, 27, 6, 3, 7, 20, 15, 30, 30, 26, 14, 30, 23, 26, 24, 1, 5, 6, 30, 20, 27, 23, 1, 26, 8, 10, 24, 29, 17, 30, 9, 18, 27, 28, 30, 26, 11, 13, 27, 3, 9, 30, 6, 24, 28, 17, 3, 5, 29, 30, 2, 7, 16, 2, 12, 7, 30, 13, 29, 25, 7, 26, 6, 24, 6, 10, 21, 7, 22, 26, 9, 29, 9, 11, 7, 29, 30, 8, 13, 7, 29]
        # island_positions = [27, 12, 25, 8, 24, 1, 23, 23, 26, 7, 21, 21, 29, 14, 3, 25, 24, 10, 6, 11, 15, 8, 30, 6, 20, 30, 29, 26, 13, 10, 8, 13, 2, 8, 27, 11, 7, 8, 20, 22, 3, 20, 1, 15, 14, 7, 30, 6, 9, 10, 30, 5, 27, 1, 22, 4, 29, 1, 20, 21, 30, 3, 3, 29, 21, 1, 20, 13, 10, 15, 8, 27, 10, 7, 29, 30, 25, 18, 6, 16, 30, 15, 3, 17, 27, 8, 27, 30, 12, 25, 17, 5, 19, 11, 23, 6, 28, 8, 20, 23, 4, 11, 13, 24, 12, 21, 30, 16, 18, 4, 29, 16, 14, 26, 19, 1, 23, 26, 28, 14, 30, 7, 20, 3, 30, 7, 17, 24, 15, 30, 7, 28, 24, 10, 21, 11, 1, 2, 15, 22, 2, 6, 6, 16, 10, 30, 12, 16, 20, 18, 23, 30, 6, 13, 15, 9, 16, 18, 10, 6, 16, 29, 26, 25, 5, 16, 7, 29, 4, 28, 11, 3, 17, 29, 3, 13, 27, 24, 14, 10, 13, 10, 14, 12, 20, 23, 30, 1, 18, 15, 9, 12, 3, 30, 26, 23, 1, 11, 12, 15, 8, 12, 30, 11, 26, 14, 20, 17, 17, 16, 10, 6, 11, 9, 5, 6, 7, 3, 22, 7, 15, 13, 5, 23, 19, 30, 29, 13, 16, 30, 4, 6, 6, 12, 9, 3, 24, 16, 13, 16, 21, 5, 20, 1, 15, 27, 5, 12, 21, 9, 2, 12, 2, 15, 24, 26, 10, 4, 16, 24, 9, 22, 23, 12, 13, 22, 16, 13, 26, 26, 11, 27, 6, 11, 2, 8, 24, 1, 5, 4, 1, 28, 27, 4, 1, 3, 22, 5, 27, 2, 19, 15, 1, 3, 14, 29, 10, 9, 2, 10, 6, 11, 2, 3, 11, 4, 6, 26, 10, 27, 5, 15, 21, 4, 30, 28, 13, 1, 9, 23, 29, 16, 29, 24, 17, 14, 16, 5, 1, 24, 25, 26, 19, 11, 26, 30, 16, 23, 25, 10, 10, 18, 4, 14, 8, 27, 1, 19, 1, 3, 6, 15, 24, 16, 19, 25, 29, 7, 30, 16, 28, 3, 26, 2, 13, 26, 3, 10, 16, 22, 16, 15, 18, 20, 22, 29, 7, 14, 27, 28, 6, 15, 16, 5, 21, 23, 1, 28, 12, 26, 23, 8, 9, 18, 8, 16, 16, 3, 28, 30]
        # island_positions = [3, 27, 12, 1, 11, 27, 6, 14, 29, 26, 17, 26, 4, 10, 14, 3, 10, 30, 10, 30, 10, 24, 1, 1, 1, 13, 17, 16, 16, 30, 16, 7, 4, 30, 13, 11, 29, 4, 24, 16, 30, 16, 18, 12, 15, 6, 15, 26, 7, 3, 7, 29, 22, 8, 15, 15, 16, 1, 26, 18, 23, 13, 13, 8, 4, 20, 15, 28, 1, 8, 4, 23, 28, 6, 1, 18, 12, 9, 3, 23, 16, 22, 12, 11, 20, 5, 2, 1, 28, 14, 12, 13, 25, 26, 24, 1, 23, 13, 27, 3, 23, 27, 27, 30, 23, 11, 2, 2, 21, 7, 19, 13, 29, 20, 15, 20, 1, 3, 3, 6, 12, 28, 22, 3, 26, 1, 10, 30, 16, 21, 6, 25, 27, 2, 27, 9, 8, 11, 21, 10, 18, 29, 24, 25, 11, 19, 6, 27, 26, 24, 30, 8, 2, 1, 11, 8, 14, 14, 5, 3, 3, 13, 20, 30, 2, 10, 15, 28, 7, 3, 15, 27, 8, 30, 29, 16, 23, 13, 3, 17, 10, 2, 27, 26, 30, 15, 18, 6, 26, 27, 2, 23, 11, 14, 14, 5, 5, 16, 30, 4, 29, 7, 14, 30, 12, 1, 19, 15, 4, 21, 5, 6, 26, 12, 5, 9, 22, 18, 21, 27, 30, 3, 16, 28, 26, 28, 10, 20, 15, 18, 12, 4, 24, 12, 10, 4, 24, 8, 9, 3, 4, 21, 16, 29, 8, 30, 20, 5, 8, 24, 28, 7, 21, 17, 24, 29, 6, 5, 16, 26, 6, 16, 16, 15, 17, 21, 6, 6, 20, 16, 29, 11, 11, 23, 7, 19, 3, 25, 9, 9, 16, 25, 24, 12, 1, 10, 16, 23, 30, 15, 7, 1, 9, 5, 15, 11, 7, 27, 8, 6, 20, 3, 17, 10, 25, 1, 14, 6, 11, 8, 29, 16, 22, 22, 21, 12, 10, 29, 24, 5, 11, 19, 1, 13, 20, 10, 17, 16, 28, 25, 24, 7, 6, 10, 22, 13, 5, 30, 26, 16, 10, 4, 26, 3, 6, 22, 9, 20, 15, 19, 3, 16, 10, 5, 16, 12, 23, 11, 23, 26, 29, 20, 26, 10, 1, 28, 30, 13, 19, 8, 2, 6, 13, 27, 13, 23, 15, 30, 2, 30, 9, 30, 18, 29, 14, 22, 23, 25, 30, 7, 21, 9, 30, 24, 6, 29, 15, 14, 16, 1]

        for i in range(SMALL_ISLAND_COUNT):
            self.i = a.Sprite("assets/island.png", SCALING)
            self.i.right = UNIT_SIZE * island_positions.pop()
            self.i.bottom = UNIT_SIZE * island_positions.pop()
            self.all_sprites.append(self.i)
            self.island_sprites.append(self.i)

        for i in range(TALL_ISLAND_COUNT):
            self.i = a.Sprite("assets/island_tall.png", SCALING)
            self.i.right = UNIT_SIZE * island_positions.pop()
            self.i.bottom = UNIT_SIZE * island_positions.pop()
            self.all_sprites.append(self.i)
            self.island_sprites.append(self.i)

        for i in range(WIDE_ISLAND_COUNT):
            self.i = a.Sprite("assets/island_wide.png", SCALING)
            self.i.right = UNIT_SIZE * island_positions.pop()
            self.i.bottom = UNIT_SIZE * island_positions.pop()
            self.all_sprites.append(self.i)
            self.island_sprites.append(self.i)

        for i in range(LARGE_ISLAND_COUNT):
            self.i = a.Sprite("assets/island_large.png", SCALING)
            self.i.right = UNIT_SIZE * island_positions.pop()
            self.i.bottom = UNIT_SIZE * island_positions.pop()
            self.all_sprites.append(self.i)
            self.island_sprites.append(self.i)

        self.red_sub = a.Sprite("assets/redMark.png", SCALING)
        self.red_sub.top = UNIT_SIZE * 15
        self.red_sub.right = UNIT_SIZE * 15
        self.all_sprites.append(self.red_sub)
        self.red_trail_sprites.append(self.red_sub)

        self.white_sub = SubmarineSprite("assets/whiteMark.png", SCALING)
        self.all_sprites.append(self.white_sub)
        looping = True
        while looping:
            self.white_sub.right = UNIT_SIZE * random.randint(1,30)
            self.white_sub.bottom = UNIT_SIZE * random.randint(1,30)
            if not self.white_sub.collides_with_list(self.island_sprites):
                looping = False
        

        #start server thread
        self.radio_opperator.start()

        self.data_to_send = {"position": self.white_sub.position, "move_log": [], "torpedo_position": None}
        self.sending_socket.bind((self.ip, CLIENT_PORT))
        self.sending_socket.connect((self.enemy_ip, SERVER_PORT))

        # send the READY flag to the other player
        self.data_to_send["position"] = "READY"
        # used code from https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
        data_to_send_local = json.dumps(self.data_to_send) # convert to json string
        data_to_send_local = data_to_send_local.encode() # convert to bytes
        self.sending_socket.sendall(data_to_send_local)

        # block until we receive the READY flag
        while True:
            if self.radio_opperator.is_other_player_ready == True:
                break

        # schedule the reactor tick to continually tick up 
        a.schedule(self._tick_reactor, REACTOR_TICK_TIME)

    def on_update(self, delta_time : float):
    # handle victory
        with self.lock:
            if self.radio_opperator.is_victory:
                self.victory = a.Sprite("assets/victory.png", SCALING)
                self.victory.center_x = SCREEN_WIDTH / 2
                self.victory.center_y = SCREEN_HEIGHT / 2
                self.all_sprites.append(self.victory)
                self.is_playing = False

    # only update the rest if the game is still going.
        if self.is_playing:
    
    # handle no lives (Failure)
            if not self.heart_1.is_active and not self.heart_2.is_active:
                self.failure = a.Sprite("assets/failure.png", SCALING)
                self.failure.center_x = SCREEN_WIDTH / 2
                self.failure.center_y = SCREEN_HEIGHT / 2
                self.all_sprites.append(self.failure)
                self.is_playing = False
                self.sending_socket

                # send the VICTORY flag to the other player (because they won)
                self.data_to_send["position"] = "VICTORY"
                # used code from https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
                data_to_send_local = json.dumps(self.data_to_send) # convert to json string
                data_to_send_local = data_to_send_local.encode() # convert to bytes
                self.sending_socket.sendall(data_to_send_local)

        
    # only update the rest if the game is still going.
            if self.is_playing:

        # Add move to the data to send, if moved 
                if self.white_sub.did_move:
                    # self.data_to_send["move_log"].append((self.white_sub.change_x, self.white_sub.change_y))
                    self.data_to_send["move_log"] = (self.white_sub.change_x, self.white_sub.change_y)

        # update sprites
                self._update_reactor_from_tick()

                with self.lock:
                    if self.radio_opperator.enemy_last_move[0] != 0 or self.radio_opperator.enemy_last_move[1] != 0:
        # handle red sub
                        marker = a.Sprite("assets/redMarkSmall.png", SCALING)
                        marker.center_x = self.red_sub.center_x
                        marker.center_y = self.red_sub.center_y
                        marker.change_x = self.red_sub.change_x
                        marker.change_y = self.red_sub.change_y
                        self.all_sprites.append(marker)
                        self.red_trail_sprites.append(marker)

                        self.red_sub.change_x += self.radio_opperator.enemy_last_move[0] # get enemy x position
                        self.red_sub.change_y += self.radio_opperator.enemy_last_move[1] # get enemy y position
                        self.radio_opperator.enemy_last_move = (0,0)

        # handle torpedo
                    torpedo_position = self.radio_opperator.enemy_torpedo_position

                    if torpedo_position != None:
                        # print("entering torpedo handling...")
                        torpedo_x = torpedo_position[0]
                        torpedo_y = torpedo_position[1]
                        indirect_hits = [
                            (torpedo_x, torpedo_y + UNIT_SIZE), # north
                            (torpedo_x - UNIT_SIZE, torpedo_y + UNIT_SIZE), # north west
                            (torpedo_x + UNIT_SIZE, torpedo_y + UNIT_SIZE), # north east
                            (torpedo_x, torpedo_y - UNIT_SIZE), # south
                            (torpedo_x - UNIT_SIZE, torpedo_y - UNIT_SIZE), # south west
                            (torpedo_x + UNIT_SIZE, torpedo_y - UNIT_SIZE), # south east
                            (torpedo_x - UNIT_SIZE, torpedo_y), # west
                            (torpedo_x + UNIT_SIZE, torpedo_y) # east
                        ]
                        if self.white_sub.collides_with_point(torpedo_position):
                            # direct hit
                            # print("direct hit".upper())
                            self._take_damage(2)
                        else:
                            for i in indirect_hits:
                                # print(f"checking for indirect hit at: {i}")
                                if self.white_sub.collides_with_point(i):
                                    # indirect hit
                                    # print("indirect hit".upper())
                                    self._take_damage(1)
                                    break

                    self.radio_opperator.enemy_torpedo_position = None
                
        # handle updating all sprites
                self.all_sprites.update()
                
        # set red sub & trail velocity back to 0
                for i in self.red_trail_sprites:
                    i.change_x = 0
                    i.change_y = 0
                
        # update and send data to the other computer, if moved 
                if self.white_sub.did_move:
                    self.data_to_send["position"] = self.white_sub.position
                    self.data_to_send["torpedo_position"] = self.white_sub.torpedo_position
                    
                    # used code from https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
                    data_to_send_local = json.dumps(self.data_to_send) # convert to json string
                    # data_to_send_local = str(self.data_to_send)
                    data_to_send_local = data_to_send_local.encode() # convert to bytes
                    self.sending_socket.sendall(data_to_send_local)
                    
                    self.white_sub.torpedo_position = None
                    self.white_sub.did_move = False

    def on_draw(self):
        a.start_render()
        #draw the sprites
        self.all_sprites.draw()
        # print(len(self.all_sprites))
        #draw a border between the map area and the control panel
        a.draw_lrtb_rectangle_filled(SCREEN_WIDTH, SCREEN_WIDTH + 10, SCREEN_HEIGHT, 0, a.color_from_hex_string(PALETTE_WHITE.upper()))

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == a.key.UP or symbol == a.key.W:
            for i in self.red_trail_sprites:
                i.change_y = 10 * SCALING
        elif symbol == a.key.DOWN or symbol == a.key.S:
            for i in self.red_trail_sprites:
                i.change_y = -10 * SCALING
        elif symbol == a.key.LEFT or symbol == a.key.A:
            for i in self.red_trail_sprites:
                i.change_x = -10 * SCALING
        elif symbol == a.key.RIGHT or symbol == a.key.D:
            for i in self.red_trail_sprites:
                i.change_x = 10 * SCALING
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if not self.white_sub.is_move_selected:
            # if NORTH
            amount_will_move = 10 * SCALING
            if self.north_button.collides_with_point((x,y)):
                potential_sub_move = a.Sprite("assets/whiteMark.png", SCALING)
                potential_sub_move.center_x = self.white_sub.center_x
                potential_sub_move.center_y = self.white_sub.center_y + amount_will_move
                # # display the potential collisions...
                # print(len(potential_sub_move.collides_with_list(self.island_sprites)) > 0)
                # print(len(potential_sub_move.collides_with_list(self.white_trail_sprites)) > 0)
                # print(potential_sub_move.top > SCREEN_HEIGHT)
                # will not allow it to be selected if the potential move collides with any island, collides with any piece of the white trail, or if it is past the play area
                if not len(potential_sub_move.collides_with_list(self.island_sprites)) > 0 and not len(potential_sub_move.collides_with_list(self.white_trail_sprites)) > 0 and not potential_sub_move.top > SCREEN_HEIGHT :
                    self.white_sub.is_move_selected = True
                    self.white_sub.selected_move = "n"
                        
                    #change out sprite
                    self.north_button.kill()
                    self.north_button = a.Sprite("assets/north_active.png", SCALING)
                    self.north_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
                    self.north_button.top = ( self.screen_height / 6 ) * 3
                    self.all_sprites.append(self.north_button)

            # if SOUTH 
            elif self.south_button.collides_with_point((x,y)):
                potential_sub_move = a.Sprite("assets/whiteMark.png", SCALING)
                potential_sub_move.center_x = self.white_sub.center_x
                potential_sub_move.center_y = self.white_sub.center_y - amount_will_move
                # will not allow it to be selected if the potential move collides with any island, collides with any piece of the white trail, or if it is past the play area
                if not len(potential_sub_move.collides_with_list(self.island_sprites)) > 0 and not len(potential_sub_move.collides_with_list(self.white_trail_sprites)) > 0 and not potential_sub_move.bottom < 0:
                    self.white_sub.is_move_selected = True
                    self.white_sub.selected_move = "s"
                        
                    #change out sprite
                    self.south_button.kill()
                    self.south_button = a.Sprite("assets/south_active.png", SCALING)
                    self.south_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
                    self.south_button.bottom = ( self.screen_height / 6 ) * 1
                    self.all_sprites.append(self.south_button)

            # if WEST 
            elif self.west_button.collides_with_point((x,y)):
                potential_sub_move = a.Sprite("assets/whiteMark.png", SCALING)
                potential_sub_move.center_x = self.white_sub.center_x - amount_will_move
                potential_sub_move.center_y = self.white_sub.center_y
                # will not allow it to be selected if the potential move collides with any island, collides with any piece of the white trail, or if it is past the play area
                if not len(potential_sub_move.collides_with_list(self.island_sprites)) > 0 and not len(potential_sub_move.collides_with_list(self.white_trail_sprites)) > 0 and not potential_sub_move.left < 0:
                    self.white_sub.is_move_selected = True
                    self.white_sub.selected_move = "w"
                        
                    #change out sprite
                    self.west_button.kill()
                    self.west_button = a.Sprite("assets/west_active.png", SCALING)
                    self.west_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
                    self.west_button.center_y = ( self.screen_height / 6 ) * 2
                    self.all_sprites.append(self.west_button)

            # if EAST
            elif self.east_button.collides_with_point((x,y)):
                potential_sub_move = a.Sprite("assets/whiteMark.png", SCALING)
                potential_sub_move.center_x = self.white_sub.center_x + amount_will_move
                potential_sub_move.center_y = self.white_sub.center_y
                # will not allow it to be selected if the potential move collides with any island, collides with any piece of the white trail, or if it is past the play area
                if not len(potential_sub_move.collides_with_list(self.island_sprites)) > 0 and not len(potential_sub_move.collides_with_list(self.white_trail_sprites)) > 0 and not potential_sub_move.right > SCREEN_WIDTH:
                    self.white_sub.is_move_selected = True
                    self.white_sub.selected_move = "e"
                        
                    #change out sprite
                    self.east_button.kill()
                    self.east_button = a.Sprite("assets/east_active.png", SCALING)
                    self.east_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
                    self.east_button.center_y = ( self.screen_height / 6 ) * 2
                    self.all_sprites.append(self.east_button)
            
            # if FIRE
            elif self.fire.collides_with_point((x,y)):
                # if all torpedo segments are active
                if self.torpedo_segment_1.is_active and self.torpedo_segment_2.is_active and self.torpedo_segment_3.is_active: 
                    self.white_sub.is_move_selected = True
                    self.white_sub.selected_move = "f"
                        
                    #change out sprite
                    self.fire.kill()
                    self.fire = a.Sprite("assets/fire_active.png", SCALING)
                    self.fire.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
                    self.fire.center_y = ( self.screen_height / 6 ) * 2
                    self.all_sprites.append(self.fire)
            
        # if MARK!
        if self.mark.collides_with_point((x,y)):
            if self.white_sub.is_move_selected:
                
                # NORTH 
                if self.white_sub.selected_move == "n" and self.nuclear_1.is_active:
                    self._tick_and_update_torpedo()

                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.change_y = 10 * SCALING
                    self._place_marker()

                    #change out sprite
                    self.north_button.kill()
                    self.north_button = a.Sprite("assets/north.png", SCALING)
                    self.north_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
                    self.north_button.top = ( self.screen_height / 6 ) * 3
                    self.all_sprites.append(self.north_button)

                # SOUTH 
                elif self.white_sub.selected_move == "s" and self.nuclear_1.is_active:
                    self._tick_and_update_torpedo()

                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.change_y = -10 * SCALING
                    self._place_marker()
                    
                    #change out sprite
                    self.south_button.kill()
                    self.south_button = a.Sprite("assets/south.png", SCALING)
                    self.south_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
                    self.south_button.bottom = ( self.screen_height / 6 ) * 1
                    self.all_sprites.append(self.south_button)

                # WEST 
                elif self.white_sub.selected_move == "w" and self.nuclear_1.is_active:
                    self._tick_and_update_torpedo()

                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.change_x = -10 * SCALING
                    self._place_marker()
                    
                    #change out sprite
                    self.west_button.kill()
                    self.west_button = a.Sprite("assets/west.png", SCALING)
                    self.west_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
                    self.west_button.center_y = ( self.screen_height / 6 ) * 2
                    self.all_sprites.append(self.west_button)

                # EAST 
                elif self.white_sub.selected_move == "e" and self.nuclear_1.is_active:
                    self._tick_and_update_torpedo()

                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.change_x = 10 * SCALING
                    self._place_marker()
                    
                    #change out sprite
                    self.east_button.kill()
                    self.east_button = a.Sprite("assets/east.png", SCALING)
                    self.east_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
                    self.east_button.center_y = ( self.screen_height / 6 ) * 2
                    self.all_sprites.append(self.east_button)

                # FIRE: 3 nuclear reactors must be active (only if that section is uncommented) and fire must be selected to fire a torpedo
                elif self.white_sub.selected_move == "f":
                    # if self.nuclear_1.is_active and self.nuclear_2.is_active and self.nuclear_3.is_active: # INCLUDE if you want to require reactors... 
                    
                        self._clear_torpedo_and_tick() # reset torpedo

                        self.white_sub.did_move = True
                        self.white_sub.is_move_selected = False #maybe change this to be in the update section
                        self.white_sub.selected_move = ""
                        self.white_sub.torpedo_position = [self.red_sub.center_x, self.red_sub.center_y]
                        
                        #change out sprite
                        self.fire.kill()
                        self.fire = a.Sprite("assets/fire.png", SCALING)
                        self.fire.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
                        self.fire.center_y = ( self.screen_height / 6 ) * 2
                        self.all_sprites.append(self.fire)

    def _place_marker(self):
        marker = a.Sprite("assets/whiteMarkSmall.png", SCALING)
        marker.center_x = self.white_sub.center_x
        marker.center_y = self.white_sub.center_y
        self.all_sprites.append(marker)
        self.white_trail_sprites.append(marker)

    def _tick_reactor(self, delta_time):
        self.reactor_tick += 1

    def _tick_and_update_torpedo(self):
        # increase torpedo tick
        
        self.torpedo_tick += 1
        
        # change out sprites according to torpedo_tick

        if self.torpedo_tick == 1:
            self.torpedo_segment_1.kill()
            self.torpedo_segment_1 = ToggleSprite("assets/torpedo_segment_1_active.png", SCALING)
            self.torpedo_segment_1.is_active = True
            self.torpedo_segment_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.torpedo_segment_1.top = (( self.screen_height / 6 ) * 4 )
            self.all_sprites.append(self.torpedo_segment_1)

            self.torpedo_segment_2.kill()
            self.torpedo_segment_2 = ToggleSprite("assets/torpedo_segment_2_inactive.png", SCALING)
            self.torpedo_segment_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.torpedo_segment_2.top = (( self.screen_height / 6 ) * 4 ) - 2
            self.all_sprites.append(self.torpedo_segment_2)

            self.torpedo_segment_3.kill()
            self.torpedo_segment_3 = ToggleSprite("assets/torpedo_segment_3_inactive.png", SCALING)
            self.torpedo_segment_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.torpedo_segment_3.top = (( self.screen_height / 6 ) * 4 ) - 2
            self.all_sprites.append(self.torpedo_segment_3)


        elif self.torpedo_tick == 2:
            self.torpedo_segment_1.kill()
            self.torpedo_segment_1 = ToggleSprite("assets/torpedo_segment_1_active.png", SCALING)
            self.torpedo_segment_1.is_active = True
            self.torpedo_segment_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.torpedo_segment_1.top = (( self.screen_height / 6 ) * 4 )
            self.all_sprites.append(self.torpedo_segment_1)

            self.torpedo_segment_2.kill()
            self.torpedo_segment_2 = ToggleSprite("assets/torpedo_segment_2_active.png", SCALING)
            self.torpedo_segment_2.is_active = True
            self.torpedo_segment_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.torpedo_segment_2.top = (( self.screen_height / 6 ) * 4 ) - 2
            self.all_sprites.append(self.torpedo_segment_2)

            self.torpedo_segment_3.kill()
            self.torpedo_segment_3 = ToggleSprite("assets/torpedo_segment_3_inactive.png", SCALING)
            self.torpedo_segment_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.torpedo_segment_3.top = (( self.screen_height / 6 ) * 4 ) - 2
            self.all_sprites.append(self.torpedo_segment_3)
            
        elif self.torpedo_tick == 3:
            self.torpedo_segment_1.kill()
            self.torpedo_segment_1 = ToggleSprite("assets/torpedo_segment_1_active.png", SCALING)
            self.torpedo_segment_1.is_active = True
            self.torpedo_segment_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.torpedo_segment_1.top = (( self.screen_height / 6 ) * 4 )
            self.all_sprites.append(self.torpedo_segment_1)

            self.torpedo_segment_2.kill()
            self.torpedo_segment_2 = ToggleSprite("assets/torpedo_segment_2_active.png", SCALING)
            self.torpedo_segment_2.is_active = True
            self.torpedo_segment_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.torpedo_segment_2.top = (( self.screen_height / 6 ) * 4 ) - 2
            self.all_sprites.append(self.torpedo_segment_2)

            self.torpedo_segment_3.kill()
            self.torpedo_segment_3 = ToggleSprite("assets/torpedo_segment_3_active.png", SCALING)
            self.torpedo_segment_3.is_active = True
            self.torpedo_segment_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.torpedo_segment_3.top = (( self.screen_height / 6 ) * 4 ) - 2
            self.all_sprites.append(self.torpedo_segment_3)
            
    
    def _clear_torpedo_and_tick(self):
        # reset tick and sprites
        
        self.torpedo_tick = 0

        self.torpedo_segment_1.kill()
        self.torpedo_segment_1 = ToggleSprite("assets/torpedo_segment_1_inactive.png", SCALING)
        self.torpedo_segment_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
        self.torpedo_segment_1.top = (( self.screen_height / 6 ) * 4 )
        self.all_sprites.append(self.torpedo_segment_1)

        self.torpedo_segment_2.kill()
        self.torpedo_segment_2 = ToggleSprite("assets/torpedo_segment_2_inactive.png", SCALING)
        self.torpedo_segment_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
        self.torpedo_segment_2.top = (( self.screen_height / 6 ) * 4 ) - 2
        self.all_sprites.append(self.torpedo_segment_2)

        self.torpedo_segment_3.kill()
        self.torpedo_segment_3 = ToggleSprite("assets/torpedo_segment_3_inactive.png", SCALING)
        self.torpedo_segment_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
        self.torpedo_segment_3.top = (( self.screen_height / 6 ) * 4 ) - 2
        self.all_sprites.append(self.torpedo_segment_3)


    def _update_reactor_from_tick(self):
        # get the timer tick
        tick = self.reactor_tick
        
        if tick == 0:
            # change out nuclear sprites

            self.nuclear_1.kill()
            self.nuclear_1 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill()
            self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill()
            self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_3)
        
        elif tick == 1:
            # change out nuclear sprites

            self.nuclear_1.kill()
            self.nuclear_1 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_1.is_active = True
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill()
            self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill()
            self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_3)
        
        elif tick == 2:
            # change out nuclear sprites

            self.nuclear_1.kill()
            self.nuclear_1 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_1.is_active = True
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill()
            self.nuclear_2 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_2.is_active = True
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill()
            self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_3)
        
        elif tick == 3:
            # change out nuclear sprites

            self.nuclear_1.kill()
            self.nuclear_1 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_1.is_active = True
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill()
            self.nuclear_2 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_2.is_active = True
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill()
            self.nuclear_3 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_3.is_active = True
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_3)
        
        elif tick > 3:
            # change out nuclear sprites

            self.nuclear_1.kill()
            self.nuclear_1 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill()
            self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill()
            self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = (( self.screen_height / 6 ) * 5 )
            self.all_sprites.append(self.nuclear_3)

            # reset the timer tick

            self.reactor_tick = 0

            # take a damage
            if TAKE_REACTOR_DAMAGE:
                self._take_damage()
    

    def _clear_reactors_and_tick(self):
        # change out nuclear sprites

        self.nuclear_1.kill()
        self.nuclear_1 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
        self.nuclear_1.top = (( self.screen_height / 6 ) * 5 )
        self.all_sprites.append(self.nuclear_1)

        self.nuclear_2.kill()
        self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
        self.nuclear_2.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_2)

        self.nuclear_3.kill()
        self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
        self.nuclear_3.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_3)

        # reset the timer tick

        self.reactor_tick = 0
    

    def _take_damage(self, amount=1):
        if amount == 1:
            if self.heart_2.is_active:
                #change out heart sprites

                self.heart_1.kill()
                self.heart_1 = ToggleSprite("assets/heart_full.png", SCALING)
                self.heart_1.is_active = True
                self.heart_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*2)
                self.heart_1.top = ( self.screen_height / 6 ) * 6 - 10
                self.all_sprites.append(self.heart_1)

                self.heart_2.kill()
                self.heart_2 = ToggleSprite("assets/heart_empty.png", SCALING)
                self.heart_2.is_active = False
                self.heart_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*4)
                self.heart_2.top = ( self.screen_height / 6 ) * 6 - 10
                self.all_sprites.append(self.heart_2)
            elif self.heart_1.is_active:
                #change out heart sprites

                self.heart_1.kill()
                self.heart_1 = ToggleSprite("assets/heart_empty.png", SCALING)
                self.heart_1.is_active = False
                self.heart_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*2)
                self.heart_1.top = ( self.screen_height / 6 ) * 6 - 10
                self.all_sprites.append(self.heart_1)

                self.heart_2.kill()
                self.heart_2 = ToggleSprite("assets/heart_empty.png", SCALING)
                self.heart_2.is_active = False
                self.heart_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*4)
                self.heart_2.top = ( self.screen_height / 6 ) * 6 - 10
                self.all_sprites.append(self.heart_2)

                # destroy white sub 

                self.white_sub.is_destroyed = True
        
        elif amount > 1:
            #change out heart sprites

            self.heart_1.kill()
            self.heart_1 = ToggleSprite("assets/heart_empty.png", SCALING)
            self.heart_1.is_active = False
            self.heart_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*2)
            self.heart_1.top = ( self.screen_height / 6 ) * 6 - 10
            self.all_sprites.append(self.heart_1)

            self.heart_2.kill()
            self.heart_2 = ToggleSprite("assets/heart_empty.png", SCALING)
            self.heart_2.is_active = False
            self.heart_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*4)
            self.heart_2.top = ( self.screen_height / 6 ) * 6 - 10
            self.all_sprites.append(self.heart_2)

            # destroy white sub 

            self.white_sub.is_destroyed = True


    def on_close(self):
        super().on_close()
        self.sending_socket.close()
        self.radio_opperator.is_listening = False
        self.radio_opperator.join()