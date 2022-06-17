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

    def setup(self):
        a.set_background_color(a.color_from_hex_string(PALETTE_BLUE.upper()))

        self.mark = a.Sprite("assets/mark.png", SCALING)
        self.mark.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
        self.mark.bottom = 0 + 10
        self.all_sprites.append(self.mark)

        self.fire = a.Sprite("assets/fire.png", SCALING)
        self.fire.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
        self.fire.center_y = ( self.screen_height / 5 ) * 2
        self.all_sprites.append(self.fire)

        self.north_button = a.Sprite("assets/north.png", SCALING)
        self.north_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
        self.north_button.top = ( self.screen_height / 5 ) * 3
        self.all_sprites.append(self.north_button)

        self.south_button = a.Sprite("assets/south.png", SCALING)
        self.south_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
        self.south_button.bottom = ( self.screen_height / 5 ) * 1
        self.all_sprites.append(self.south_button)

        self.east_button = a.Sprite("assets/east.png", SCALING)
        self.east_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
        self.east_button.center_y = ( self.screen_height / 5 ) * 2
        self.all_sprites.append(self.east_button)

        self.west_button = a.Sprite("assets/west.png", SCALING)
        self.west_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
        self.west_button.center_y = ( self.screen_height / 5 ) * 2
        self.all_sprites.append(self.west_button)

        self.nuclear_1 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
        self.nuclear_1.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_1)

        self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
        self.nuclear_2.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_2)

        self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
        self.nuclear_3.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_3)

        self.heart_1 = ToggleSprite("assets/heart_full.png", SCALING)
        self.heart_1.is_active = True
        self.heart_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*2)
        self.heart_1.top = ( self.screen_height / 5 ) * 5 - 10
        self.all_sprites.append(self.heart_1)

        self.heart_2 = ToggleSprite("assets/heart_full.png", SCALING)
        self.heart_2.is_active = True
        self.heart_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*4)
        self.heart_2.top = ( self.screen_height / 5 ) * 5 - 10
        self.all_sprites.append(self.heart_2)

        island_positions = [14, 10, 15, 11, 24, 20, 1, 27, 2, 24, 16, 12, 16, 7, 16, 9, 16, 30, 15, 10, 20, 7, 24, 19, 12, 24, 30, 7, 24, 30, 3, 16, 22, 3, 10, 6, 24, 30, 10, 11, 19, 6, 16, 30, 8, 1, 23, 23, 27, 23, 30, 1, 4, 27, 13, 18, 9, 26, 16, 15, 29, 13, 28, 25, 27, 23, 5, 1, 6, 30, 28, 29, 23, 2, 21, 27, 24, 7, 14, 27, 11, 2, 6, 15, 11, 3, 13, 13, 19, 30, 10, 17, 25, 19, 3, 13, 28, 6, 11, 28, 3, 7, 14, 27, 26, 29, 24, 10, 15, 28, 5, 5, 18, 4, 16, 4, 7, 23, 12, 12, 8, 13, 3, 8, 9, 5, 10, 17, 1, 8, 15, 22, 24, 22, 17, 19, 23, 4, 2, 6, 5, 27, 12, 29, 20, 24, 12, 16, 8, 30, 17, 6, 28, 5, 16, 15, 16, 15, 11, 18, 23, 9, 29, 12, 1, 4, 6, 27, 9, 2, 23, 15, 23, 30, 1, 3, 13, 8, 24, 18, 3, 10, 6, 18, 17, 23, 19, 3, 10, 6, 15, 29, 1, 28, 29, 10, 24, 11, 26, 10]
        # island_positions = [19, 11, 3, 25, 28, 20, 30, 7, 11, 4, 26, 15, 10, 25, 4, 22, 3, 14, 30, 20, 14, 6, 3, 8, 6, 27, 16, 7, 17, 1, 20, 10, 13, 30, 10, 26, 12, 30, 11, 26, 30, 1, 16, 15, 21, 1, 20, 26, 30, 16, 3, 2, 7, 12, 10, 29, 16, 20, 22, 10, 26, 20, 11, 5, 21, 11, 29, 25, 8, 6, 26, 21, 2, 26, 16, 14, 21, 9, 25, 14, 5, 20, 22, 1, 26, 9, 8, 11, 13, 5, 3, 28, 27, 18, 25, 18, 10, 14, 13, 22, 29, 12, 26, 8, 9, 9, 13, 11, 6, 16, 1, 16, 6, 16, 7, 1, 29, 12, 16, 28, 12, 4, 27, 10, 18, 21, 8, 15, 21, 30, 24, 14, 26, 8, 29, 20, 13, 23, 15, 30, 8, 3, 21, 2, 6, 12, 15, 25, 30, 29, 30, 13, 2, 1, 30, 3, 1, 16, 22, 29, 30, 21, 3, 14, 5, 2, 21, 4, 6, 23, 4, 16, 17, 26, 27, 1, 27, 3, 29, 5, 1, 26, 9, 7, 22, 7, 6, 13, 16, 4, 26, 5, 23, 15, 20, 30, 16, 14, 1, 15]
        # island_positions = [26, 9, 23, 20, 27, 4, 9, 14, 5, 21, 30, 10, 4, 15, 26, 6, 15, 25, 15, 7, 10, 8, 11, 10, 29, 25, 7, 26, 16, 21, 7, 8, 24, 20, 6, 18, 23, 26, 5, 25, 30, 2, 7, 18, 29, 25, 18, 23, 23, 17, 6, 10, 7, 11, 29, 25, 14, 5, 10, 5, 1, 16, 23, 10, 2, 30, 27, 25, 1, 10, 26, 13, 14, 4, 28, 13, 6, 29, 18, 4, 2, 7, 2, 18, 28, 27, 5, 25, 4, 20, 1, 3, 2, 7, 30, 30, 2, 13, 28, 19, 22, 27, 24, 17, 9, 24, 19, 18, 3, 10, 9, 4, 11, 17, 13, 23, 21, 7, 11, 6, 18, 2, 12, 11, 28, 3, 2, 29, 19, 9, 21, 11, 1, 8, 18, 25, 16, 4, 19, 9, 27, 4, 25, 23, 8, 12, 25, 20, 20, 23, 20, 9, 29, 22, 25, 30, 30, 8, 22, 27, 25, 24, 1, 21, 11, 25, 18, 2, 27, 20, 29, 27, 10, 14, 9, 25, 20, 13, 23, 14, 14, 26, 12, 9, 22, 10, 17, 18, 27, 22, 26, 28, 12, 1, 18, 30, 26, 3, 30, 14]
        # island_positions = [11, 1, 11, 24, 19, 10, 12, 26, 15, 8, 3, 29, 20, 9, 22, 22, 6, 22, 18, 8, 24, 16, 16, 26, 27, 13, 11, 17, 7, 15, 22, 28, 22, 20, 21, 27, 15, 27, 22, 9, 11, 7, 2, 15, 12, 22, 28, 7, 15, 7, 28, 20, 3, 12, 10, 3, 16, 6, 30, 19, 13, 2, 1, 18, 1, 16, 26, 9, 28, 24, 30, 9, 30, 29, 23, 7, 10, 27, 27, 30, 7, 17, 15, 28, 7, 1, 17, 14, 6, 25, 12, 4, 14, 5, 2, 29, 7, 17, 4, 7, 17, 8, 30, 11, 21, 29, 10, 23, 6, 3, 29, 17, 12, 23, 8, 29, 12, 14, 26, 7, 20, 30, 4, 25, 19, 15, 28, 24, 27, 3, 22, 23, 1, 6, 19, 7, 5, 21, 21, 5, 28, 1, 16, 21, 4, 4, 24, 25, 9, 30, 14, 12, 11, 14, 7, 20, 29, 29, 24, 5, 18, 26, 11, 12, 17, 13, 26, 27, 10, 24, 19, 19, 27, 1, 22, 18, 27, 21, 22, 15, 17, 4, 11, 18, 21, 8, 22, 1, 29, 2, 18, 25, 17, 3, 25, 27, 22, 25, 7, 11]
        # island_positions = [16, 8, 12, 13, 11, 21, 16, 13, 30, 18, 16, 26, 17, 27, 19, 26, 29, 16, 14, 29, 20, 25, 12, 11, 23, 5, 3, 12, 5, 13, 23, 22, 17, 22, 22, 3, 11, 22, 10, 14, 8, 19, 21, 1, 29, 28, 13, 22, 1, 25, 6, 4, 29, 12, 26, 26, 14, 24, 20, 4, 28, 22, 25, 29, 20, 13, 8, 26, 23, 19, 30, 13, 10, 19, 17, 4, 3, 26, 20, 17, 27, 10, 28, 15, 21, 14, 9, 18, 29, 17, 10, 4, 9, 24, 3, 27, 10, 5, 7, 16, 22, 1, 12, 19, 21, 26, 17, 5, 2, 14, 9, 6, 9, 20, 25, 9, 13, 13, 10, 5, 12, 16, 30, 25, 6, 29, 5, 13, 12, 7, 8, 10, 6, 26, 13, 27, 6, 9, 20, 7, 22, 24, 8, 25, 10, 23, 29, 8, 20, 4, 9, 10, 14, 24, 23, 8, 5, 4, 21, 15, 9, 13, 14, 25, 4, 15, 1, 17, 23, 30, 10, 1, 18, 24, 1, 22, 24, 13, 7, 12, 15, 16, 11, 27, 9, 9, 5, 11, 29, 8, 20, 17, 13, 15, 9, 15, 12, 23, 26, 5]


        for i in range(25):
            self.i = a.Sprite("assets/island.png", SCALING)
            self.i.right = UNIT_SIZE * island_positions.pop()
            self.i.bottom = UNIT_SIZE * island_positions.pop()
            self.all_sprites.append(self.i)
            self.island_sprites.append(self.i)

        for i in range(15):
            self.i = a.Sprite("assets/island_tall.png", SCALING)
            self.i.right = UNIT_SIZE * island_positions.pop()
            self.i.bottom = UNIT_SIZE * island_positions.pop()
            self.all_sprites.append(self.i)
            self.island_sprites.append(self.i)

        for i in range(15):
            self.i = a.Sprite("assets/island_wide.png", SCALING)
            self.i.right = UNIT_SIZE * island_positions.pop()
            self.i.bottom = UNIT_SIZE * island_positions.pop()
            self.all_sprites.append(self.i)
            self.island_sprites.append(self.i)

        for i in range(10):
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

        # schedule the reactor tick to continually tick up 
        a.schedule(self._tick_reactor, REACTOR_TICK_TIME)

        # send the READY flag to the other player
        self.data_to_send["position"] = "READY"
        # used code from https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
        data_to_send_local = json.dumps(self.data_to_send) # convert to json string
        data_to_send_local = data_to_send_local.encode() # convert to bytes
        self.sending_socket.sendall(data_to_send_local)

        # block until we receive the READY flag
        while True:
            if self.radio_opperator.ready == True:
                break




    def on_update(self, delta_time : float):
        # Add move to the data to send, if moved 
        if self.white_sub.did_move:
            # self.data_to_send["move_log"].append((self.white_sub.change_x, self.white_sub.change_y))
            self.data_to_send["move_log"] = (self.white_sub.change_x, self.white_sub.change_y)
        
        # NOTE: check collisions (if applicable for this game) before updating sprites

        # update sprites
        self._update_reactor_from_tick()

        with self.lock:
            if self.radio_opperator.enemy_last_move[0] != 0 or self.radio_opperator.enemy_last_move[1] != 0:
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

        self.all_sprites.update()

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
            if self.north_button.collides_with_point((x,y)):
                self.white_sub.is_move_selected = True
                self.white_sub.selected_move = "n"
                    
                #change out sprite
                self.north_button.kill()
                self.north_button = a.Sprite("assets/north_active.png", SCALING)
                self.north_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
                self.north_button.top = ( self.screen_height / 5 ) * 3
                self.all_sprites.append(self.north_button)

            # if SOUTH 
            elif self.south_button.collides_with_point((x,y)):
                self.white_sub.is_move_selected = True
                self.white_sub.selected_move = "s"
                    
                #change out sprite
                self.south_button.kill()
                self.south_button = a.Sprite("assets/south_active.png", SCALING)
                self.south_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
                self.south_button.bottom = ( self.screen_height / 5 ) * 1
                self.all_sprites.append(self.south_button)

            # if WEST 
            elif self.west_button.collides_with_point((x,y)):
                self.white_sub.is_move_selected = True
                self.white_sub.selected_move = "w"
                    
                #change out sprite
                self.west_button.kill()
                self.west_button = a.Sprite("assets/west_active.png", SCALING)
                self.west_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
                self.west_button.center_y = ( self.screen_height / 5 ) * 2
                self.all_sprites.append(self.west_button)

            # if EAST
            elif self.east_button.collides_with_point((x,y)):
                self.white_sub.is_move_selected = True
                self.white_sub.selected_move = "e"
                    
                #change out sprite
                self.east_button.kill()
                self.east_button = a.Sprite("assets/east_active.png", SCALING)
                self.east_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
                self.east_button.center_y = ( self.screen_height / 5 ) * 2
                self.all_sprites.append(self.east_button)
            
            # if FIRE
            elif self.fire.collides_with_point((x,y)):
                self.white_sub.is_move_selected = True
                self.white_sub.selected_move = "f"
                    
                #change out sprite
                self.fire.kill()
                self.fire = a.Sprite("assets/fire_active.png", SCALING)
                self.fire.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
                self.fire.center_y = ( self.screen_height / 5 ) * 2
                self.all_sprites.append(self.fire)
            
        # if MARK!
        if self.mark.collides_with_point((x,y)):
            if self.white_sub.is_move_selected:
                
                # NORTH 
                if self.white_sub.selected_move == "n" and self.nuclear_1.is_active:
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
                    self.north_button.top = ( self.screen_height / 5 ) * 3
                    self.all_sprites.append(self.north_button)

                # SOUTH 
                elif self.white_sub.selected_move == "s" and self.nuclear_1.is_active:
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
                    self.south_button.bottom = ( self.screen_height / 5 ) * 1
                    self.all_sprites.append(self.south_button)

                # WEST 
                elif self.white_sub.selected_move == "w" and self.nuclear_1.is_active:
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
                    self.west_button.center_y = ( self.screen_height / 5 ) * 2
                    self.all_sprites.append(self.west_button)

                # EAST 
                elif self.white_sub.selected_move == "e" and self.nuclear_1.is_active:
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
                    self.east_button.center_y = ( self.screen_height / 5 ) * 2
                    self.all_sprites.append(self.east_button)

                # FIRE: 2 nuclear reactors must be active and fire must be selected to fire a torpedo
                elif self.white_sub.selected_move == "f" and self.nuclear_1.is_active and self.nuclear_2.is_active:
                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self.white_sub.torpedo_position = [self.red_sub.center_x, self.red_sub.center_y]
                    
                    #change out sprite
                    self.fire.kill()
                    self.fire = a.Sprite("assets/fire.png", SCALING)
                    self.fire.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
                    self.fire.center_y = ( self.screen_height / 5 ) * 2
                    self.all_sprites.append(self.fire)

    def _place_marker(self):
        marker = a.Sprite("assets/whiteMarkSmall.png", SCALING)
        marker.center_x = self.white_sub.center_x
        marker.center_y = self.white_sub.center_y
        self.all_sprites.append(marker)
        self.white_trail_sprites.append(marker)

    def _tick_reactor(self, delta_time):
        self.reactor_tick += 1

    def _update_reactor_from_tick(self):
        # get the timer tick
        tick = self.reactor_tick
        
        if tick == 0:
            # change out nuclear sprites

            self.nuclear_1.kill
            self.nuclear_1 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill
            self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill
            self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_3)
        
        elif tick == 1:
            # change out nuclear sprites

            self.nuclear_1.kill
            self.nuclear_1 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_1.is_active = True
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill
            self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill
            self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_3)
        
        elif tick == 2:
            # change out nuclear sprites

            self.nuclear_1.kill
            self.nuclear_1 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_1.is_active = True
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill
            self.nuclear_2 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_2.is_active = True
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill
            self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_3)
        
        elif tick == 3:
            # change out nuclear sprites

            self.nuclear_1.kill
            self.nuclear_1 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_1.is_active = True
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill
            self.nuclear_2 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_2.is_active = True
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill
            self.nuclear_3 = ToggleSprite("assets/nuclear_active.png", SCALING)
            self.nuclear_3.is_active = True
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_3)
        
        elif tick > 3:
            # change out nuclear sprites

            self.nuclear_1.kill
            self.nuclear_1 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
            self.nuclear_1.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_1)

            self.nuclear_2.kill
            self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
            self.nuclear_2.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_2)

            self.nuclear_3.kill
            self.nuclear_3 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
            self.nuclear_3.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
            self.nuclear_3.top = ( self.screen_height / 5 ) * 4
            self.all_sprites.append(self.nuclear_3)

            # reset the timer tick

            self.reactor_tick = 0

            # take a damage

            self._take_damage()
    

    def _clear_reactors_and_tick(self):
        # change out nuclear sprites

        self.nuclear_1.kill
        self.nuclear_1 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
        self.nuclear_1.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_1)

        self.nuclear_2.kill
        self.nuclear_2 = ToggleSprite("assets/nuclear_inactive.png", SCALING)
        self.nuclear_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
        self.nuclear_2.top = ( self.screen_height / 5 ) * 4
        self.all_sprites.append(self.nuclear_2)

        self.nuclear_3.kill
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

                self.heart_1 = ToggleSprite("assets/heart_full.png", SCALING)
                self.heart_1.is_active = True
                self.heart_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*2)
                self.heart_1.top = ( self.screen_height / 5 ) * 5 - 10
                self.all_sprites.append(self.heart_1)

                self.heart_2 = ToggleSprite("assets/heart_empty.png", SCALING)
                self.heart_2.is_active = False
                self.heart_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*4)
                self.heart_2.top = ( self.screen_height / 5 ) * 5 - 10
                self.all_sprites.append(self.heart_2)
            elif self.heart_1.is_active:
                #change out heart sprites

                self.heart_1 = ToggleSprite("assets/heart_empty.png", SCALING)
                self.heart_1.is_active = False
                self.heart_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*2)
                self.heart_1.top = ( self.screen_height / 5 ) * 5 - 10
                self.all_sprites.append(self.heart_1)

                self.heart_2 = ToggleSprite("assets/heart_empty.png", SCALING)
                self.heart_2.is_active = False
                self.heart_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*4)
                self.heart_2.top = ( self.screen_height / 5 ) * 5 - 10
                self.all_sprites.append(self.heart_2)

                # destroy white sub 

                self.white_sub.is_destroyed = True
        
        elif amount > 1:
            #change out heart sprites

            self.heart_1 = ToggleSprite("assets/heart_full.png", SCALING)
            self.heart_1.is_active = False
            self.heart_1.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*2)
            self.heart_1.top = ( self.screen_height / 5 ) * 5 - 10
            self.all_sprites.append(self.heart_1)

            self.heart_2 = ToggleSprite("assets/heart_empty.png", SCALING)
            self.heart_2.is_active = False
            self.heart_2.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 6)*4)
            self.heart_2.top = ( self.screen_height / 5 ) * 5 - 10
            self.all_sprites.append(self.heart_2)

            # destroy white sub 

            self.white_sub.is_destroyed = True


    def on_close(self):
        self.sending_socket.close()
        self.radio_opperator.is_listening = False
        self.radio_opperator.join()
        self.reactor_timer.is_running = False
        self.reactor_timer.join()
        super().on_close()