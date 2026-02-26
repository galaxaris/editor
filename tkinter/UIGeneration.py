import tkinter as tk
from tkinter import ttk

from editor.tkinter.ButtonsFunctions import *

def generate_ui(self):
    self.root.grid_columnconfigure(0, weight=1, uniform="col")
    self.root.grid_columnconfigure(1, weight=4, uniform="col")

    game_frame_w = 0.8*self.root.winfo_screenwidth()

    self.root.grid_rowconfigure(0, minsize=game_frame_w*9/16*3/16, weight=0)
    self.root.grid_rowconfigure(1, minsize=game_frame_w*9/16*13/16, weight=0)
    self.root.grid_rowconfigure(2, weight=1)
    self.root.grid_rowconfigure(3, weight=3)

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
    canvas = tk.Canvas(self.edit_object_frame, highlightthickness=0, background="black")
    canvas.grid(row=3, column=0, columnspan=2, sticky="news", padx=(2, 0))

    self.scrollbar = ttk.Scrollbar(self.edit_object_frame, orient="vertical", command=canvas.yview)
    self.scrollbar.grid(row=3, column=2, sticky="ns")

    self.sclbox_object_att = ttk.Frame(canvas, style = "Noborder.TFrame")

    canvas_window = canvas.create_window((0, 0), window=self.sclbox_object_att, anchor="nw")

    canvas.configure(yscrollcommand=self.scrollbar.set)

    self.sclbox_object_att.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))

    canvas.bind("<Enter>", lambda _: canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")))
    canvas.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))

def generate_edit_object_frame(self):
    self.edit_object_frame.grid_columnconfigure((0, 1), weight=1)
    self.edit_object_frame.grid_columnconfigure(2, weight=0)

    self.edit_object_frame.grid_rowconfigure((0, 1, 2), weight=0)
    self.edit_object_frame.grid_rowconfigure(3, weight=1)

    create_scrollbox(self)

    check_var = tk.BooleanVar(value=False)
    self.chk_global = ttk.Checkbutton(self.edit_object_frame,text="Is it Global ?",variable=check_var)
    self.chk_global.grid(row=0, column=0, columnspan=2, sticky="news", padx=(10, 5), pady=5)

    self.btn_discard = ttk.Button(self.edit_object_frame, text="Discard changes", command=lambda : exit_edit(self))
    self.btn_discard.grid(row=0, column=1, columnspan=2, sticky="news", padx=(5, 10), pady=5)

    self.lbl_object_class = ttk.Label(self.edit_object_frame, text="Object class")
    self.lbl_object_class.grid(row=1, column=0, sticky="news", padx=(10,5), pady=5)

    self.lbl_object_name = ttk.Label(self.edit_object_frame, text="Object name")
    self.lbl_object_name.grid(row=1, column=1, sticky="news", padx=(5,10), pady=5)

    self.cbb_object_class = ttk.Combobox(self.edit_object_frame, values=list(self.placeable_classes.keys()), state="readonly")
    self.cbb_object_class.grid(row=2, column=0, sticky="news", padx=(10, 5), pady=5)
    self.cbb_object_class.current(0)

    self.root.update()
    generate_build_params(self, self.cbb_object_class.get())
    self.cbb_object_class.bind("<<ComboboxSelected>>", lambda event: generate_build_params(self, event.widget.get()))

    self.ntr_object_name = ttk.Entry(self.edit_object_frame)
    self.ntr_object_name.grid(row=2, column=1, sticky="news", padx=(5, 0), pady=5)

def generate_actions_frame_ui(self):
    self.actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
    self.actions_frame.grid_rowconfigure((0, 1), weight=1)

    self.btn_add_object = ttk.Button(self.actions_frame, text="Add an\nobject", command=lambda : new_object(self))
    self.btn_add_object.grid(row=0, column=0, sticky="news", padx=(10,5), pady=(10,5))

    self.btn_edit_object = ttk.Button(self.actions_frame, text="Edit the\nobject", command=lambda : edit_object(self))
    self.btn_edit_object.grid(row=0, column=1, sticky="news", padx=(5, 10), pady=(10,5))

    self.btn_save_object = ttk.Button(self.actions_frame, text="Save the\nobject", command=lambda : save_object(self))
    self.btn_save_object.grid(row=1, column=1, sticky="news", padx=(5, 10), pady=(5,10))

    self.btn_del_object = ttk.Button(self.actions_frame, text="Delete the\nobject")
    self.btn_del_object.grid(row=1, column=0, sticky="news", padx=(10,5), pady=(5,10))

    self.btn_add_asset = ttk.Button(self.actions_frame, text="Add an\nasset")
    self.btn_add_asset.grid(row=0, column=2, sticky="news", padx=10, pady=(10,5))

    self.btn_del_asset = ttk.Button(self.actions_frame, text="Delete the\nasset")
    self.btn_del_asset.grid(row=1, column=2, sticky="news", padx=10, pady=(5,10))


def generate_header_frame_ui(self):
    self.header_frame.grid_columnconfigure((0, 1, 2), weight=1)

    self.header_frame.grid_rowconfigure(0, weight=0)

    self.header_frame.grid_rowconfigure(1, weight=1)

    self.ntr_level_title = ttk.Entry(self.header_frame)
    self.ntr_level_title.grid(row=0, column=0, columnspan=4, sticky="news", padx=10, pady=(10, 5))

    self.play_icon = tk.PhotoImage(file="assets\\icons\\play.png")
    self.btn_play = ttk.Button(self.header_frame, image=self.play_icon, style="Image.TButton")
    self.btn_play.grid(row=1, column=0, sticky="news", padx=(10, 5), pady=(5, 10))

    self.pause_icon = tk.PhotoImage(file="assets\\icons\\pause.png")
    self.btn_pause = ttk.Button(self.header_frame, image=self.pause_icon, style="Image.TButton")
    self.btn_pause.grid(row=1, column=1, sticky="news", padx=5, pady=(5, 10))

    self.replay_icon = tk.PhotoImage(file="assets\\icons\\replay.png")
    self.btn_restart = ttk.Button(self.header_frame, image=self.replay_icon, style="Image.TButton")
    self.btn_restart.grid(row=1, column=2, sticky="news", padx=5, pady=(5, 10))