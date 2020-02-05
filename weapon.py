import pygame
from thing import Thing


class Weapon(Thing):
    def __init__(self, bitmap, gook, image, size):
        super().__init__(bitmap, gook.get_pos(), image, size)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)