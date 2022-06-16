from turtle import update
import arcade
import random
import Constants

class SpaceShooter(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.clouds_list = arcade.SpriteList()  
        self.enemies_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        self.paused = False

    def on_update(self, delta_time: float):
        if self.paused:
            return

        if self.player.collides_with_list(self.enemies_list):
            arcade.close_window()

        self.all_sprites.update()

        if self.player.top > self.height:
            self.player.top = self.height

        if self.player.right > self.width:
            self.player.right = self.width

        if self.player.bottom < 0:
            self.player.bottom = 0

        if self.player.left < 0:
            self.player.left = 0
    
    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()

    def setup(self):
        arcade.set_background_color(arcade.color.BEIGE)

        self.player = arcade.Sprite("assets/fremen_down_right_raised.png", Constants.SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

        arcade.schedule(self.add_enemy, 0.25)
        arcade.schedule(self.add_cloud, 5.0)

    def add_enemy(self, delta_time : float):
        enemy = FlyingSprite("assets/fremen_down_left_lowered.png", Constants.SCALING)

        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        enemy.velocity = (random.randint(-20, -5), 0)

        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_cloud(self, delta_time:float):
        cloud = FlyingSprite("assets/Screenshot.png", Constants.SCALING)
        
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height - 10)

        cloud.velocity = (random.randint(-5, -1), 0)

        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()
        
        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.W or symbol == arcade.key.UP:
            self.player.change_y = 5

        if symbol == arcade.key.S or symbol == arcade.key.DOWN:
            self.player.change_y = -5

        if symbol == arcade.key.A or symbol == arcade.key.LEFT:
            self.player.change_x = -5

        if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
            self.player.change_x = 5


    def on_key_release(self, symbol: int, modifiers: int):
            """Undo movement vectors when movement keys are released
            Arguments:
                symbol {int} -- Which key was pressed
                modifiers {int} -- Which modifiers were pressed
            """
            if (
                symbol == arcade.key.W
                or symbol == arcade.key.S
                or symbol == arcade.key.UP
                or symbol == arcade.key.DOWN
            ):
                self.player.change_y = 0

            if (
                symbol == arcade.key.A
                or symbol == arcade.key.D
                or symbol == arcade.key.LEFT
                or symbol == arcade.key.RIGHT
            ):
                self.player.change_x = 0



class FlyingSprite(arcade.Sprite):
    def update(self):
        super().update()

        if self.right < 0:
            self.remove_from_sprite_lists()


if __name__ == "__main__":
    space_shooter = SpaceShooter(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, Constants.SCREEN_TITLE)
    space_shooter.setup()
    space_shooter.run()
