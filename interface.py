from functions import *
from locals import *


class InterfaceThing:
    def __init__(self, position, image, size):
        self.position = position
        self.image = image
        self.size = size
        self.rect = self.image.get_rect(
            bottomright=(self.get_pos()[0] + self.get_size()[0],
                         self.get_pos()[1] + self.get_size()[1])
        )

    def get_image(self):
        return self.image

    def get_pos(self):
        return self.position

    def get_size(self):
        return self.size

    def get_rect(self):
        return self.rect

    def draw(self, window):
        window.blit(self.get_image(), self.get_rect())


class WindIndicator(InterfaceThing):
    def __init__(self, position):
        super().__init__(position, WIND_IMGS[0], WIND_RES)
        self.winds = dict()
        for key, wind_img in WIND_IMGS:
            self.winds[key] = load_image(wind_img, -1)

    def get_image(self, wind_num=0):
        return self.winds[wind_num]

    def draw(self, window, wind_num=0):
        window.blit(self.get_image(wind_num), self.get_rect())


class ChargeBar(InterfaceThing):
    def __init__(self, position):
        super().__init__(position, CHARGE_BAR_IMG, CHARGE_BAR_RES)
        self.positive_wind = list()
        self.negative_wind = list()
        self.zero_wind = load_image('windbox.png', -1)
        for i in range(1, 6):
            self.positive_wind.append(load_image(f'windbox{str(i)}.png'))
        for j in range(1, 6):
            self.negative_wind.append(load_image(f'windbox{str(j * -1)}.png'))

    def get_image(self, wind_num):
        if not wind_num:
            return self.zero_wind
        elif wind_num > 0:
            return self.positive_wind[wind_num - 1]
        else:
            return self.negative_wind[wind_num * -1 - 1]

    def get_pos(self):
        return self.position