from ReadApiGa import Param
from tkinter import ttk
import pygame as pg

from api.environment.Solid import Solid

class LevelInfo:
    def __init__(self):
        self.name = ""
        self.music = None
        self.script = None
        self.parallax = None

class ObjectsInfo:
    def __init__(self):
        self.objects = []

    def add(self, name:str, class_ref:str, params: list, tags: set):
        self.objects.append(ObjectDef(name, class_ref, params, tags))

    def delete(self, btn: ttk.Button):
        class_ref, sep, obj_name = btn.cget("text").partition(":")
        for obj in self.objects:
            if obj["name"] == obj_name.strip():
                self.objects.remove(obj)
                break

    def name_dont_exist(self, name: str) -> bool:
        names = [obj["name"] for obj in self.objects]
        if not name in names:
            return True
        return False

class ObjectsLayout:
    def __init__(self):
        self.obj_list = []

class Object:
    def __init__(self, name: str, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] | pg.Vector2):
        self.name = name
        self.pos = pg.Vector2(pos)
        self.size = pg.Vector2(size)
        self.layer = ""
        self.tags = set()
        self.solid = Solid(self.pos, self.size)
        self.solid.set_color((200, 200, 200))

    def resize(self, size):
        self.size = pg.Vector2(size)
        self.solid = Solid(self.pos, self.size)
        self.solid.set_color((200, 200, 200))

class ObjectDef:
    def __init__(self, name: str, class_ref: str, params: list[Param], tags: set):
        self.name = name
        self.class_ref = class_ref
        self.params = params
        self.tags = tags

