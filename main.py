import pygame
import math
from pygame.constants import *
from locals import *
import random
import itertools
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_next_team():
    for team_now in teams:
        yield team_now


team_gen = get_next_team()
gook_gen = itertools.cycle(range(TEAM_LEN))
n_gook = next(gook_gen)


def next_turn():
    global cur_team, cur_gook, team_gen, n_gook
    try:
        cur_team = next(team_gen)
        cur_gook = cur_team.get_gook(n_gook)
    except StopIteration:
        n_gook = next(gook_gen)
        team_gen = get_next_team()
        cur_team = next(team_gen)
        cur_gook = cur_team.get_gook(n_gook)
    print(cur_team, cur_gook)


def optimised_draw(moved_gooks, bullets, bitmap, window):  # Bitmap заменить на название переменной карты
    # Закрашивание прошлых позиций
    for gook in moved_gooks:
        bitmap.draw_part(window, gook.get_last_pos(), gook.get_size())
    for bullet in bullets:
        bitmap.draw_part(window, bullet.get_last_pos(), bullet.get_size())
    # отрисовка объектов
    for gook in moved_gooks:
        gook.draw(window)
    for bullet in bullets:
        bullet.draw(window)


def collision(self, direction):
    if direction == 'left':
        for i in range(self.get_pos()[0] - 2, self.get_pos()[0]):
            for j in range(self.get_pos()[1], self.get_pos()[1] + self.get_size()[1]):
                if map1.get_bitmap()[j][i]:
                    return True
    elif direction == 'right':
        for i in range(self.get_pos()[0] + self.get_size()[0] + 1, self.get_pos()[0] + self.get_size()[0] + 3):
            for j in range(self.get_pos()[1], self.get_pos()[1] + self.get_size()[1]):
                if map1.get_bitmap()[j][i]:
                    return True
    elif direction == 'up':
        for i in range(self.get_pos()[0], self.get_pos()[0] + self.get_size()[0]):
            for j in range(self.get_pos()[1] + 1, self.get_pos()[1] + 3):
                if map1.get_bitmap()[j][i]:
                    return True
    else:
        for i in range(self.get_pos()[0], self.get_pos()[0] + self.get_size()[0]):
            for j in range(self.get_pos()[1] + self.get_size()[1] + 1, self.get_pos()[1] + self.get_size()[1] + 3):
                if map1.get_bitmap()[j][i]:
                    return True
    return False


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

    def get_bitmap(self):
        return self.bitmap


class Thing:
    def __init__(self, pos, image, res):
        self.position = pos
        self.resolution = res
        self.image = load_image(image)

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_rect(self):
        return pygame.Rect(self.get_x(), self.get_y(), self.resolution[0], self.resolution[1])

    def draw(self):
        self.image_rect = self.image.get_rect(
            bottomright=(self.position[0] + self.resolution[0],
                         self.position[1] + self.resolution[1])
        )
        window.blit(self.image, self.image_rect)

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)


class Bullet(Thing):
    def __init__(self, pos, weapon, angle, speed):
        super().__init__(pos, PROJECTILES[weapon][0], PROJECTILES[weapon][1])
        self.g = PROJECTILES[weapon][2] * G
        self.speed_x = speed * math.cos(angle) + wind
        self.speed_y = speed * math.sin(angle)

    def move(self):
        super().move(self.speed_x, self.speed_y)
        self.speed_y -= self.g * 10

    def check_boom(self):
        pass
        # Проверка столкновения

    def boom(self):
        pass  # Взрыв снаряда


class Gook:
    def __init__(self, position, color, name, size, start_image):
        self.name = name
        self.color = color
        self.position = position
        self.size = size  # size - кортеж из двух элементов (x, y)

        self.x_speed = 0  # Только для перемещения без участия игрока!
        self.y_speed = 0
        self.speed_decrease = 5  # Замедление

        self.last_pos = position  # Для оптимизации отрисовки битмапа

        self.image = load_image(start_image, colorkey=-1)

    def get_size(self):
        return self.size

    def get_last_pos(self):
        return self.last_pos

    def change_image(self, image):
        self.image = load_image(image)

    def draw(self, window):
        self.image_rect = self.image.get_rect(
            bottomright=(self.get_pos()[0] + self.get_size()[0],
                         self.get_pos()[1] + self.get_size()[1])
        )
        window.blit(self.image, self.image_rect)

    def change_speed(self, change):  # change - кортеж изменения скорости (x, y)
        self.x_speed += change[0]
        self.y_speed += change[1]

    def get_pos(self):
        return self.position

    def key_move(self, move):
        self.last_pos = self.position
        if move == 'D':
            self.x_speed = 5
        else:
            self.x_speed = -5

        if self.x_speed > 0:
            if collision(self, 'right'):
                self.x_speed = 0
            else:
                self.position = self.position[0] + self.x_speed, self.position[1]
        else:
            if collision(self, 'left'):
                self.x_speed = 0
            else:
                self.position = self.position[0] + self.x_speed, self.position[1]
        self.x_speed = 0

    def passive_move(self):
        changed = False
        last_pos = self.position
        self.change_speed((0, G))
        if self.x_speed:
            if self.x_speed > 0:
                if collision(self, 'right'):
                    self.x_speed = 0
                else:
                    self.position = self.position[0] + self.x_speed, self.position[1]
                    self.x_speed -= self.speed_decrease
                    if self.x_speed < 0:
                        self.x_speed = 0
                        changed = True
            else:
                if collision(self, 'left'):
                    self.x_speed = 0
                else:
                    self.position = self.position[0] + self.x_speed, self.position[1]
                    self.x_speed += self.speed_decrease
                    if self.x_speed > 0:
                        self.x_speed = 0
                    changed = True

        if self.y_speed:
            if self.y_speed > 0:
                if collision(self, 'down'):
                    self.x_speed = 0
                else:
                    self.position = self.position[0], self.position[1] + self.y_speed
                    self.y_speed -= self.speed_decrease
                    if self.y_speed < 0:
                        self.y_speed = 0
                    changed = True
            else:
                if collision(self, 'up'):
                    self.y_speed = 0
                else:
                    self.position = self.position[0], self.position[1] + self.y_speed
                    self.y_speed += self.speed_decrease
                    if self.y_speed > 0:
                        self.y_speed = 0
                changed = True

        if changed:
            self.last_pos = last_pos

        return changed


class Team:
    def __init__(self, team_name, team_color, positions, names):
        self.gooks = list()
        print(positions, names)
        for i in range(TEAM_LEN):
            self.gooks.append(Gook(positions[i], team_color, names[i], GOOK_RES, GOOK_IMG))
        self.team_name = team_name

    def get_gook(self, n):
        return self.gooks[n % len(self.gooks)] if self.gooks else None

    def get_gooks(self):
        return self.gooks


pygame.init()
window: pygame.Surface = pygame.display.set_mode(RESOLUTION, FULLSCREEN)
pygame.display.set_caption('Gooks')

for team in TEAMS:
    teams.append(Team(*team))

map1 = Map('map.txt', (0, 255, 0), (0, 0, 0))
map1.draw()
next_turn()
for team in teams:
    for gook in team.get_gooks():
        gook.draw(window)

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
                next_turn()
                pass  # Выстрел тут зафигачить
            if event.key == K_d:
                print(cur_gook)
                cur_gook.key_move('D')
            if event.key == K_a:
                cur_gook.key_move('A')

    for team in teams:
        for gook in team.get_gooks():
            if gook.passive_move():
                moved_gooks.append(gook)
    optimised_draw(moved_gooks, bullets, map1, window)
    moved_gooks.clear()
    bullets.clear()
    pygame.display.flip()