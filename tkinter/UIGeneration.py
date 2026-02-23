import tkinter as tk
from tkinter import ttk

from editor.tkinter.ButtonsFunctions import *

def generate_ui(self):
    self.root.grid_columnconfigure(0, weight=1, uniform="col")
    self.root.grid_columnconfigure(1, weight=4, uniform="col")

    self.root.grid_rowconfigure(0, weight=4, uniform="row")
    self.root.grid_rowconfigure(1, weight=12, uniform="row")
    self.root.grid_rowconfigure(2, weight=1, uniform="row")
    self.root.grid_rowconfigure(3, weight=3, uniform="row")

    self.game_frame = ttk.Frame(self.root)
    self.game_frame.grid(row=0, column=1, rowspan=2, sticky="news")

    self.header_frame = ttk.Frame(self.root)
    self.header_frame.grid(row=0, column=0, sticky="news")

    generate_header_frame_ui(self)

    self.object_frame = ttk.Frame(self.root)
    self.object_frame.grid(row=1, column=0, rowspan=2, sticky="news")

    self.edit_object_frame = ttk.Frame(self.root)
    self.edit_object_frame.grid(row=1, column=0, rowspan=2, sticky="news")
    generate_edit_object_frame(self)

    self.object_frame.tkraise()

    self.actions_frame = ttk.Frame(self.root)
    self.actions_frame.grid(row=3, column=0, sticky="news")

    generate_actions_frame_ui(self)

    self.assets_frame = ttk.Frame(self.root)
    self.assets_frame.grid(row=2, column=1, rowspan=2, sticky="news")

def create_scrollbox(self):
    canvas = tk.Canvas(self.edit_object_frame, highlightthickness=0)
    canvas.grid(row=2, column=0, columnspan=2, sticky="news")

    self.scrollbar = ttk.Scrollbar(self.edit_object_frame, orient="vertical", command=canvas.yview)
    self.scrollbar.grid(row=2, column=2, sticky="ns")

    self.sclbox_object_att = ttk.Frame(canvas)

    canvas_window = canvas.create_window((0, 0), window=self.sclbox_object_att, anchor="nw")

    canvas.configure(yscrollcommand=self.scrollbar.set)

    self.sclbox_object_att.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))

    canvas.bind("<Enter>", lambda _: canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")))
    canvas.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))

def generate_edit_object_frame(self):
    self.edit_object_frame.grid_columnconfigure(0, weight=1)
    self.edit_object_frame.grid_columnconfigure(1, weight=1)
    self.edit_object_frame.grid_columnconfigure(2, weight=0)

    self.edit_object_frame.grid_rowconfigure(0, weight=1)
    self.edit_object_frame.grid_rowconfigure(1, weight=1)
    self.edit_object_frame.grid_rowconfigure(2, weight=18)

    self.cbb_object_class = ttk.Combobox(self.edit_object_frame, values=("raphix","lisa","lazare","gautier","axel"))
    self.cbb_object_class.grid(row=0, column=0, sticky="news", padx=5, pady=5)
    self.cbb_object_class.current(0)

    self.btn_discard = ttk.Button(self.edit_object_frame, text="Discard")
    self.btn_discard.grid(row=0, column=1, sticky="news", padx=5, pady=5)

    check_var = tk.BooleanVar(value=False)
    self.chk_global = ttk.Checkbutton(self.edit_object_frame,text="Global ?",variable=check_var)
    self.chk_global.grid(row=1, column=0, columnspan=2, sticky="news", padx=5, pady=5)

    self.ntr_object_name = ttk.Entry(self.edit_object_frame)
    self.ntr_object_name.grid(row=1, column=1, columnspan=2, sticky="news", padx=5, pady=5)

    create_scrollbox(self)

    for i in range(30):
        ttk.Label(self.sclbox_object_att, text=f"Attribut {i}", padding=10).pack(fill="x", padx = 5, pady = 5)

def generate_actions_frame_ui(self):
    self.actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
    self.actions_frame.grid_rowconfigure((0, 1), weight=1)

    self.btn_add_object = ttk.Button(self.actions_frame, text="Add an object")
    self.btn_add_object.grid(row=0, column=0, sticky="news", padx=5, pady=5)
    self.btn_add_object.bind("<Button-1>", lambda event: new_object(self, event))

    self.btn_edit_object = ttk.Button(self.actions_frame, text="Edit the object")
    self.btn_edit_object.grid(row=0, column=1, sticky="news", padx=(5, 10), pady=5)
    self.btn_edit_object.bind("<Button-1>", lambda event: edit_object(self, event))

    self.btn_save_object = ttk.Button(self.actions_frame, text="Save the object")
    self.btn_save_object.grid(row=1, column=1, sticky="news", padx=(5, 10), pady=5)
    self.btn_save_object.bind("<Button-1>", lambda event: save_object(self, event))

    self.btn_del_object = ttk.Button(self.actions_frame, text="Delete the object")
    self.btn_del_object.grid(row=1, column=0, sticky="news", padx=5, pady=5)

    self.btn_add_asset = ttk.Button(self.actions_frame, text="Add an asset")
    self.btn_add_asset.grid(row=0, column=2, sticky="news", padx=(10,5), pady=5)

    self.btn_del_asset = ttk.Button(self.actions_frame, text="Delete the asset")
    self.btn_del_asset.grid(row=1, column=2, sticky="news", padx=(10,5), pady=5)


def generate_header_frame_ui(self):
    self.header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    self.header_frame.grid_rowconfigure((0, 1, 2), weight=1)

    self.ntr_level_title = ttk.Entry(self.header_frame)
    self.ntr_level_title.grid(row=0, column=0, columnspan=4, sticky="news", padx=5, pady=5)

    self.btn_parallax = ttk.Button(self.header_frame, text="Add parallax")
    self.btn_parallax.grid(row=1, column=0, sticky="news", padx=5, pady=5)

    self.btn_music = ttk.Button(self.header_frame, text="Add music")
    self.btn_music.grid(row=1, column=1, sticky="news", padx=5, pady=5)

    self.btn_load = ttk.Button(self.header_frame, text="Load a level")
    self.btn_load.grid(row=1, column=2, sticky="news", padx=5, pady=5)

    self.btn_save = ttk.Button(self.header_frame, text="Save the level")
    self.btn_save.grid(row=1, column=3, sticky="news", padx=5, pady=5)

    self.btn_play = ttk.Button(self.header_frame, text="Play level")
    self.btn_play.grid(row=2, column=0, sticky="news", padx=5, pady=5)

    self.btn_pause = ttk.Button(self.header_frame, text="Pause level")
    self.btn_pause.grid(row=2, column=1, sticky="news", padx=5, pady=5)

    self.btn_restart = ttk.Button(self.header_frame, text="Restart level")
    self.btn_restart.grid(row=2, column=2, sticky="news", padx=5, pady=5)