import pygame as pg
import zipfile as zip
import json
import io
import os

from editor.tkinter.TkApp import TkApp

from api.Game import Game
from api.GameObject import GameObject
from api.entity.Player import Player
from api.environment.Parallax import ParallaxBackground, ParallaxLayer
from api.assets.Texture import Texture
from api.assets.Resource import Resource, ResourceType

class PgApp:
    def __init__(self):
        self.control_panel = TkApp(self)

        #this part lets us run the pygame window in a frame in our tkinter window
        embed_id = self.control_panel.get_game_frame_id()

        os.environ['SDL_WINDOWID'] = str(embed_id)
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ["EDITOR"] = "1"


        self.RES = pg.Vector2(640, 360)
        self.FPS = 60

        self.game = Game((1920, 1080), self.RES, "Editor", pg.NOFRAME, self.FPS)

        self.setup_api()

        self.game.run(self.loop)

    def setup_api(self):
        glob = Resource(ResourceType.GLOBAL, "assets")

        grid = Texture("grid.png", glob) #draw the grid via a parallax layer :)
        self.p_bg = ParallaxBackground(self.RES, [ParallaxLayer(pg.Vector2(1, 1), grid)], (0, 0, 0))

    def loop(self):
        self.control_panel.update()

        self.game.scene.set_background(self.p_bg)

class Data:
    def __init__(self):
        self.music = ""
        self.title = ""
        self.parallax = []
        self.images = []

    def load_data(self, lvl_path: str, global_path: str="game/global/"):
        with zip.ZipFile(lvl_path, 'r') as lvl:

            with lvl.open('header.json') as header:
                lvl_data = json.load(header)

            for f_name in lvl.namelist():
                if f_name.endswith(('.png','.jpg')):

                    img_data = lvl.read(f_name)
                    img_stream = io.BytesIO(img_data)
                    self.images.append(pg.image.load(img_stream).convert_alpha())

        #temporary way as we haven't set a global yet
        if global_path != "game/global/":
            for file in os.listdir(global_path):

                if file.endswith('.json'):
                    with open(os.path.join(global_path, file), 'r') as g_header:
                        global_data = json.load(g_header)

                elif file.endswith(('.png','.jpg')):

                    self.images.append(pg.image.load(os.path.join(global_path, file)).convert_alpha())


if __name__ == "__main__":
    app = PgApp()