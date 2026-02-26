import tkinter as tk
from tkinter import ttk

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

def generate_build_params(self, class_name):
    for widget in self.sclbox_object_att.winfo_children():
        widget.destroy()

    for param_name, param_val in self.placeable_classes[class_name]["params"].items():
        label_p = ttk.Label(self.sclbox_object_att, text=param_name, padding=10)
        label_p.pack(fill="x", padx=10, pady=5)