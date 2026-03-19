import tkinter as tk
from os.path import join

from editor.tk_utils.ButtonsFunctions import *
from editor.tk_utils.KeyRedirection import bind_keys, unbind_keys

def generate_ui(self) -> int:
    self.root.grid_columnconfigure(0, weight=1, uniform="col")
    self.root.grid_columnconfigure(1, weight=4, uniform="col")

    game_frame_w = 0.8*self.root.winfo_screenwidth()

    self.root.grid_rowconfigure(0, minsize=game_frame_w*9/16*3/16, weight=0)
    self.root.grid_rowconfigure(1, minsize=game_frame_w*9/16*13/16, weight=0)
    self.root.grid_rowconfigure(2, weight=4)

    self.game_frame = ttk.Frame(self.root)
    self.game_frame.grid(row=0, column=1, rowspan=2, sticky="news")
    self.game_frame.bind("<Enter>", lambda event: bind_keys(self, event))
    self.game_frame.bind("<Leave>", lambda event: unbind_keys(self, event))

    self.header_frame = ttk.Frame(self.root)
    self.header_frame.grid(row=0, column=0, sticky="news")

    generate_header_frame_ui(self)

    self.object_frame = ttk.Frame(self.root)
    self.object_frame.grid(row=1, column=0, sticky="news")

    generate_object_frame(self)

    self.edit_object_frame = ttk.Frame(self.root)
    self.edit_object_frame.grid(row=1, column=0, sticky="news")
    generate_edit_object_frame(self)

    self.object_frame.tkraise()

    self.placement_frame = ttk.Frame(self.root)
    self.placement_frame.grid(row=2, column=0, sticky="news")

    generate_placement_frame_ui(self)

    self.assets_frame = ttk.Frame(self.root)
    self.assets_frame.grid(row=2, column=1, sticky="news")

    self.root.update()
    return self.game_frame.winfo_id()

def generate_object_frame(self):
    self.object_frame.grid_columnconfigure(0, weight=1)
    self.object_frame.grid_rowconfigure(0, weight=0)
    self.object_frame.grid_rowconfigure(1, weight=1)

    self.object_btn_frame = ttk.Frame(self.object_frame, style="Noborder.TFrame")
    self.object_btn_frame.grid(row=0, column=0, sticky="news")

    self.object_btn_frame.columnconfigure((0,1,2), weight=1)
    self.object_btn_frame.rowconfigure(0, weight=1)

    self.btn_add_object = ttk.Button(self.object_btn_frame, text="Add an\nobject", command=lambda: new_object(self))
    self.btn_add_object.grid(row=0, column=0, sticky="news", padx=(10, 5), pady=10)

    self.btn_edit_object = ttk.Button(self.object_btn_frame, text="Edit the\nobject", command=lambda: edit_object(self))
    self.btn_edit_object.grid(row=0, column=1, sticky="news", padx=5, pady=10)

    self.btn_del_object = ttk.Button(self.object_btn_frame, text="Delete the\nobject", command=lambda: delete_object(self))
    self.btn_del_object.grid(row=0, column=2, sticky="news", padx=(5,10), pady=10)

    self.sub_frame = ttk.Frame(self.object_frame, style="Noborder.TFrame")
    self.sub_frame.grid(row=1, column=0, sticky="news")
    self.sclbox_object = create_scrollbox(self, self.sub_frame)

def create_scrollbox(self, dest_frame: ttk.Frame) -> ttk.Frame:
    dest_frame.grid_columnconfigure(0, weight=1)
    dest_frame.grid_columnconfigure(1, weight=0)
    dest_frame.grid_rowconfigure(0, weight=1)

    canvas = tk.Canvas(dest_frame, highlightthickness=0, background="black")
    canvas.grid(row=0, column=0, sticky="news", padx=(2, 0))

    scrollbar = ttk.Scrollbar(dest_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    sclbox_object_att = ttk.Frame(canvas, style = "Noborder.TFrame")

    canvas_window = canvas.create_window((0, 0), window=sclbox_object_att, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    sclbox_object_att.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))

    canvas.bind("<Enter>", lambda _: canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")))
    canvas.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))

    return sclbox_object_att

def generate_edit_object_frame(self) -> None:
    self.edit_object_frame.grid_columnconfigure((0, 1), weight=1)
    self.edit_object_frame.grid_columnconfigure(2, weight=0)

    self.edit_object_frame.grid_rowconfigure((0, 1, 2), weight=0)
    self.edit_object_frame.grid_rowconfigure(3, weight=1)

    intermediate_frame = ttk.Frame(self.edit_object_frame, style = "Noborder.TFrame")
    intermediate_frame.grid(row=3, column=0, columnspan=3, sticky="news")
    self.sclbox_object_att = create_scrollbox(self, intermediate_frame)

    self.btn_save_object = ttk.Button(self.edit_object_frame, text="Save the object", command=lambda: save_object(self))
    self.btn_save_object.grid(row=0, column=0, sticky="news", padx=(10, 5), pady=5)

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

def generate_placement_frame_ui(self) -> None:
    self.placement_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    self.placement_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

    self.lbl_obj_pos = ttk.Label(self.placement_frame, text="Position")
    self.lbl_obj_pos.grid(row=0, column=0, columnspan=2, padx=5,sticky="ew")

    self.ntr_obj_posx = ttk.Entry(self.placement_frame)
    self.ntr_obj_posx.grid(row=1, column=0, padx=5, sticky="ew")

    self.ntr_obj_posy = ttk.Entry(self.placement_frame)
    self.ntr_obj_posy.grid(row=1, column=1, padx=5, sticky="ew")

    self.ntr_obj_sizex = ttk.Entry(self.placement_frame)
    self.ntr_obj_sizex.grid(row=1, column=2, padx=5, sticky="ew")

    self.ntr_obj_sizey = ttk.Entry(self.placement_frame)
    self.ntr_obj_sizey.grid(row=1, column=3, padx=5, sticky="ew")

    self.lbl_obj_size = ttk.Label(self.placement_frame, text="Size")
    self.lbl_obj_size.grid(row=0, column=2, columnspan=2, padx=5,sticky="ew")

    self.lbl_obj_layer = ttk.Label(self.placement_frame, text="Layer")
    self.lbl_obj_layer.grid(row=2, column=0, columnspan=2, padx=5, sticky="ew")

    self.ntr_obj_layer = ttk.Entry(self.placement_frame)
    self.ntr_obj_layer.grid(row=3, column=0, columnspan=2, padx=5, sticky="ew")

    self.lbl_obj_tags = ttk.Label(self.placement_frame, text="tags")
    self.lbl_obj_tags.grid(row=2, column=2, columnspan=2, padx=5, sticky="ew")

    self.ntr_obj_tags = ttk.Entry(self.placement_frame)
    self.ntr_obj_tags.grid(row=3, column=2, columnspan=2, padx=5, sticky="ew")

def generate_header_frame_ui(self) -> None:
    self.header_frame.grid_columnconfigure((0, 1, 2), weight=1)

    self.header_frame.grid_rowconfigure(0, weight=0)

    self.header_frame.grid_rowconfigure(1, weight=1)

    self.ntr_level_title = ttk.Entry(self.header_frame)
    self.ntr_level_title.grid(row=0, column=0, columnspan=4, sticky="news", padx=10, pady=(10, 5))

    self.play_icon = tk.PhotoImage(file=join(self.assets_path, "icons", "play.png"))
    self.btn_play = ttk.Button(self.header_frame, image=self.play_icon, style="Image.TButton")
    self.btn_play.grid(row=1, column=0, sticky="news", padx=(10, 5), pady=(5, 10))

    self.pause_icon = tk.PhotoImage(file=join(self.assets_path, "icons", "pause.png"))
    self.btn_pause = ttk.Button(self.header_frame, image=self.pause_icon, style="Image.TButton")
    self.btn_pause.grid(row=1, column=1, sticky="news", padx=5, pady=(5, 10))

    self.replay_icon = tk.PhotoImage(file=join(self.assets_path, "icons", "replay.png"))
    self.btn_restart = ttk.Button(self.header_frame, image=self.replay_icon, style="Image.TButton")
    self.btn_restart.grid(row=1, column=2, sticky="news", padx=5, pady=(5, 10))