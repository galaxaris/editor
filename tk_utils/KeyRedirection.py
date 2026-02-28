import pygame as pg

from api.utils import Inputs

def bind_keys(self, event):
    self.root.bind("<KeyPress>", lambda _event: handle_keydown(self, _event))
    self.root.bind("<KeyRelease>", lambda _event: handle_keyup(self, _event))

def unbind_keys(self, event):
    Inputs.editor_release_key()
    self.root.unbind("<KeyPress>")
    self.root.unbind("<KeyRelease>")

def generate_key_map():
    mapping = {
        "Escape": pg.K_ESCAPE,
        "Return": pg.K_RETURN,
        "space": pg.K_SPACE,
        "Up": pg.K_UP,
        "Down": pg.K_DOWN,
        "Left": pg.K_LEFT,
        "Right": pg.K_RIGHT,
        "BackSpace": pg.K_BACKSPACE,
        "Delete": pg.K_DELETE,
        "Tab": pg.K_TAB,
        "Shift_L": pg.K_LSHIFT
    }

    for i in range(1, 13): #F keys
        if i == 11:
            continue  # we want to skip F11 because the fullscreen of the pygame window would break the editor
        mapping[f"F{i}"] = getattr(pg, f"K_F{i}")

    for i in range(10): #num keys
        mapping[str(i)] = getattr(pg, f"K_{i}")

    for i in range(26): #letters
        char = chr(i + 97)
        char_upper = chr(i + 65)
        mapping[char] = getattr(pg, f"K_{char}")
        mapping[char_upper] = getattr(pg, f"K_{char}")

    return mapping

def handle_keydown(self, event):
    pg_key = self.key_map.get(event.keysym)
    if pg_key:
        pg.event.post(pg.event.Event(pg.KEYDOWN, {'key': pg_key}))
        Inputs.editor_edit_key(pg_key, True)

def handle_keyup(self, event):
    pg_key = self.key_map.get(event.keysym)
    if pg_key:
        pg.event.post(pg.event.Event(pg.KEYUP, {'key': pg_key}))
        Inputs.editor_edit_key(pg_key, False)