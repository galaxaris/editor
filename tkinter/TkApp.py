import tkinter as tk
import pygame as pg

from api.utils import Inputs
from editor.tkinter.UIGeneration import generate_ui
from editor.tkinter.TtkCss import apply_ttk_style
from editor.tkinter.MenuBarGeneration import generate_mb
from editor.ReadApi import get_placeable_classes



class TkApp:
    def __init__(self, master):
        self.master = master
        self.root = tk.Tk()

        self.root.title("Galaxaris editor")
        self.root.state('zoomed')
        self.root.resizable(False, False) #very important to avoid crash from the pygame app that is embedded

        self.menubar = tk.Menu(self.root)
        generate_mb(self)
        self.root.config(menu=self.menubar)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_editor) #the x button that close the tkinter window is redirected to kill the pg window

        apply_ttk_style()

        self.root.bind("<KeyPress>", self.handle_keydown)
        self.root.bind("<KeyRelease>", self.handle_keyup)

        self.obj_editing = False
        self.key_map = self.generate_key_map()
        self.placeable_classes = get_placeable_classes()

        generate_ui(self)
        self.game_frame.bind("<Enter>", lambda e: self.game_frame.focus_set()) #if the mouse is over the game frame, we give the game_frame the focus
        self.game_frame.bind("<Leave>", lambda e: self.release_keys())

    def generate_key_map(self):
        mapping = {
            "Escape": pg.K_ESCAPE,
            "Return": pg.K_RETURN,
            "space": pg.K_SPACE,
            "Up": pg.K_UP,
            "Down": pg.K_DOWN,
            "Left": pg.K_LEFT,
            "Right": pg.K_RIGHT,
            "BackSpace": pg.K_BACKSPACE,
            "Delete": pg.K_DELETE,
            "Tab": pg.K_TAB,
            "Shift_L": pg.K_LSHIFT
        }

        for i in range(1, 13):
            mapping[f"F{i}"] = getattr(pg, f"K_F{i}")

        for i in range(10):
            mapping[str(i)] = getattr(pg, f"K_{i}")

        for i in range(26):
            char = chr(i + 97)
            char_upper = chr(i + 65)
            mapping[char] = getattr(pg, f"K_{char}")
            mapping[char_upper] = getattr(pg, f"K_{char}")

        return mapping

    def handle_keydown(self, event):
        pg_key = self.key_map.get(event.keysym)
        if pg_key:
            pg.event.post(pg.event.Event(pg.KEYDOWN, {'key': pg_key}))
            Inputs.editor_edit_key(pg_key, True)

    def handle_keyup(self, event):
        pg_key = self.key_map.get(event.keysym)
        if pg_key:
            pg.event.post(pg.event.Event(pg.KEYUP, {'key': pg_key}))
            Inputs.editor_edit_key(pg_key, False)

    def exit_editor(self) -> None:
        self.master.game.stop()

    def get_game_frame_id(self) -> None:
        self.root.update()
        return self.game_frame.winfo_id()

    def update(self) -> None:
        self.root.update()

    def release_keys(self):
        Inputs.editor_release_key()

