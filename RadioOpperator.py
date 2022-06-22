# used socket code from https://realpython.com/python-sockets/

import json
import threading as th
import socket as so
from Constants import *

class RadioOpperator(th.Thread):
    def __init__(self, ip:str, lock):
        super().__init__()
        self.ip = ip
        self.is_listening = True
        self.enemy_position = (0,0)
        self.enemy_last_move = (0,0)
        self.enemy_torpedo_position = None
        self.lock = lock
        self.is_other_player_ready = False
        self.is_victory = None

    def run(self):
        with so.socket() as s:
            s.bind((self.ip, SERVER_PORT))
            s.listen()
            connection_socket, connection_address = s.accept()
            with connection_socket as cs:
                while self.is_listening:
                    # used code from https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
                    data = cs.recv(115)
                    if SHOW_RADIO:
                        print(f"RADIO -- size: {data.__sizeof__()} - data: ", end="")
                    data = data.decode(encoding="utf8")
                    data = json.loads(data)
                    if SHOW_RADIO:
                        print(f"{data}")
                    if data["position"] == "READY": # first time (readying up)...
                        self.is_other_player_ready = True
                    else: # usual procedure...
                        with self.lock:
                            if data["position"] == "VICTORY":
                                self.is_victory = True
                            else:
                                self.enemy_position = (float(data["position"][0]), float(data["position"][1]))
                                self.enemy_last_move = (float(data["move_log"][0]), float(data["move_log"][1]))
                                if data["torpedo_position"] is not None:
                                    self.enemy_torpedo_position = (float(data["torpedo_position"][0]), float(data["torpedo_position"][1]))
                                else:
                                    self.enemy_torpedo_position = None