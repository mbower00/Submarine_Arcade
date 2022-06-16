import json
import threading as th
import socket as so
from turtle import position
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

    def run(self):
        with so.socket() as s:
            s.bind((self.ip, SERVER_PORT))
            s.listen()
            connection_socket, connection_address = s.accept()
            with connection_socket as cs:
                while self.is_listening:
                    # used code from https://www.geeksforgeeks.org/python-interconversion-between-dictionary-and-bytes/
                    data = cs.recv(90)
                    print(f"RADIO -- size: {data.__sizeof__()} - data: ", end="")
                    data = data.decode(encoding="utf8")
                    data = json.loads(data)
                    print(f"{data}")
                    with self.lock:
                        self.enemy_position = (float(data["position"][0]), float(data["position"][1]))
                        self.enemy_last_move = (float(data["move_log"][0]), float(data["move_log"][1]))
                        if data["torpedo_position"] is not None:
                            self.enemy_torpedo_position = (float(data["torpedo_position"][0]), float(data["torpedo_position"][1]))
                        else:
                            self.enemy_torpedo_position = None