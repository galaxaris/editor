import tkinter as tk
import pygame as pg
import os

from api.Game import Game

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

        pg.init()
        self.RES = (640, 360)
        WIDTH, HEIGHT = self.RES
        self.FPS = 60
        self.font = pg.font.Font("fonts/FRm6x11.ttf", 16) #this font is a modified version of this one https://managore.itch.io/m6x11, it now handles French accents thanks to me, axel.

        self.game = Game(real_w, real_h, WIDTH, HEIGHT,"Editor", pg.SCALED | pg.NOFRAME, self.FPS)
        self.game.run(self.loop)

    def loop(self, master):
        self.control_panel.update()
        pg.draw.rect(master.screen, (170,130,125), (0, 0, 640, 360), 1)

        fps_count = self.font.render(f"FPS : {int(master.clock.get_fps())}", False, (200,200,200,150)).convert_alpha()
        master.screen.blit(fps_count, (0,0))

class TkApp:
    def __init__(self,master):
        self.master = master
        self.root = tk.Tk()
        self.root.title("Galaxaris editor")
        self.root.state('zoomed')

        self.root.protocol("WM_DELETE_WINDOW", self.exit_editor)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_w}x{screen_h}+0+0")

        self.root.grid_columnconfigure(1, weight=4)
        self.root.grid_columnconfigure(0, weight=1)

        # La ligne 0 prend tout l'espace vertical
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=6)
        self.root.grid_rowconfigure(2, weight=2)

        # 1. Zone Pygame (à gauche, 80% de large)
        self.game_frame = tk.Frame(self.root, bg="green")
        self.game_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.header_frame = tk.Frame(self.root, bg="red")
        self.header_frame.grid(row=0, column=0, sticky="nsew")

        self.blocks_frame = tk.Frame(self.root, bg="blue")
        self.blocks_frame.grid(row=1, column=0, sticky="nsew")

        self.actions_frame = tk.Frame(self.root, bg="green")
        self.actions_frame.grid(row=2, column=0, sticky="nsew")

        self.assets_frame = tk.Frame(self.root, bg="yellow")
        self.assets_frame.grid(row=2, column=1, sticky="nsew")

    def exit_editor(self):
        self.master.game.stop()

    def get_game_frame_id(self):
        self.root.update()
        return self.game_frame.winfo_id()

    def update(self):
        self.root.update()

if __name__ == "__main__":
    app = PgApp()