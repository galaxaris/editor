from tkinter import filedialog
from tkinter import ttk
import tkinter as tk

def new_object(self):
    self.obj_editing = True
    raise_obj_frame(self)

def edit_object(self):
    self.obj_editing = True
    raise_obj_frame(self)

def exit_edit(self):
    self.obj_editing = False
    raise_obj_frame(self)

def save_object(self):
    exit_edit(self)

def raise_obj_frame(self):
    if self.obj_editing:
        self.edit_object_frame.tkraise()
    else:
        self.object_frame.tkraise()

def numerize(content:str, type_: str):
    try:
        if content == "-": #with only a single - a casting wouldn't work
            pass
        elif type_ == "int":
            a = int(content)
        else:
            a = float(content)
    except:
        content = content[0:-1]

    return content

def only_numbers(event, type_: str):
    w = event.widget
    content = w.get()
    new_content = numerize(content, type_)

    if content != new_content:
        w.delete(0, tk.END)
        w.insert(0, content)

def vectorise(event, count:int=1):
    w = event.widget
    content = w.get()

    if content == "":
        w.config(validate="none") #lets us put ourselves the "," because the forbid_comma is very strong
        w.insert(0, ","*count)
        w.config(validate="key")

    else:
        values = content.split(",")
        new_content = numerize(values[0], type_="float")
        for i in range(1,len(values)):
            content += ","+numerize(values[i], type_="float")

        w.config(validate="none")  # lets us put ourselves the "," because the forbid_comma is very strong
        w.delete(0, tk.END)
        w.insert(0, new_content)
        w.config(validate="key")



def forbid_comma(char):
    if char == ",":
        return False
    return True

def generate_build_params(self, class_name):
    for widget in self.sclbox_object_att.winfo_children():
        widget.destroy()

    row = 0
    for param_name, param in self.placeable_classes[class_name]["params"].items():
        label_p = ttk.Label(self.sclbox_object_att, text=param_name, padding=10)
        label_p.grid(row=row, column=0, padx=5, pady=5, sticky="news")
        print(param["type"])
        match param["type"]:
            case "int" | "float":
                entry_p = ttk.Entry(self.sclbox_object_att)
                entry_p.grid(row=row, column=1, padx=5, sticky="ew")

                entry_p.bind("<KeyRelease>", lambda event,type_=param["type"]: only_numbers(event, type_))

            case "str":
                entry_p = ttk.Entry(self.sclbox_object_att)
                entry_p.grid(row=row, column=1, padx=5, sticky="ew")

            case "Vector2" | "tuple":
                entry_p = ttk.Entry(self.sclbox_object_att, validatecommand=(self.root.register(forbid_comma), "%S"))
                entry_p.grid(row=row, column=1, padx=5, sticky="ew")
                entry_p.insert(0, ",")
                entry_p.config(validate="key") #activates the blocus on the ","

                entry_p.bind("<KeyRelease>", vectorise)

        row += 1

    self.sclbox_object_att.grid_columnconfigure((0,1), weight=1)
    self.sclbox_object_att.grid_rowconfigure([i for i in range(row)], weight=1)

def add_a_music(self):
    filetypes = (('Audio files', '*.mp3 *.wav *.ogg'),('Any files', '*.*'))

    filename = filedialog.askopenfilename(title='Select a music',initialdir='/',filetypes=filetypes)

    if filename:
        print(f"Musique sélectionnée : {filename}")
        return filename

    return None