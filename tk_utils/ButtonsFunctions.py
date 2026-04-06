from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

from api.utils.Debug import toggle
from editor.EditorData import Object
from api.utils.Inputs import get_mouse
from api.GameObject import GameObject
from api.physics.Collision import get_collided_objects

def new_object(self):
    if not self.obj_editing:
        self.ntr_object_name.delete(0, tk.END)
        self.obj_editing = True
        raise_obj_frame(self)

def edit_object(self):
    if self.selected_object and not self.obj_editing:
        self.ntr_object_name.delete(0, tk.END)
        class_ref, sep, obj_name = self.selected_object.cget("text").partition(":")
        self.ntr_object_name.insert(0, obj_name.strip())

        self.obj_editing = True
        raise_obj_frame(self)

def delete_object(self):
    if self.selected_object and not self.obj_editing:
        self.objects_info.delete(self.selected_object)
        self.selected_object.destroy()

def exit_edit(self):
    self.obj_editing = False
    raise_obj_frame(self)

def save_object(self):
    if self.obj_editing:
        name = self.ntr_object_name.get()
        if name != "" and self.objects_info.name_dont_exist(name):
            params = retrieve_params(self)
            if params:
                self.objects_info.add(name, self.cbb_object_class.get(), params, set())

                btn_object = ttk.Button(self.sclbox_object, text= f"{self.cbb_object_class.get()} : {name}")
                btn_object.pack(padx=5,pady=5, fill="x")
                btn_object.configure(command=lambda btn=btn_object: select_object(self,btn))

                exit_edit(self)

def retrieve_params(self) -> list|None:
    params = []
    entries = self.sclbox_object_att.grid_slaves(column=1)
    expected_params = self.placeable_classes[self.cbb_object_class.get()]["params"]
    entries.reverse()

    for index, param in enumerate(expected_params):
        try:
            match param.type_:
                case "int":
                    val = int(entries[index].get())

                case "float":
                    val = float(entries[index].get())

                case "str":
                    val = entries[index].get()

                case "bool":
                    val = entries[index].cget("text")
                    val = True if val == "True" else False

                case t if any(x in t for x in ['tuple', 'Vector2']):
                    sub_entries = entries[index].grid_slaves(row=0)
                    sub_entries.reverse()

                    val = []
                    for index2, type_ in enumerate(param.many_types):
                        match type_:
                            case "int":
                                val.append(int(sub_entries[index2].get()))

                            case "float":
                                val.append(float(sub_entries[index2].get()))

                            case "str":
                                val.append(sub_entries[index2].get())

                            case "bool":
                                tmp = sub_entries[index2].cget("text")
                                val.append(True if tmp == "True" else False)

                            case _:
                                val.append(None)

                case _:
                    val = None

        except:
            messagebox.showwarning("Warning!", f"{param.name} {param.type_} is not filled!")
            val = None

        params.append(val)
    if len(params) == 0:
        return None
    return params

def place_object(self, event: tk.Event):
    if self.selected_object and self.gameFrameFocused:
        name = self.selected_object.cget("text")
        self.objects_layout.obj_list.append(Object(get_mouse()/self.pg_app.game.scene.scale_ratio+self.pg_app.game.scene.camera.position, (10,10), name))

def replace_object(self, event: tk.Event):
    mouse = GameObject(get_mouse()/self.pg_app.game.scene.scale_ratio+self.pg_app.game.scene.camera.position, (1,1))
    obj_touched = get_collided_objects(mouse, "editorObj",self.objects_layout.obj_list, 0, 0)

    if len(obj_touched) > 0:
        self.replace_obj = obj_touched[0][0]
        update_replace_window(self)

def update_replace_window(self):
    rewrite_ntr(self.ntr_obj_posx, int(self.replace_obj.pos.x))
    rewrite_ntr(self.ntr_obj_posy, int(self.replace_obj.pos.y))

    rewrite_ntr(self.ntr_obj_sizex, int(self.replace_obj.size.x))
    rewrite_ntr(self.ntr_obj_sizey, int(self.replace_obj.size.y))

def rewrite_ntr(ntr: ttk.Entry, text: str|int|float):
    ntr.delete(0, tk.END)
    ntr.insert(0, text)

def select_object(self,btn):
    if self.selected_object:
        self.selected_object.configure(style="TButton")

    self.selected_object = btn
    self.selected_object.configure(style="Selected.TButton")

def raise_obj_frame(self):
    if self.obj_editing:
        self.edit_object_frame.tkraise()
    else:
        self.object_frame.tkraise()

def numerize(content:str, type_: str, cursor_pos: int):
    try:
        if content == "-": #with only a single - a casting wouldn't work
            pass
        elif type_ == "int":
            a = int(content)
        else:
            a = float(content)
        return content
    except:
        return content[:cursor_pos] + content[cursor_pos+1:]

def only_numbers(event, type_: str):
    w = event.widget
    content = w.get()
    cursor_pos = w.index(tk.INSERT)-1 #needs the -1 to remove the right letter and to stay in place in that case
    new_content = numerize(content, type_, cursor_pos)

    if content != new_content:
        w.delete(0, tk.END)
        w.insert(0, new_content)
        w.icursor(cursor_pos)

def resize_obj(self):
    self.replace_obj.set_size((int(self.ntr_obj_sizex.get()), int(self.ntr_obj_sizey.get())))

def move_obj(self):
    self.replace_obj.set_position((int(self.ntr_obj_posx.get()), int(self.ntr_obj_posy.get())))

def toggle_button(btn: ttk.Button):
    if btn.cget("text") == "True":
        btn.configure(text="False")

    else:
        btn.configure(text="True")

def generate_build_params(self, class_name):
    for widget in self.sclbox_object_att.winfo_children():
        widget.destroy()

    row = 0
    for params in self.placeable_classes[class_name]["params"]:
        label_p = ttk.Label(self.sclbox_object_att, text=f"{params.name}\n({params.type_})", padding=10)
        label_p.grid(row=row, column=0, padx=5, pady=5, sticky="news")

        param = params.many_types
        match params.type_:
            case "int" | "float":
                entry_p = ttk.Entry(self.sclbox_object_att)
                entry_p.grid(row=row, column=1, padx=5, sticky="ew")

                entry_p.bind("<KeyRelease>", lambda event,type_=params.type_: only_numbers(event, type_))

            case "str":
                entry_p = ttk.Entry(self.sclbox_object_att)
                entry_p.grid(row=row, column=1, padx=5, sticky="ew")

            case "bool":
                toggle_p = ttk.Button(self.sclbox_object_att, text = "True")
                toggle_p.grid(row=row, column= 1, padx=5, sticky="ew")
                toggle_p.configure(command= lambda btn=toggle_p: toggle_button(btn))

            case t if any(x in t for x in ['tuple', 'list', 'Vector2']):
                tuple_frame = ttk.Frame(self.sclbox_object_att, style="Noborder.TFrame")
                tuple_frame.grid(row=row, column=1, sticky="news")
                range_ = [i for i in range(param["count"]+1)]
                tuple_frame.columnconfigure(range_, weight=1)
                tuple_frame.rowconfigure(0, weight=1)

                for i in range(param["count"]):
                    entry_p = ttk.Entry(tuple_frame)
                    entry_p.grid(row=0, column=i, padx=5, sticky="ew")

                    entry_p.bind("<KeyRelease>", lambda event, type_=param["val"][0]: only_numbers(event, type_))

            case _:
                print("default",params.__dict__)

        row += 1

    self.sclbox_object_att.grid_columnconfigure((0, 1), weight=1, uniform="col3")
    if row!=0:
        self.sclbox_object_att.grid_rowconfigure([i for i in range(row)], weight=1)

def add_a_music(self):
    filetypes = (('Audio files', '*.mp3 *.wav *.ogg'),('Any files', '*.*'))

    filename = filedialog.askopenfilename(title='Select a music',initialdir='/',filetypes=filetypes)

    if filename:
        self.level_info.music = filename
        self.env_menu.entryconfig(3, label="✓ Choose a music")

def add_a_script(self):
    filetypes = (('Python file', '*.py'),('Any files', '*.*'))

    filename = filedialog.askopenfilename(title='Select a script',initialdir='/',filetypes=filetypes)

    if filename:
        self.level_info.script = filename
        self.env_menu.entryconfig(4, label="✓ Choose a script")
