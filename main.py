from RedOctoberGame import RedOctoberGame
from Constants import *

def main():
    # differentiate between the two computers 
    choice = input("white or black computer? [w, b] > ")
    if choice == "w":
        ip = WHITE_IP
        enemy_ip = BLACK_IP
    else:
        ip = BLACK_IP
        enemy_ip = WHITE_IP
    
    red_october_game = RedOctoberGame(ip, enemy_ip)
    red_october_game.setup()
    red_october_game.run()


if __name__ == "__main__":
    main()