from tkinter import filedialog
from tkinter import ttk
import tkinter as tk

from api.utils.Debug import toggle


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
            self.objects_info.add(name, self.cbb_object_class.get(), [])

            btn_object = ttk.Button(self.sclbox_object, text= f"{self.cbb_object_class.get()} : {name}")
            btn_object.pack(padx=5,pady=5, fill="x")
            btn_object.configure(command=lambda btn=btn_object: select_object(self,btn))

            exit_edit(self)

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

        param = params.many_types[0]
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

    self.sclbox_object_att.grid_columnconfigure((0,1), weight=1, uniform="col3")
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
