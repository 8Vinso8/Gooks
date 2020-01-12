import pygame
import math
from pygame.constants import *
from constants import *


pygame.init()
wind = 0
is_working = True


class Thing:
    def __init__(self, pos, image, res):
        self.position = pos
        self.resolution = res
        self.image = pygame.image.load(image).convert()
        self.image_surf = self.image
        self.image_surf.set_colorkey((0, 0, 0))

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_rect(self):
        return pygame.Rect(self.get_x(), self.get_y(), self.resolution[0], self.resolution[1])

    def draw(self):
        self.image_rect = self.image_surf.get_rect(
            bottomright=(self.position[0] + self.resolution[0],
                         self.position[1] + self.resolution[1])
        )
        window.blit(self.image_surf, self.image_rect)

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)


class Gook(Thing):
    def __init__(self, pos, team):
        super().__init__(pos, gook_img, gook_res)
        self.team = team
        self.movement = 100

    def get_team(self):
        return self.team

    def move(self, x, y=0):
        super().move(x, y)
        self.movement -= x


class Projectile(Thing):
    def __init__(self, pos, weapon, angle, speed):
        super().__init__(pos, projectiles[weapon][0], projectiles[weapon][1])
        self.g = projectiles[weapon][2]
        self.speed_x = speed * math.cos(angle) + wind
        self.speed_y = speed * math.sin(angle)

    def move(self):
        super().move(self.speed_x, self.speed_y)
        self.speed_y -= g


while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            working = False
        if event.type == KEYDOWN:
            if event.key == K_F1:
                if fullscreen:
                    window: pygame.Surface = pygame.display.set_mode(resolution)
                    fullscreen = False
                else:
                    window: pygame.Surface = pygame.display.set_mode(resolution, FULLSCREEN)
                    fullscreen = True
            if event.key == K_ESCAPE:
                working = False



