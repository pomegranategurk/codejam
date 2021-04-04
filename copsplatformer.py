from types import prepare_class
import arcade
import random
import time
import os
#TODO IDEA: Platformer | You are criminal being pursued by cop | Must go fast as to not get caught | Endless | Increasing speed

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Cop Platformer"

class Helicopter(arcade.Sprite):
    """
    *Class for helicopter sprite
    """
    def __init__(self):
        super().__init__()

        self.scale = 3
        self.textures = []

        texture = arcade.load_texture(f"{os.getcwd()}/helicopter.png")
        self.textures.append(texture)
        texture = arcade.load_texture(f"{os.getcwd()}/helicopter.png", flipped_horizontally=True)
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def flip(self):
        if flip_right == True:
            self.texture = self.textures[1]
        else:
            self.texture = self.textures[0]
#! -=-=-=-=-=-=-=--==-=-=-=-=-=-=-=-==-=-==-=-=-==--=-=-=====-=-=-==
class StartView(arcade.View):
    """
    *Start screen
    """
    def __init__(self):
        super().__init__()

    def setup(self):
        pass

    def on_draw(self):
        window.clear()
        arcade.set_background_color(arcade.csscolor.BISQUE)

        arcade.draw_text("Click to play!", 250, 500, arcade.color.AMARANTH_PURPLE, 45)

    def update(self, delta_time: float):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        try:
	        game_view = GameView()
	        window.show_view(game_view)
	        game_view.setup()
        finally:
            input("a")
#! -=-=-=-=-=-=-=--==-=-=-=-=-=-=-=-==-=-==-=-=-==--=-=-=====-=-=-==

class GameView(arcade.View):
    """
    *Game screen. Responsible for almost everything
    """
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.csscolor.LIGHT_GREY)

    def setup(self):
        self.player = arcade.Sprite(f"{os.getcwd()}/criminal.png", 3)
        self.player.center_x = 400;self.player.center_y = 1200

        self.heli = Helicopter()
        self.heli.center_x = 400;self.heli.center_y = 150

        self.falling_speed = -3
        self.tile_list = arcade.SpriteList()
        for x in range(300, 556, 50):
            self.mid_tile = arcade.Sprite(":resources:images/tiles/planet.png", 0.5)
            self.mid_tile.center_x = x;self.mid_tile.center_y = 1200
            self.tile_list.append(self.mid_tile)

        self.grav_veloc = 0.7
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.tile_list, self.grav_veloc)  

        self.a_pressed = None
        self.d_pressed = None
        self.space_pressed = None

        self.seconds = 0
        self.total_time = 0
        self.past_time = 0

        self.bar_list = arcade.SpriteList()
        self.game_over = False

        self.coin_list = arcade.SpriteList()
        self.coin_count = 0
        
        self.music = arcade.Sound(":resources:music/funkyrobot.mp3", streaming=True)
        self.music_player = self.music.play(0.07)

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.tile_list.draw() 
        
        minutes = int(self.total_time) // 60
        self.seconds = int(self.total_time) % 60
        output = f"Time: {minutes:02d}:{self.seconds:02d}"
        arcade.draw_text(output, 60, 900, arcade.color.BOTTLE_GREEN, 45)

        arcade.draw_text(f"Score: {self.coin_count}", 500, 900, arcade.color.BOTTLE_GREEN, 45)

        if self.player.center_y <= 100:
            self.game_over = True
            for x in range(0, 800, 125):
                self.jail_bar = arcade.Sprite(":resources:images/tiles/planetCenter_rounded.png", 1)
                self.jail_bar.width = 50
                self.jail_bar.height = 800
                self.jail_bar.center_x = x
                self.jail_bar.center_y = 1400
                self.bar_list.append(self.jail_bar)
            self.bar_list.draw()
            time.sleep(0.1)
            for x in range(20):
                for bar in self.bar_list:
                    bar.center_y -= 2
            jail_text = f"You evaded the cops for {minutes:02d}:{self.seconds:02d}!"
            arcade.draw_text(jail_text, 50, 600, arcade.color.DARK_BYZANTIUM, 45)
            arcade.draw_text("Press R to restart", 50, 500, arcade.color.ALIZARIN_CRIMSON, 40)

        self.heli.draw()
        self.coin_list.draw()

    def update(self, delta_time: float):
        global flip_right
        super().update(delta_time)
        if self.game_over == False:
            self.physics_engine.update()

            if self.a_pressed:
                self.player.center_x -= 5
                flip_right = False
            if self.d_pressed:
                self.player.center_x += 5
                flip_right = True
            if self.space_pressed and self.physics_engine.can_jump():
                self.player.change_y = 16

            for self.tile in self.tile_list:
                self.tile.change_y = self.falling_speed

            self.total_time += delta_time

            if len(self.tile_list) < 100:
                if self.total_time-2 >= self.past_time:
                    self.past_time = self.total_time
                    for x in range(1, 3):
                        if x == 1:
                            #*Render left side
                            self.temp_x = random.randint(0, 400)
                            self.mid_tile = arcade.Sprite(":resources:images/tiles/planet.png", 0.5)
                            self.mid_tile.center_x = self.temp_x;self.mid_tile.center_y = 1000
                            self.tile_list.append(self.mid_tile)
                            if random.randint(1, 4) == 2:
                                self.coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
                                self.coin.center_x = self.mid_tile.center_x 
                                self.coin.center_y = self.mid_tile.center_y + 65
                                self.coin_list.append(self.coin)
                        self.mid_tile = arcade.Sprite(":resources:images/tiles/planet.png", 0.5)
                        self.mid_tile.center_x = self.temp_x+50;self.mid_tile.center_y = 1000
                        self.tile_list.append(self.mid_tile)

                        if x == 1:
                            #*Render right side
                            self.temp_x = random.randint(400, 800)
                            self.mid_tile = arcade.Sprite(":resources:images/tiles/planet.png", 0.5)
                            self.mid_tile.center_x = self.temp_x;self.mid_tile.center_y = 1000
                            self.tile_list.append(self.mid_tile)
                            if random.randint(1, 4) == 2:
                                self.coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
                                self.coin.center_x = self.mid_tile.center_x
                                self.coin.center_y = self.mid_tile.center_y + 65
                                self.coin_list.append(self.coin)
                        self.mid_tile = arcade.Sprite(":resources:images/tiles/planet.png", 0.5)
                        self.mid_tile.center_x = self.temp_x+50;self.mid_tile.center_y = 1000
                        self.tile_list.append(self.mid_tile)
            
            for self.tile in self.tile_list:
                if self.tile.center_y <= 0:
                    self.tile_list.remove(self.tile)
                    print("tile removed") 

            self.heli.center_x = self.player.center_x + random.random()
            self.heli.flip()
            self.heli.update()

            for coin in self.coin_list:
                coin.center_y += self.falling_speed
                if coin.center_y <= 0:
                    self.coin_list.remove(coin)
                if arcade.check_for_collision(coin, self.player):
                    self.coin_count += 1
                    self.coin_list.remove(coin)
                    self.falling_speed -= 0.3

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == 97: #* a
            self.a_pressed = True
        if symbol == 100: #* d
            self.d_pressed = True
        if symbol == 32: #* space
            self.space_pressed = True
        if symbol == 114:
            if self.game_over == True:
                self.music.stop()
                start_view = StartView()
                window.show_view(start_view)
                start_view.setup()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == 97: #* a
            self.a_pressed = False
        if symbol == 100: #* d
            self.d_pressed = False
        if symbol == 32: #* space
            self.space_pressed = False

def main():
    global window, flip_right, music_played
    music_played = False
    flip_right = False 
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()