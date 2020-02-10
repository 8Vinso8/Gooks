import pygame
from functions import load_image
from locals import G
from random import randint, choice
from math import copysign


class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, wind, sprites_group, images, screen_rect):
        super().__init__(sprites_group)
        self.screen_rect = screen_rect
        self.prev_wind = wind
        self.images = images
        if wind >= 0:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        self.rect = self.image.get_rect()
        self.x_speed = wind
        self.y_speed = 0
        self.rect.x, self.rect.y = pos
        self.res = (18, 10)

    def update(self, wind, places_to_fill):
        places_to_fill.append(((self.rect.x, self.rect.y), self.res))
        self.x_speed += wind
        self.y_speed += G
        if copysign(1, wind) != copysign(1, self.prev_wind):
            if wind >= 0:
                self.image = self.images[0]
            else:
                self.image = self.images[1]
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if not self.rect.colliderect(self.screen_rect):
            self.kill()


def create_particle(wind, sprites_group, leaves_images, screen_rect):
        Particle((randint(0, 1920), 0), wind, sprites_group, leaves_images, screen_rect)