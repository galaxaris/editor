import tkinter as tk
from editor.tkinter.UIGeneration import generate_ui
from editor.tkinter.TtkCss import apply_ttk_style

class TkApp:
    def __init__(self, master):
        self.master = master
        self.root = tk.Tk()
        self.root.title("Galaxaris editor")
        self.root.state('zoomed')
        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_editor)

        screen_w = self.root.winfo_screenwidth()

        apply_ttk_style()

        self.obj_editing = False
        generate_ui(self)

    def exit_editor(self):
        self.master.game.stop()

    def get_game_frame_id(self):
        self.root.update()
        return self.game_frame.winfo_id()

    def update(self):
        self.root.update()

