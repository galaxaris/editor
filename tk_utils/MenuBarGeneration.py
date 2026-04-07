import tkinter as tk
from editor.tk_utils.ButtonsFunctions import add_a_music, add_a_script

def generate_mb(self):
    file_menu = tk.Menu(self.menubar, tearoff=0)
    file_menu.add_command(label="New level", command=lambda: print("n"))
    file_menu.add_command(label="Open a level", command=lambda: print("o"))
    file_menu.add_command(label="Save level", command=lambda: print("s"))

    self.menubar.add_cascade(label="Files", menu=file_menu)

    self.env_menu = tk.Menu(self.menubar, tearoff=0)
    self.env_menu.add_command(label="Add a parallax layer", command=lambda: print("p"))
    self.env_menu.add_command(label="Remove a parallax layer", command=lambda: print("r"))

    self.env_menu.add_separator()

    self.env_menu.add_command(label="Add an sfx", command=lambda: print("p"))
    self.env_menu.add_command(label="Remove an sfx", command=lambda: print("r"))

    self.env_menu.add_separator()

    self.env_menu.add_command(label="Choose a music", command=lambda: add_a_music(self))

    self.env_menu.add_separator()

    self.env_menu.add_command(label="Choose a script (.py)", command=lambda: add_a_script(self))

    self.menubar.add_cascade(label="Environment", menu=self.env_menu)
