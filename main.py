import tkinter as tk
import threading

from editor.tk_utils.UIGeneration import generate_ui
from editor.tk_utils.TtkCss import apply_ttk_style
from editor.tk_utils.MenuBarGeneration import generate_mb
from editor.tk_utils.KeyRedirection import generate_key_map, handle_keydown, handle_keyup
from editor.ReadApiGa import get_placeable
from editor.PgApp import PgApp

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

        self.obj_editing = False
        self.key_map = generate_key_map()
        self.placeable_classes = get_placeable("class")
        self.placeable_func = get_placeable("func")
        print(self.placeable_classes)
        print(self.placeable_func)

        game_frame_id = generate_ui(self)

        self.pg_app = PgApp(game_frame_id)
        #self.root.bind("<KeyPress>", lambda event: handle_keydown(self, event))
        #self.root.bind("<KeyRelease>", lambda event: handle_keyup(self, event))

        self.game_thread = threading.Thread(target=lambda: self.pg_app.game.run(self.pg_app.loop), daemon=True)
        self.game_thread.start()
        self.root.mainloop()

    def exit_editor(self) -> None:
        self.pg_app.game.stop()
        self.game_thread.join() #just in case I guess
        self.root.destroy()

if __name__ == "__main__":
    app = TkApp()