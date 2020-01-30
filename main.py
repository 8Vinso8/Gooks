import pygame
import math
from pygame.constants import *
from locals import *
import random
import itertools


def get_next_team():
    for team_now in TEAMS:
        yield team_now


team_gen = get_next_team()
gook_gen = itertools.cycle(range(TEAM_LEN))
n_gook = next(gook_gen)


def next_turn():
    global team, gook, team_gen, n_gook
    try:
        team = next(team_gen)
        gook = team[n_gook]
    except StopIteration:
        n_gook = next(gook_gen)
        team_gen = get_next_team()
        team = next(team_gen)
        gook = team[n_gook]
    print(team, gook)


class Map:
    def __init__(self, map_file, color_zero, color_one):
        self.bitmap = list()
        self.color_zero = color_zero
        self.color_one = color_one
        self.load_map_file(map_file)

    def load_map_file(self, map_file):
        with open(map_file, 'r') as f:
            for line in f.readlines():
                line_list = list(map(int, list(line.strip())))
                self.bitmap.append(line_list)
        print(self.bitmap)

    def draw(self):
        for i in range(1920):
            for j in range(1080):
                window.set_at((i, j), self.color_one if self.bitmap[j][i] else self.color_zero)

    def draw_part(self, window, start, size):
        for i in range(start[0], start[0] + size[0]):
            for j in range(start[1], start[1] + size[1]):
                window.set_at((i, j), self.color_one if self.bitmap[j][i] else self.color_zero)
                # Поменять цвета местами если баги

    def explode(self, point, size):
        for i in range(point[0] - size, point[0] + size):
            for j in range(point[1] - size, point[1] + size):
                self.bitmap[j][i] = 0


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
    def __init__(self, pos, name):
        super().__init__(pos, GOOK_IMG, GOOK_RES)
        self.name = name
        self.movement = 100

    def move(self, x, y=0):
        super().move(x, y)
        self.movement -= x


class Shot(Thing):
    def __init__(self, pos, weapon, angle, speed):
        super().__init__(pos, PROJECTILES[weapon][0], PROJECTILES[weapon][1])
        self.g = PROJECTILES[weapon][2]
        self.speed_x = speed * math.cos(angle) + wind
        self.speed_y = speed * math.sin(angle)

    def move(self):
        super().move(self.speed_x, self.speed_y)
        self.speed_y -= self.g * 10

    def check_boom(self):
        pass
        # Проверка столкновения

    def boom(self):
        pass
        is_shot = False
        del shot
        # BOOM


pygame.init()
window: pygame.Surface = pygame.display.set_mode(RESOLUTION, FULLSCREEN)
pygame.display.set_caption('Gooks')
map1 = Map('map.txt', (0, 255, 0), (0, 0, 0))

# Создание гуков
gooks = []
for team in TEAMS:
    for gook in team:
        pos = random.choice(POSITIONS)
        POSITIONS.remove(pos)
        gooks.append(Gook(pos, gook))

map1.draw()

while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == KEYDOWN:
            if event.key == K_F1:
                if fullscreen:
                    window: pygame.Surface = pygame.display.set_mode(RESOLUTION)
                    fullscreen = False
                else:
                    window: pygame.Surface = pygame.display.set_mode(RESOLUTION, FULLSCREEN)
                    fullscreen = True
            if event.key == K_ESCAPE:
                is_working = False
            if event.key == K_SPACE:
                shot = ''
                next_turn()

    for gook in gooks:
        gook.draw()

    if is_shot:
        shot.draw()
        shot.move()
        if shot.check_boom():
            shot.boom()
           # next_turn()
        else:
            shot.draw()
    pygame.display.flip()