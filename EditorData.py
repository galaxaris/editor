from tkinter import ttk
import pygame as pg

from api.GameObject import GameObject
from api.environment.Solid import Solid
from api.assets.Texture import Texture
from editor.ReadApiGa import Param

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

class Object(Solid):
    def __init__(self, pos: tuple[int, int] | pg.Vector2, size: tuple[int, int] | pg.Vector2, name: str, texture: str = None):
        super().__init__(pos, size)
        self.name = name
        self.layer = ""
        self.tags = {"editorObj"}
        self._texture = texture

        self.set_color((200, 200, 200))
        if texture is not None:
            self.set_texture(Texture(texture))

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        self._texture = value
        self.set_texture(Texture(value))

class ObjectDef:
    def __init__(self, name: str, class_ref: str, params: list[Param], tags: set):
        self.name = name
        self.class_ref = class_ref
        self.params = params
        self.tags = tags
        self.texture = None

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value):
        self._texture = value
        #update_textures(self.name, self.texture)