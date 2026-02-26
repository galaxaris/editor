import tkinter as tk
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

        self.obj_editing = False
        self.placeable_classes = get_placeable_classes()

        generate_ui(self)

    def exit_editor(self):
        self.master.game.stop()

    def get_game_frame_id(self):
        self.root.update()
        return self.game_frame.winfo_id()

    def update(self):
        self.root.update()

