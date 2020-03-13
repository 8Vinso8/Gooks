from functions import *
from locals import *


class InterfaceThing:
    def __init__(self, position, image, size):
        self.position = position
        self.image = load_image(image)
        self.size = size

    def get_image(self):
        return self.image

    def get_pos(self):
        return self.position

    def get_size(self):
        return self.size

    def draw(self, window):
        self.rect = self.image.get_rect(
            bottomright=(self.get_pos()[0] + self.get_size()[0],
                         self.get_pos()[1] + self.get_size()[1])
        )
        window.blit(self.get_image(), self.rect)


class WindIndicator(InterfaceThing):
    def __init__(self, position):
        super().__init__(position, WIND_IMGS[0], WIND_RES)
        self.winds = dict()
        for key in WIND_IMGS:
            self.winds[key] = load_image(WIND_IMGS[key], -1)

    def get_image(self, wind_num=0):
        return self.winds[wind_num]

    def draw(self, window, wind_num=0):
        self.rect = self.image.get_rect(
            bottomright=(self.get_pos()[0] + self.get_size()[0],
                         self.get_pos()[1] + self.get_size()[1])
        )
        window.blit(self.get_image(wind_num), self.rect)


class ChargeBar(InterfaceThing):
    def __init__(self, position):
        super().__init__(position, CHARGE_BAR_IMGS[0], CHARGE_BAR_RES)
        self.next_time = 1/12
        self.n_image = 0
        self.timer = pygame.time.get_ticks()
        self.is_charging = False

    def draw(self, window):
        if self.is_charging:
            self.change_image()
        super().draw(window)

    def change_image(self):
        if pygame.time.get_ticks() - self.timer > self.next_time * 2000:
            self.next_time += 1/12
            if self.n_image < 12:
                self.n_image += 1
            self.image = load_image(CHARGE_BAR_IMGS[self.n_image], -1)

    def start_charge(self):
        self.timer = pygame.time.get_ticks()
        self.is_charging = True

    def stop_charge(self):
        self.is_charging = False
        self.next_time = 1 / 12
        self.n_image = 0
        self.image = load_image(CHARGE_BAR_IMGS[0])