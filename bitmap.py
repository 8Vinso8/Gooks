from functions import *
from locals import *
from PIL import Image
import os
import math
from explosions import Explosion


class Bitmap:
    def __init__(self, map_file, color_zero, color_one):
        self.bitmap = list()
        self.color_zero = color_zero
        self.color_one = color_one
        self.load_map_file(map_file)
        fullname = os.path.join('data', GROUND_IMG)
        ground_img = Image.open(fullname)
        self.pixels1 = ground_img.load()
        fullname = os.path.join('data', BACKGROUND_IMG)
        background_img = Image.open(fullname)
        self.pixels0 = background_img.load()

    def load_map_file(self, map_file):
        fullname = os.path.join('data', map_file)
        with open(fullname, 'r') as f:
            for line in f.readlines():
                line_list = list(map(int, list(line.strip())))
                self.bitmap.append(line_list)

    def draw(self, window):
        self.draw_part(window, (0, 0), RESOLUTION)

    def draw_part(self, window, start, size):
        start = tuple(map(int, start))
        for i in range(start[0], start[0] + size[0] + 30):
            for j in range(start[1] - 20, start[1] + size[1]):
                try:
                    bit = self.bitmap[j][i]
                except IndexError:
                    continue
                pixel_one = self.pixels1[i, j]
                pixel_zero = self.pixels0[i, j]
                window.set_at((i, j), pixel_one if bit else pixel_zero)

    def explode(self, window, point, size):
        point = tuple(map(round, point))
        for i in range(point[0] - size, point[0] + size):
            for j in range(point[1] - size, point[1] + size):
                if math.sqrt((point[0] - i)**2 + (point[1] - j)**2) <= size:
                    try:
                        self.bitmap[j][i] = 0
                    except IndexError:
                        continue
                    pixel_zero = self.pixels0[i, j]
                    window.set_at((i, j), pixel_zero)
        explosions.append(
            Explosion(
                window,
                (point[0] - size, point[1] - size),
                pygame.transform.scale(load_image(EXPLOSION_IMG, -1), (size * 2, size * 2)),
                (size * 2, size * 2)
            )
        )

    def get_bitmap(self):
        return self.bitmap
