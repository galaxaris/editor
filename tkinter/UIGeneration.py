import tkinter as tk

def generate_ui(self):
    self.root.grid_columnconfigure(0, weight=1, uniform="col")
    self.root.grid_columnconfigure(1, weight=4, uniform="col")

    self.root.grid_rowconfigure(0, weight=4, uniform="row")
    self.root.grid_rowconfigure(1, weight=12, uniform="row")
    self.root.grid_rowconfigure(2, weight=1, uniform="row")
    self.root.grid_rowconfigure(3, weight=3, uniform="row")

    self.game_frame = tk.Frame(self.root, bg="green")
    self.game_frame.grid(row=0, column=1, rowspan=2, sticky="news")

    self.header_frame = tk.Frame(self.root, bg="red")
    self.header_frame.grid(row=0, column=0, sticky="news")

    generate_header_frame_ui(self)

    self.blocks_frame = tk.Frame(self.root, bg="pink")
    self.blocks_frame.grid(row=1, column=0, rowspan=2, sticky="news")

    self.edit_blocks_frame = tk.Frame(self.root, bg="blue")
    self.edit_blocks_frame.grid(row=1, column=0, rowspan=2, sticky="news")
    self.edit_blocks_frame.tkraise()

    self.actions_frame = tk.Frame(self.root, bg="green")
    self.actions_frame.grid(row=3, column=0, sticky="news")

    generate_actions_frame_ui(self)

    self.assets_frame = tk.Frame(self.root, bg="yellow")
    self.assets_frame.grid(row=2, column=1, rowspan=2, sticky="news")


def generate_actions_frame_ui(self):
    self.actions_frame.grid_columnconfigure((0, 1, 2), weight=1)
    self.actions_frame.grid_rowconfigure((0, 1), weight=1)

    self.btn_add_block = tk.Button(self.actions_frame, text="Add an object")
    self.btn_add_block.grid(row=0, column=0, sticky="news", padx=5, pady=5)

    self.btn_edit_block = tk.Button(self.actions_frame, text="Edit the object")
    self.btn_edit_block.grid(row=0, column=1, sticky="news", padx=(5,10), pady=5)

    self.btn_save_block = tk.Button(self.actions_frame, text="Save the object")
    self.btn_save_block.grid(row=1, column=1, sticky="news", padx=(5,10), pady=5)

    self.btn_del_block = tk.Button(self.actions_frame, text="Delete the object")
    self.btn_del_block.grid(row=1, column=0, sticky="news", padx=5, pady=5)

    self.btn_add_asset = tk.Button(self.actions_frame, text="Add an asset")
    self.btn_add_asset.grid(row=0, column=2, sticky="news", padx=(10,5), pady=5)

    self.btn_del_asset = tk.Button(self.actions_frame, text="Delete the asset")
    self.btn_del_asset.grid(row=1, column=2, sticky="news", padx=(10,5), pady=5)


def generate_header_frame_ui(self):
    self.header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    self.header_frame.grid_rowconfigure((0, 1, 2), weight=1)

    self.ntr_level_title = tk.Entry(self.header_frame)
    self.ntr_level_title.grid(row=0, column=0, columnspan=4, sticky="news", padx=5, pady=5)

    self.btn_parallax = tk.Button(self.header_frame, text="Add parallax")
    self.btn_parallax.grid(row=1, column=0, sticky="news", padx=5, pady=5)

    self.btn_music = tk.Button(self.header_frame, text="Add music")
    self.btn_music.grid(row=1, column=1, sticky="news", padx=5, pady=5)

    self.btn_load = tk.Button(self.header_frame, text="Load a level")
    self.btn_load.grid(row=1, column=2, sticky="news", padx=5, pady=5)

    self.btn_save = tk.Button(self.header_frame, text="Save the level")
    self.btn_save.grid(row=1, column=3, sticky="news", padx=5, pady=5)

    self.btn_play = tk.Button(self.header_frame, text="Play level")
    self.btn_play.grid(row=2, column=0, sticky="news", padx=5, pady=5)

    self.btn_pause = tk.Button(self.header_frame, text="Pause level")
    self.btn_pause.grid(row=2, column=1, sticky="news", padx=5, pady=5)

    self.btn_restart = tk.Button(self.header_frame, text="Restart level")
    self.btn_restart.grid(row=2, column=2, sticky="news", padx=5, pady=5)