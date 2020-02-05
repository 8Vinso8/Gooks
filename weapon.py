import pygame
from thing import Thing


class Weapon(Thing):
    def __init__(self, bitmap, pos, image, size):
        super().__init__(bitmap, pos, image, size)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)