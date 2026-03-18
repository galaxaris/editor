"""
=== Omicronde Project Editor - Galaxaris ===

This is the entry point of the Omicronde Editor. Built using tkinter & the Omicronde API.

Authors: Galaxaris & Associates

v.Beta (in development)
- 06/03/2026

Copyright (c) 2026 Galaxaris & Associates. All rights reserved.

"""

#### RUN THE EDITOR WITH "python -m editor.main" FROM THE ROOT DIRECTORY OF THE PROJECT ####

import os
import tkinter as tk
import threading

from editor.EditorData import ObjectsInfo, LevelInfo

#### CHANGE WORK DIRECTORY TO THE EDITOR FOLDER ####
#=> relative paths for assets loading is managed properly. Can be runned then from anywhere without issue 
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from editor.tk_utils.UIGeneration import generate_ui
from editor.tk_utils.TtkCss import apply_ttk_style
from editor.tk_utils.MenuBarGeneration import generate_mb
from editor.tk_utils.KeyRedirection import generate_key_map, handle_keydown, handle_keyup
from editor.ReadApiGa import get_placeable
from editor.PgApp import PgApp
from editor.tk_utils.ButtonsFunctions import place_object

from EditorData import ObjectsInfo, LevelInfo, ObjectsLayout

from api.utils.ResourcePath import resource_path

class TkApp:
    def __init__(self):
        self.root = tk.Tk()

        self.root.title("Galaxaris editor")
        self.root.state('zoomed')
        self.root.resizable(False, False) #pygame app shouldn't be resized, it is good as it is

        self.menubar = tk.Menu(self.root)
        generate_mb(self)
        self.root.config(menu=self.menubar)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_editor) #the x button that close the tkinter window is redirected to also kill the pg window

        apply_ttk_style()

        self.assets_path = resource_path("assets")
        self.obj_editing = False
        self.key_map = generate_key_map()
        self.placeable_classes = get_placeable("class")
        self.placeable_func = get_placeable("func")

        self.level_info = LevelInfo()
        self.objects_info = ObjectsInfo()
        self.info_colors = []
        self.objects_layout = ObjectsLayout()
        self.selected_object = None

        game_frame_id = generate_ui(self)

        self.pg_app = PgApp(game_frame_id, self, self.assets_path)
        #self.root.bind("<KeyPress>", lambda event: handle_keydown(self, event))
        #self.root.bind("<KeyRelease>", lambda event: handle_keyup(self, event))
        self.root.bind("<F11>", self.maximize)
        self.root.bind("<Control-F11>", self.toggle_fullscreen)
        self.root.bind("<n>", lambda event: place_object(self, event))

        self.game_thread = threading.Thread(target=lambda: self.pg_app.game.run(self.pg_app.loop), daemon=True)
        self.game_thread.start()
        self.root.mainloop()

    def maximize(self, event):
        window = event.widget.winfo_toplevel()

        if window.state() == 'zoomed':
            window.state('normal')
        else:
            window.state('zoomed')

    def toggle_fullscreen(self, event):
        is_fullscreen = event.widget.winfo_toplevel().attributes("-fullscreen")
        event.widget.winfo_toplevel().attributes("-fullscreen", not is_fullscreen)
        return "break"

    def exit_editor(self) -> None:
        self.pg_app.game.stop()
        self.game_thread.join() #just in case I guess
        self.root.destroy()

if __name__ == "__main__":
    app = TkApp()