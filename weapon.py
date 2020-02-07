import pygame
from thing import Thing
from math import degrees
from locals import *


class Weapon(Thing):
    def __init__(self, bitmap, pos, image, size, direction, angle_rad):
        super().__init__(bitmap, pos, image, size)
        self.direction = direction
        if self.direction == 'left':
            self.flip_x()
        self.angle = degrees(angle_rad)
        '''self.rotate(self.angle)'''

    def rotate(self, angle):
        if self.direction == 'right':
            self.image = pygame.transform.rotate(self.image, angle - self.angle)

    def set_pos(self, position):
        self.position = (position[0] + GOOK_RES[0] // 2 - self.size[0] // 2,
                         position[1] + GOOK_RES[1] // 2 + self.size[1] // 2)
