import time
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
        self.ip = ip
        self.enemy_ip = enemy_ip
        self.timer_lock = th.Lock()
        self.radio_opperator = RadioOpperator(self.ip)
        self.sending_socket = so.socket()
        self.reactor_tick = 0

    def setup(self):
        a.set_background_color(a.color_from_hex_string(PALETTE_BLUE.upper()))

        self.red_sub = SubmarineSprite("assets/redMark.png", SCALING)
        self.red_sub.center_x = self.red_sub.right
        self.red_sub.center_y = self.red_sub.bottom
        self.all_sprites.append(self.red_sub)

        self.white_sub = SubmarineSprite("assets/whiteMark.png", SCALING)
        self.white_sub.center_x = self.white_sub.right
        self.white_sub.center_y = self.white_sub.bottom
        self.all_sprites.append(self.white_sub)

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

        #start server thread
        self.radio_opperator.start()

        self.data_to_send = {"position": self.white_sub.position, "move_log": [], "torpedo_position": None}
        self.sending_socket.bind((self.ip, CLIENT_PORT))
        self.sending_socket.connect((self.enemy_ip, SERVER_PORT))

        # schedule the reactor tick to continually tick up 
        a.schedule(self._tick_reactor, REACTOR_TICK_TIME)

    def on_update(self, delta_time : float):
        # Add move to the data to send, if moved 
        if self.white_sub.did_move:
            # self.data_to_send["move_log"].append((self.white_sub.change_x, self.white_sub.change_y))
            self.data_to_send["move_log"] = (self.white_sub.change_x, self.white_sub.change_y)
        
        # NOTE: check collisions (if applicable for this game) before updating sprites

        # update sprites
        self._update_reactor_from_tick()
        self.red_sub.center_x = self.radio_opperator.enemy_position[0] # get enemy x position
        self.red_sub.center_y = self.radio_opperator.enemy_position[1] # get enemy y position
        self.all_sprites.update()
        
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

    # def on_key_release(self, symbol: int, modifiers: int):
    #     if not self.white_sub.did_move:
    #         if symbol == a.key.UP or symbol == a.key.W:
    #             self.white_sub.change_y = 10 * SCALING
    #             self.white_sub.did_move = True
    #         elif symbol == a.key.DOWN or symbol == a.key.S:
    #             self.white_sub.change_y = -10 * SCALING
    #             self.white_sub.did_move = True
    #         elif symbol == a.key.LEFT or symbol == a.key.A:
    #             self.white_sub.change_x = -10 * SCALING
    #             self.white_sub.did_move = True
    #         elif symbol == a.key.RIGHT or symbol == a.key.D:
    #             self.white_sub.change_x = 10 * SCALING
    #             self.white_sub.did_move = True
    
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
                

                if self.white_sub.selected_move == "n":
                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.change_y = 10 * SCALING
                    
                    #change out sprite
                    self.north_button.kill()
                    self.north_button = a.Sprite("assets/north.png", SCALING)
                    self.north_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
                    self.north_button.top = ( self.screen_height / 5 ) * 3
                    self.all_sprites.append(self.north_button)


                elif self.white_sub.selected_move == "s":
                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.change_y = -10 * SCALING
                    
                    #change out sprite
                    self.south_button.kill()
                    self.south_button = a.Sprite("assets/south.png", SCALING)
                    self.south_button.center_x = SCREEN_WIDTH + ( (SCREEN_WIDTH // 2) / 2)
                    self.south_button.bottom = ( self.screen_height / 5 ) * 1
                    self.all_sprites.append(self.south_button)

                elif self.white_sub.selected_move == "w":
                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.change_x = -10 * SCALING
                    
                    #change out sprite
                    self.west_button.kill()
                    self.west_button = a.Sprite("assets/west.png", SCALING)
                    self.west_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*1)
                    self.west_button.center_y = ( self.screen_height / 5 ) * 2
                    self.all_sprites.append(self.west_button)


                elif self.white_sub.selected_move == "e":
                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.change_x = 10 * SCALING
                    
                    #change out sprite
                    self.east_button.kill()
                    self.east_button = a.Sprite("assets/east.png", SCALING)
                    self.east_button.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*3)
                    self.east_button.center_y = ( self.screen_height / 5 ) * 2
                    self.all_sprites.append(self.east_button)

                # all nuclear reactors must be active and fire must be selected to fire a torpedo
                elif self.white_sub.selected_move == "f" and self.nuclear_1.is_active and self.nuclear_2.is_active and self.nuclear_3.is_active:
                    self.white_sub.did_move = True
                    self.white_sub.is_move_selected = False #maybe change this to be in the update section
                    self.white_sub.selected_move = ""
                    self._clear_reactors_and_tick()
                    self.white_sub.torpedo_position = [self.red_sub.center_x, self.red_sub.center_y]
                    
                    #change out sprite
                    self.fire.kill()
                    self.fire = a.Sprite("assets/fire.png", SCALING)
                    self.fire.center_x = SCREEN_WIDTH + (((SCREEN_WIDTH // 2) / 4)*2)
                    self.fire.center_y = ( self.screen_height / 5 ) * 2
                    self.all_sprites.append(self.fire)

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