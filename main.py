import pygame as pg
import sys
from pathlib import Path
from collections import defaultdict

import utility_functions as ut
import rendering_functions as rd

class Game:
    def __init__(self):
        pg.init()

        self.RES = (640, 360)
        self.FPS = 60

        self.screen = pg.display.set_mode(self.RES, pg.FULLSCREEN | pg.SCALED)
        self.display = pg.Surface(self.RES)

        pg.display.set_caption("Galaxaris level editor")

        self.clock = pg.time.Clock()
        self.running = True

        self.rendered = defaultdict(list) #if we add a new key, it will already contain an empty list
        self.cam = ut.Camera((0,0))
        self.still_layers = {2, } #every layer that does not move when the cam move
        self.permanent_layers = {0, 1} #every layer that are not rendered again each frame
        self.parallax_layers = []
        self.buttons = []
        self.grid1 = []
        self.font = pg.font.Font("fonts/FRm6x11.ttf", 16) #this font is a modified version of this one https://managore.itch.io/m6x11, it now handles French accents thanks to me, axel.

        try:
            self.block_img = pg.image.load("textures/grass.png").convert() #.convert_alpha() s'il a un canal alpha
        except:
            # Haven't loaded fast enough we show a red square
            self.block_img = pg.Surface((32, 32))
            self.block_img.fill((255, 0, 0))

        for i in range(20):
            x_pos = i * 32
            y_pos = 320

            self.rendered[0].append(ut.RenderedSurface(self.block_img, pg.Vector2(x_pos, y_pos)))

        ut.render_text(self,f"Alors ? l'évênement de samedi est trop tôt ? Près de là bas de toute façon. Si vous le dîtes ...",(0, 90), self.font, layer=1)
        ut.render_text(self,"0, 0",(2, 2), self.font, layer=1, color = (255, 100, 100), alpha=100)

        self.buttons.append(ut.BasicButton((50,50), (75,25), message="salut", font=self.font))

    def _check_events(self):
        """Get every input, and act accordingly"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.MOUSEMOTION:
                if pg.mouse.get_pressed()[2]:  #left clic
                    self.cam.pos -= event.rel

                for button in self.buttons:
                    if button.check_collision(event.pos + self.cam.pos):
                        button.render((0,200,0), button.message, button.txt_color, size_factor=1.1)

            elif event.type == pg.KEYDOWN:
                if (event.mod & pg.KMOD_CTRL) and event.key == pg.K_p:

                    parallax_path = ut.get_file_path(message = "Choose a texture for parallax")
                    if not parallax_path == "":
                        parallax_texture  = pg.image.load(parallax_path).convert_alpha()

                        speed = float(Path(parallax_path).name.split("x")[0]) #the name of the file should be written this way speedx*.png, * is obviously anything and speed a float/int
                        self.parallax_layers.append(ut.Parallax(parallax_texture, pg.Vector2(0, 0), pg.Vector2(speed, speed)))

                        self.parallax_layers.sort(key=lambda parallax: parallax.speed.x)

    def _update(self):
        """Run any logic not related to drawing"""
        pass

    def _draw(self):
        """Draw things on the screen"""
        self.display.fill((20, 20, 30))  # It is our clear screen, color = black

        ut.render_text(self, f"FPS: {int(self.clock.get_fps())}", (1, 348), self.font, layer = 2, alpha=100)

        rd.render_grid(self)

        rd.render_parallax(self)

        rd.render_buttons(self)

        cellx, celly = ut.xy_to_grid(pg.mouse.get_pos() + self.cam.pos)
        highlight = pg.Surface((32, 32)).convert_alpha()
        highlight.fill((255,244,79, 50))
        self.rendered[3].append(ut.RenderedSurface(highlight, pg.Vector2(cellx*32, celly*32)))

        for layer in sorted(self.rendered.keys()):

            if layer in self.still_layers:
                for rendered in self.rendered[layer]:
                    self.display.blit(rendered.surface, rendered.pos)

            else:
                for rendered in self.rendered[layer]:
                    self.display.blit(rendered.surface, rendered.pos - self.cam.pos)

            if layer not in self.permanent_layers:
                del self.rendered[layer] #we will render again this layer in the next frame so we erase it

        pg.transform.scale(self.display, self.screen.get_size(), self.screen) #scales up everything to fit the fullscreen
        pg.display.flip()  # Draw the new frame

    def run(self):
        """Game loop"""
        while self.running:
            self._check_events()
            self._update()
            self._draw()
            self.clock.tick(self.FPS)  # If we still have time left, we wait until reaching 1000/FPS ms

        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()