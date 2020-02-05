from thing import Thing
from locals import *


class Explosion(Thing):
    def __init__(self, bitmap, pos, image, size):
        super().__init__(bitmap, pos, EXPLOSION_IMG, size)
        self.image = image
        self.life_timer = 0

    def increase_life_timer(self):
        self.life_timer += 1

    def check_state(self):
        if self.life_timer >= 10:
            return 'del'
