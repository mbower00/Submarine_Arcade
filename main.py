import threading
from ControllerWindow import ControllerWindow
from RedOctoberGame import RedOctoberGame
from Constants import *

def main():
    choice = input("white or black computer? [w, b] > ")
    if choice == "w":
        ip = WHITE_IP
        enemy_ip = BLACK_IP
    else:
        ip = BLACK_IP
        enemy_ip = WHITE_IP
    
    controller_window = ControllerWindow()
    red_october_game = RedOctoberGame(ip, enemy_ip, controller_window)
    red_october_game.setup()
    red_october_game_thread = threading.Thread(target=run_window, args=(red_october_game,))
    controller_window_thread = threading.Thread(target=run_window, args=(controller_window,))
    controller_window_thread.start()
    red_october_game_thread.start()

def run_window(window):
    window.run()

if __name__ == "__main__":
    main()