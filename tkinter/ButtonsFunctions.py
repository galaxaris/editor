def new_object(self, event):
    self.obj_editing = True
    raise_obj_frame(self)

def edit_object(self, event):
    self.obj_editing = True
    raise_obj_frame(self)

def save_object(self, event):
    self.obj_editing = False
    raise_obj_frame(self)

def raise_obj_frame(self):
    if self.obj_editing:
        self.edit_object_frame.tkraise()
    else:
        self.object_frame.tkraise()