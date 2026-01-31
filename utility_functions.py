import pygame as pg
import tkinter as tk
from tkinter import filedialog

#The master of this place is I, Axel. Contact me if you have a problem with this module or the game class in general

class RenderedSurface:
    def __init__(self, surface: pg.Surface, pos: pg.Vector2) -> None:
        self.surface = surface
        self.pos = pos

def render_text(self, text: str, pos: tuple[float, float], font: pg.font.Font, layer: int=0, color: tuple[int, int, int]=(255,255,255), alpha: int =255) -> None:
    """Create a new rendered surface with a new text surface. Then add it to the right layer in the rendered dict"""
    text_surface = font.render(text, False, color).convert_alpha()

    if alpha != 255:
        text_surface.set_alpha(alpha)

    self.rendered[layer].append(RenderedSurface( text_surface, pg.Vector2(pos[0], pos[1])))

class Camera:
    def __init__(self, pos: tuple[float, float]) -> None:
        self.pos = pg.Vector2(pos[0], pos[1])

class Parallax:
    def __init__(self, surface: pg.Surface, pos: pg.Vector2, speed: pg.Vector2) -> None:
        self.surface = surface
        self.pos = pos
        self.speed = speed

def get_file_path(message: str = "choose a file"):
    root = tk.Tk()
    root.withdraw() #hide the tkinter app

    root.attributes('-topmost', True) #put the window in foreground because we are in fullscreen

    file_path = filedialog.askopenfilename(title=message,filetypes=[("Images PNG", "*.png"), ("Any files", "*.*")])

    root.destroy() #goodbye tkinter

    #this is a way to put the focus back on our window (thank you very much internet, I would never find another way to do it)
    pg.display.set_caption("Galaxaris level editor")
    pg.event.pump()

    return file_path

class BasicButton:
    def __init__(self, pos: tuple[float, float], size: tuple[int, int], message: str = "", font: pg.font.Font = None, bg_color: tuple[int, int,int]=(255,255,255), txt_color: tuple[int, int,int]=(0,0,0), visible: bool=True) -> None:
        self.hitbox = pg.Rect(pos, size)
        self.og_hitbox = pg.Rect(pos, size) #is used to remember what is the non hovered size
        self.message = message
        self.bg_color = bg_color
        self.txt_color = txt_color
        self.font = font
        self.hovered = False
        self.surface = None
        self.visible = visible

        self.render(bg_color, message, txt_color) #initial render

    def render(self, bg_color: tuple[int, int,int], message: str, txt_color: tuple[int, int,int], size_factor: float=1.0) -> None:
        self.hitbox.size = pg.Vector2(self.og_hitbox.size) * size_factor
        self.hitbox.center = self.og_hitbox.center

        bg = pg.Surface(self.hitbox.size)
        bg.fill(bg_color)

        if message != "" and self.font is not None:

            text_surface = self.font.render(message, False, txt_color)
            centered_pos = text_surface.get_rect(center=bg.get_rect().center)

            bg.blit(text_surface, centered_pos) #we put our text surface on the button bg so the bg become the whole button that we blit later

        self.surface = RenderedSurface(bg, pg.Vector2(self.hitbox.topleft))

    def check_collision(self, mouse_pos: tuple[float, float]) -> bool:
        hover = self.hitbox.collidepoint(mouse_pos)

        if not hover and self.hovered:
            self.render(self.bg_color, self.message, self.txt_color)

        self.hovered = hover
        return hover

class TextureButton:
    def __init__(self, pos: tuple[float, float], texture: pg.Surface, message: str = "", font: pg.font.Font = None, txt_color: tuple[int, int,int]=(0,0,0), visible: bool=True) -> None:
        self.hitbox = texture.get_rect(topleft=pos)
        self.texture = texture
        self.message = message
        self.txt_color = txt_color
        self.font = font
        self.hovered = False
        self.surface = None
        self.visible = visible

        self.render(texture, message, txt_color) #initial render

    def render(self, texture: pg.Surface, message: str, txt_color: tuple[int, int,int]) -> None:
        bg = texture.copy()

        if message != "" and self.font is not None:

            text_surface = self.font.render(message, False, txt_color)
            centered_pos = text_surface.get_rect(center=bg.get_rect().center)

            bg.blit(text_surface, centered_pos) #we put our text surface on the button bg so the bg become the whole button that we blit later

        self.surface = RenderedSurface(bg, pg.Vector2(self.hitbox.topleft))

    def check_collision(self, mouse_pos: tuple[float, float]) -> bool:
        hover = self.hitbox.collidepoint(mouse_pos)

        if not hover and self.hovered:
            self.render(self.texture, self.message, self.txt_color)

        self.hovered = hover
        return hover

def xy_to_grid(pos: tuple[int, int]) -> tuple[int, int]:
    return pos[0]//32, pos[1]//32