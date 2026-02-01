import pygame as pg
import tkinter as tk
from tkinter import ttk
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

class Object:
    def __init__(self):
        self.texture = None
        self.color = None
        self.property = None
        self.type = None
        self.texture_type = None

class ControlPanel:
    def __init__(self, master):
        self.master = master
        self.root = tk.Tk()
        self.root.title("Control Panel")
        self.root.geometry("720x720")

        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)

        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.input_bg = "#3c3f41"
        self.accent_color = "#4a90e2"
        self.root.configure(bg=self.bg_color)

        self.actual_object = Object()

        self.setup_styles()
        self.create_ui()

    def setup_styles(self):
        """Style configuration using ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=self.input_bg, background=self.input_bg, foreground=self.fg_color)
        style.configure("TLabel", background=self.bg_color, foreground=self.fg_color, font=('Arial', 10, 'bold'))

    def create_ui(self):
        l_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        l_frame.grid(row=0, column=0, sticky="ns")

        tk.Label(l_frame, text="OBJECT", bg=self.bg_color, fg=self.fg_color,
                 font=('Arial', 14, 'bold', 'underline')).pack(anchor="w")

        self.obj_cbb = ttk.Combobox(l_frame, values=["Player", "Enemy", "Wall"], width=15)
        self.obj_cbb.pack(pady=(10, 5))

        tk.Label(l_frame, text="OR", bg=self.bg_color, fg=self.fg_color).pack(pady=5)

        # BUTTON NEW
        tk.Button(l_frame, text="NEW", bg=self.accent_color, fg="white", width=10, relief="flat").pack(pady=5)

        # LINE
        separator = tk.Frame(self.root, bg="#444444", width=2)
        separator.grid(row=0, column=1, sticky="ns", pady=20)

        r_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        r_frame.grid(row=0, column=2, sticky="nsew")

        # NAME
        tk.Label(r_frame, text="NAME", bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        self.name_ntr = tk.Entry(r_frame, bg=self.input_bg, fg=self.fg_color, insertbackground="white",borderwidth=0)
        self.name_ntr.pack(fill="x", pady=(0, 15))
        self.name_ntr.bind("<KeyRelease>", self.update_name)

        # COLOR
        tk.Label(r_frame, text="COLOR (in the editor and hex format)", bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        self.color_ntr = tk.Entry(r_frame, bg=self.input_bg, fg=self.fg_color, insertbackground="white",borderwidth=0)
        self.color_ntr.pack(fill="x", pady=(0, 15))
        self.color_ntr.bind("<KeyRelease>", self.update_color)

        # TYPE
        tk.Label(r_frame, text="TYPE", bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        self.type_cbb = ttk.Combobox(r_frame, values=["block","enemy", "player", "item", "decoration", "event trigger"], state="readonly")
        self.type_cbb.pack(fill="x", pady=(0, 15))
        self.type_cbb.bind("<<ComboboxSelected>>", self.update_type)

        # PROPERTIES
        tk.Label(r_frame, text="PROPERTIES", bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        self.prop_cbb = ttk.Combobox(r_frame, values=["SOLID", "FIXED_POSITION", "BREAKABLE"], state="readonly")
        self.prop_cbb.pack(fill="x", pady=(0, 15))
        self.prop_cbb.bind("<<ComboboxSelected>>", self.update_property)

        # TEXTURE TYPE
        tk.Label(r_frame, text="TEXTURE TYPE", bg=self.bg_color, fg=self.fg_color).pack(anchor="w")
        self.tex_cbb = ttk.Combobox(r_frame, values=["no texture", "single", "tile set", "sprite sheet"], state="readonly")
        self.tex_cbb.pack(fill="x", pady=(0, 15))
        self.tex_cbb.bind("<<ComboboxSelected>>", self.update_texture_type)

        # BUTTON ADD TEXT
        tk.Button(r_frame, text="ADD TEXTURE", bg="#444444", fg="white", relief="flat").pack(pady=10)

        # BUTTON DELETE OBJECT
        tk.Label(l_frame, text="DANGER ZONE", bg=self.bg_color, fg="#ff4444", font=('Arial', 8, 'bold')).pack(anchor="w", pady=(80, 0))
        tk.Button(l_frame, text="DELETE OBJECT", bg="#992222", fg="white", relief="flat", font=('Arial', 10, 'bold'), command=self.delete_object_action).pack(fill="x", pady=5)

    def update_name(self):
        self.actual_object.name = self.name_ntr.get()

    def update_color(self):
        self.actual_object.color = self.color_ntr.get()

    def update_texture(self):
        self.actual_object.texture = get_file_path(message="Choose a texture image")

    def update_texture_type(self, event):
        self.actual_object.texture_type = self.tex_cbb.get()

    def update_property(self, event):
        self.actual_object.property = self.pop_cbb.get()

    def update_type(self, event):
        self.actual_object.type = self.type_cbb.get()

    def delete_object_action(self):
        pass

    def disable_event(self):
        # When the user try to kill this window it redirect to this function that does nothing instead
        pass

    def update(self):
        self.root.update() #used to update this window in our app so it can run at the same time without blocking it in a while loop