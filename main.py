import tkinter as tk
import pygame as pg
import zipfile as zip
import json
import io
import os

from api.Game import Game
from api.GameObject import GameObject

class PgApp:
    def __init__(self):
        self.control_panel = TkApp(self)

        #this part lets us run the pygame window in a frame in our tkinter window
        embed_id = self.control_panel.get_game_frame_id()

        os.environ['SDL_WINDOWID'] = str(embed_id)
        os.environ['SDL_VIDEODRIVER'] = 'windib'

        self.control_panel.root.update()
        real_w = self.control_panel.game_frame.winfo_width()
        real_h = self.control_panel.game_frame.winfo_height()

        self.RES = pg.Vector2(640, 360)
        self.FPS = 60

        self.game = Game((1920, 1080), self.RES, "Editor", pg.NOFRAME, self.FPS)

        self.scale_ratio = self.RES.x/real_w

        self.font = pg.font.Font("fonts/FRm6x11.ttf", 16) #this font is a modified version of this one https://managore.itch.io/m6x11, it now handles French accents thanks to me, axel.

        self.cam_offset = pg.Vector2(0, 0)

        self.game.bind(pg.MOUSEMOTION, self.update_camera_pos)
        self.grid = GameObject((0, 0), self.RES)

        self.fps_counter = GameObject((0, 0), (640, 360))

        self.game.run(self.loop)

    def update_camera_pos(self, event: pg.event.Event):
        if pg.mouse.get_pressed()[2]:
            delta = pg.Vector2(event.rel)
            self.cam_offset -= delta * self.scale_ratio

    def loop(self):
        self.control_panel.update()

        self.game.screen.set_layer(0, "grille")
        self.grid.set_surface(self.render_grid())
        self.game.screen.add(self.grid, "grille")

        self.fps_counter.set_surface(self.font.render(f"FPS : {int(self.game.clock.get_fps())}", False, (200, 200, 200, 150)).convert_alpha())
        self.game.screen.add(self.fps_counter)

    def render_grid(self):
        grid = pg.Surface(self.RES, pg.SRCALPHA)

        offset = pg.Vector2(self.cam_offset.x % 32, self.cam_offset.y % 32)

        for i in range(21):
            pg.draw.line(grid, (200, 200, 200, 50), (32 * i, 0) - offset, (32 * i, self.RES.y + 32) - offset, width=1)

        for j in range(13):
            pg.draw.line(grid, (200, 200, 200, 50), (0, 32 * j) - offset, (self.RES.x + 32, 32 * j) - offset, width=1)
        return grid

class TkApp:
    def __init__(self, master):
        self.master = master
        self.root = tk.Tk()
        self.root.title("Galaxaris editor")
        self.root.state('zoomed')

        self.root.protocol("WM_DELETE_WINDOW", self.exit_editor)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_w}x{screen_h}+0+0")

        self.generate_ui()

    def exit_editor(self):
        self.master.game.stop()

    def get_game_frame_id(self):
        self.root.update()
        return self.game_frame.winfo_id()

    def update(self):
        self.root.update()

    def generate_ui(self):
        self.root.grid_columnconfigure(0, weight=1, uniform="col")
        self.root.grid_columnconfigure(1, weight=4, uniform="col")

        self.root.grid_rowconfigure(0, weight=4, uniform="row")
        self.root.grid_rowconfigure(1, weight=12, uniform="row")
        self.root.grid_rowconfigure(2, weight=1, uniform="row")
        self.root.grid_rowconfigure(3, weight=3, uniform="row")

        self.game_frame = tk.Frame(self.root, bg="green")
        self.game_frame.grid(row=0, column=1, rowspan=2, sticky="news")

        self.header_frame = tk.Frame(self.root, bg="red")
        self.header_frame.grid(row=0, column=0, sticky="news")

        self.generate_header_frame_ui()

        self.blocks_frame = tk.Frame(self.root, bg="pink")
        self.blocks_frame.grid(row=1, column=0, rowspan=2, sticky="news")

        self.edit_blocks_frame = tk.Frame(self.root, bg="blue")
        self.edit_blocks_frame.grid(row=1, column=0, rowspan=2, sticky="news")
        self.edit_blocks_frame.tkraise()

        self.actions_frame = tk.Frame(self.root, bg="green")
        self.actions_frame.grid(row=3, column=0, sticky="news")

        self.generate_actions_frame_ui()

        self.assets_frame = tk.Frame(self.root, bg="yellow")
        self.assets_frame.grid(row=2, column=1, rowspan=2, sticky="news")

    def generate_actions_frame_ui(self):
        self.actions_frame.grid_columnconfigure((0,1,2), weight=1)
        self.actions_frame.grid_rowconfigure((0,1), weight=1)

        self.btn_add_block = tk.Button(self.actions_frame, text="Add a block")
        self.btn_add_block.grid(row=0, column=0, sticky="news", padx=5, pady=5)

        self.btn_edit_block = tk.Button(self.actions_frame, text="Edit the block")
        self.btn_edit_block.grid(row=0, column=1, sticky="news", padx=5, pady=5)

        self.btn_save_block = tk.Button(self.actions_frame, text="Save the block")
        self.btn_save_block.grid(row=1, column=1, sticky="news", padx=5, pady=5)

        self.btn_del_block = tk.Button(self.actions_frame, text="Delete the block")
        self.btn_del_block.grid(row=1, column=0, sticky="news", padx=5, pady=5)

        self.btn_add_asset = tk.Button(self.actions_frame, text="Add an asset")
        self.btn_add_asset.grid(row=0, column=2, sticky="news", padx=5, pady=5)

        self.btn_del_asset = tk.Button(self.actions_frame, text="Delete the asset")
        self.btn_del_asset.grid(row=1, column=2, sticky="news", padx=5, pady=5)

    def generate_header_frame_ui(self):
        self.header_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.header_frame.grid_rowconfigure((0,1,2), weight=1)

        self.ntr_level_title = tk.Entry(self.header_frame)
        self.ntr_level_title.grid(row=0, column=0, columnspan=4, sticky="news", padx=5, pady=5)

        self.btn_parallax = tk.Button(self.header_frame, text="Add parallax")
        self.btn_parallax.grid(row=1, column=0, sticky="news", padx=5, pady=5)

        self.btn_music = tk.Button(self.header_frame, text="Add music")
        self.btn_music.grid(row=1, column=1, sticky="news", padx=5, pady=5)

        self.btn_load = tk.Button(self.header_frame, text="Load a level")
        self.btn_load.grid(row=1, column=2, sticky="news", padx=5, pady=5)

        self.btn_save = tk.Button(self.header_frame, text="Save the level")
        self.btn_save.grid(row=1, column=3, sticky="news", padx=5, pady=5)

        self.btn_play = tk.Button(self.header_frame, text="Play level")
        self.btn_play.grid(row=2, column=0, sticky="news", padx=5, pady=5)

        self.btn_pause = tk.Button(self.header_frame, text="Pause level")
        self.btn_pause.grid(row=2, column=1, sticky="news", padx=5, pady=5)

        self.btn_restart = tk.Button(self.header_frame, text="Restart level")
        self.btn_restart.grid(row=2, column=2, sticky="news", padx=5, pady=5)

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