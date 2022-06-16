import time
import arcade as a
import socket as so
import threading as th
from Constants import *
from ControllerWindow import ControllerWindow
from RadioOpperator import RadioOpperator
from SubmarineSprite import SubmarineSprite
import json


class RedOctoberGame(a.Window):
    def __init__(self, ip, enemy_ip):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.all_sprites = a.SpriteList()
        self.ip = ip
        self.enemy_ip = enemy_ip
        self.lock = th.Lock()
        self.radio_opperator = RadioOpperator(self.ip, self.lock)
        self.sending_socket = so.socket()

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

        #start server thread
        self.radio_opperator.start()

        self.data_to_send = {"position": self.white_sub.position, "move_log": []}
        self.sending_socket.bind((self.ip, CLIENT_PORT))
        self.sending_socket.connect((self.enemy_ip, SERVER_PORT))

        self.controller_window = ControllerWindow()
        self.controller_window.run()

    def on_update(self, delta_time : float):
        if self.white_sub.did_move:
            # self.data_to_send["move_log"].append((self.white_sub.change_x, self.white_sub.change_y))
            self.data_to_send["move_log"] = (self.white_sub.change_x, self.white_sub.change_y)
        
        # NOTE: check collisions (if applicable for this game) before updating sprites

        self.red_sub.center_x = self.radio_opperator.enemy_position[0]
        self.red_sub.center_y = self.radio_opperator.enemy_position[1]
        self.all_sprites.update()

        if self.white_sub.did_move:
            self.data_to_send["position"] = self.white_sub.position
            
            # used code from https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
            data_to_send_local = json.dumps(self.data_to_send) # convert to json string
            # data_to_send_local = str(self.data_to_send)
            data_to_send_local = data_to_send_local.encode() # convert to bytes
            self.sending_socket.sendall(data_to_send_local)
            
            self.white_sub.did_move = False

    def on_draw(self):
        a.start_render()
        self.all_sprites.draw()

    def on_key_release(self, symbol: int, modifiers: int):
        if not self.white_sub.did_move:
            if symbol == a.key.UP or symbol == a.key.W:
                self.white_sub.change_y = 10 * SCALING
                self.white_sub.did_move = True
            elif symbol == a.key.DOWN or symbol == a.key.S:
                self.white_sub.change_y = -10 * SCALING
                self.white_sub.did_move = True
            elif symbol == a.key.LEFT or symbol == a.key.A:
                self.white_sub.change_x = -10 * SCALING
                self.white_sub.did_move = True
            elif symbol == a.key.RIGHT or symbol == a.key.D:
                self.white_sub.change_x = 10 * SCALING
                self.white_sub.did_move = True


    def on_close(self):
        self.sending_socket.close()
        self.radio_opperator.is_listening = False
        self.radio_opperator.join()
        super().on_close()