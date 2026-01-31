import pygame as pg
import utility_functions as ut

def render_grid(self) -> None:
    self.grid = pg.Surface(self.RES, pg.SRCALPHA)

    offset = pg.Vector2(self.cam.pos.x % 32, self.cam.pos.y % 32)

    for i in range(21):
        pg.draw.line(self.grid, (200, 200, 200, 50), (32 * i, 0) - offset, (32 * i, self.RES[1] + 32) - offset, width=1)

    for j in range(13):
        pg.draw.line(self.grid, (200, 200, 200, 50), (0, 32 * j) - offset, (self.RES[0] + 32, 32 * j) - offset, width=1)

    self.rendered[2].append(ut.RenderedSurface(self.grid, pg.Vector2(0, 0)))

def render_parallax(self) -> None:
    for index, parallax in enumerate(self.parallax_layers):

        w,h = parallax.surface.get_size()
        offset = pg.Vector2(self.cam.pos.x * parallax.speed.x % w, self.cam.pos.y * parallax.speed.y % h)

        if parallax.speed.x < 1:

            for j in range(2):
                for i in range(2):
                    self.rendered[-20+index].append(ut.RenderedSurface(parallax.surface, pg.Vector2(w * i, h * j) - offset))
                    self.still_layers.add(-20+index)

        else:
            for i in range(2):
                for j in range(2):
                    self.rendered[20 + index].append(ut.RenderedSurface(parallax.surface, pg.Vector2(w * i, h * j) - offset))
                    self.still_layers.append(20 + index)
                    self.still_layers.add(20 + index)

def render_buttons(self) -> None:
    for button in self.buttons:
        if button.visible:
            self.rendered[4].append(button.surface)
