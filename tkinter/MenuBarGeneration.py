import tkinter as tk
from editor.tkinter.ButtonsFunctions import add_a_music

def generate_mb(self):
    file_menu = tk.Menu(self.menubar, tearoff=0)
    file_menu.add_command(label="Open a level", command=lambda: print("o"))
    file_menu.add_command(label="New level", command=lambda: print("n"))
    file_menu.add_command(label="Save level", command=lambda: print("s"))

    self.menubar.add_cascade(label="Files", menu=file_menu)

    env_menu = tk.Menu(self.menubar, tearoff=0)
    env_menu.add_command(label="Add a parallax layer", command=lambda: print("p"))
    env_menu.add_command(label="Remove a parallax layer", command=lambda: print("r"))

    env_menu.add_separator()

    env_menu.add_command(label="Choose a music", command=lambda: add_a_music(self))

    self.menubar.add_cascade(label="Environment", menu=env_menu)
