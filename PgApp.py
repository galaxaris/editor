import pygame as pg
import zipfile as zip
import json
import io
import os
from os.path import join
import threading

from api.utils import Debug, Fonts

from api.Game import Game
from api.environment.Parallax import ParallaxBackground, ParallaxLayer
from api.assets.Texture import Texture
from api.assets.Resource import Resource, ResourceType
from api.utils.Inputs import get_inputs, get_once_inputs


class PgApp:
    def __init__(self, embed_id, master, assets_path):
        #this part lets us run the pygame window in a frame in our tkinter window
        os.environ['SDL_WINDOWID'] = str(embed_id)
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ["EDITOR"] = "1" #and this let us redirect inputs from tkinter to the api

        self.RES = pg.Vector2(640, 360)
        self.FPS = 60
        self.master = master
        self.assets_path = assets_path

        self.font_G = "**/" + join(self.assets_path, "Fonts\\Gm6x11.ttf")
        Fonts.DEFAULT_FONT = self.font_G
        Debug.debug_font = self.font_G
        self.game = Game((1920, 1080), self.RES, "Editor", pg.NOFRAME, self.FPS)

        self.setup_api()
        self.previous_click_mouse = pg.Vector2(0, 0)

    def loop(self):
        for obj in self.master.objects_layout.obj_list:
            self.game.scene.add(obj.solid, "#editor")

    def setup_api(self):
        glob = Resource(ResourceType.GLOBAL, self.assets_path)
        Debug.toggle("freecam")
        self.game.enable_debug()
        grid = Texture("grid.png", glob) #draw the grid via a parallax layer :)
        p_bg = ParallaxBackground(self.RES, [ParallaxLayer(pg.Vector2(1, 1), grid)], (0, 0, 0))
        self.game.scene.set_background(p_bg)
        self.game.scene.set_layer(0, "#editor")

