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


class Map:
    def __init__(self, map_file, color_zero, color_one):
        self.bitmap = list()
        self.color_zero = color_zero
        self.color_one = color_one
        self.load_map_file(map_file)

    def load_map_file(self, map_file):
        fullname = os.path.join('data', map_file)
        with open(fullname, 'r') as f:
            for line in f.readlines():
                line_list = list(map(int, list(line.strip())))
                self.bitmap.append(line_list)
        print(self.bitmap)

    def draw(self, window):
        for i in range(1920):
            for j in range(1080):
                window.set_at((i, j), self.color_one if self.bitmap[j][i] else self.color_zero)

    def draw_part(self, window, start, size):
        start = tuple(map(int, start))
        for i in range(start[0], start[0] + size[0]):
            for j in range(start[1], start[1] + size[1]):
                try:
                    window.set_at((i, j), self.color_one if self.bitmap[j][i] else self.color_zero)
                except IndexError:
                    continue
                # Поменять цвета местами если баги

    def explode(self, window, point, size):
        for i in range(point[0] - size, point[0] + size):
            for j in range(point[1] - size, point[1] + size):
                try:
                    self.bitmap[j][i] = 0
                    window.set_at((i, j), self.color_one if self.bitmap[j][i] else self.color_zero)
                except IndexError:
                    continue

    def get_bitmap(self):
        return self.bitmap


class Thing:
    def __init__(self, bitmap, pos, image, size):
        self.bitmap = bitmap
        self.position = pos
        self.size = size
        self.image = load_image(image, colorkey=-1)
        self.last_pos = pos

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.position

    def get_last_pos(self):
        return self.last_pos

    def get_rect(self):
        return pygame.Rect(self.get_x(), self.get_y(), self.get_size()[0], self.get_size()[1])

    def draw(self, window):
        self.rect = self.image.get_rect(
            bottomright=(self.get_pos()[0] + self.get_size()[0],
                         self.get_pos()[1] + self.get_size()[1])
        )
        window.blit(self.image, self.rect)

    def move(self, x, y):
        self.last_pos = self.get_pos()
        self.position = (self.get_x() + x, self.get_y() + y)

    def collision(self, direction):
        if direction == 'left':
            for i in range(int(self.get_pos()[0]) - 2, int(self.get_pos()[0])):
                for j in range(int(self.get_pos()[1]), int(self.get_pos()[1] + self.get_size()[1])):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return True
                    except IndexError:
                        continue
        elif direction == 'right':
            for i in range(int(self.get_pos()[0] + self.get_size()[0]) + 1,
                           int(self.get_pos()[0] + self.get_size()[0]) + 3):
                for j in range(int(self.get_pos()[1]), int(self.get_pos()[1] + self.get_size()[1])):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return True
                    except IndexError:
                        continue
        elif direction == 'up':
            for i in range(int(self.get_pos()[0]), int(self.get_pos()[0] + self.get_size()[0])):
                for j in range(int(self.get_pos()[1]) + 1, int(self.get_pos()[1]) + 3):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return True
                    except IndexError:
                        continue
        else:
            for i in range(int(self.get_pos()[0]), int(self.get_pos()[0] + self.get_size()[0])):
                for j in range(int(self.get_pos()[1] + self.get_size()[1]) + 1,
                               int(self.get_pos()[1] + self.get_size()[1]) + 3):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return True
                    except IndexError:
                        continue
        return False


class Bullet(Thing):
    def __init__(self, bitmap, pos, weapon, angle, power):
        super().__init__(bitmap, pos, PROJECTILES[weapon][0], PROJECTILES[weapon][1])
        self.g = PROJECTILES[weapon][2] * G
        speed = PROJECTILES[weapon][3] * power
        self.speed_x = speed * math.cos(angle) + wind
        self.speed_y = speed * math.sin(angle)
        self.explosion = PROJECTILES[weapon][4]

    def move(self):
        super().move(int(self.speed_x), int(self.speed_y))
        self.speed_y += self.g

    def check_boom(self):
        if self.get_x() + self.get_size()[0] >= RESOLUTION[0] or \
                self.get_y() + self.get_size()[1] >= RESOLUTION[1] or \
                self.get_x() < 0 or \
                self.get_y() < 0:
            return 'delete'
        if self.collision('left') or self.collision('right') \
                or self.collision('down') or self.collision('up'):
            return 'BOOM'
        # Проверка столкновения

    def boom(self, window):
        self.bitmap.explode(
            window,
            (self.get_x() + self.get_size()[0], self.get_y() + self.get_size()[1]),
            self.explosion
        )


class Gook(Thing):
    def __init__(self, bitmap, position, color, name, size, start_image, weapon='cannon'):
        super().__init__(bitmap, position, start_image, size)
        self.name = name
        self.color = color
        self.weapon = weapon
        self.direction = 'right'
        self.x_speed = 0  # Только для перемещения без участия игрока!
        self.y_speed = 0
        self.speed_decrease = 0.5  # Замедление

        self.image = load_image(start_image, colorkey=-1)

    def get_weapon(self):
        return self.weapon

    def change_image(self, image):
        self.image = load_image(image, colorkey=-1)

    def change_speed(self, change):  # change - кортеж изменения скорости (x, y)
        self.x_speed += change[0]
        self.y_speed += change[1]

    def key_move(self, move):
        last_direction = self.direction
        self.last_pos = self.get_pos()
        if self.collision('down'):
            if move == 'D':
                self.x_speed = 5
                self.direction = 'right'
            else:
                self.x_speed = -5
                self.direction = 'left'

        if self.x_speed > 0:
            if self.collision('right'):
                self.x_speed = 0

        elif self.x_speed < 0:
            if self.collision('left'):
                self.x_speed = 0

        self.move(self.x_speed, self.y_speed)

        self.x_speed = 0

        if self.direction != last_direction:
            print(self.direction, last_direction)
            self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        if self.collision('down'):
            if self.direction == 'left':
                self.change_speed((10, -20))
            else:
                self.change_speed((-10, -20))

    def passive_move(self):
        changed = False
        last_pos = self.position
        self.change_speed((0, G))
        if self.x_speed > 0:
            if self.collision('right'):
                self.x_speed = 0
            else:
                self.position = self.position[0] + self.x_speed, self.position[1]
                self.x_speed -= self.speed_decrease
                if self.x_speed < 0:
                    self.x_speed *= -0.5
                changed = True
        elif self.x_speed < 0:
            if self.collision('left'):
                self.x_speed *= -0.5
            else:
                self.position = self.position[0] + self.x_speed, self.position[1]
                self.x_speed += self.speed_decrease
                if self.x_speed > 0:
                    self.x_speed = 0
                changed = True

        if self.y_speed > 0:
            if self.collision('down'):
                self.y_speed = 0
            else:
                self.position = self.position[0], self.position[1] + self.y_speed
                if self.y_speed < 0:
                    self.y_speed = 0
                changed = True
        elif self.y_speed < 0:
            if self.collision('up'):
                self.y_speed = 0
            else:
                self.position = self.position[0], self.position[1] + self.y_speed
                if self.y_speed > 0:
                    self.y_speed = 0
            changed = True

        if changed:
            self.last_pos = last_pos

        return changed

    def shoot(self, final_cords, power):
        fin_x, fin_y = final_cords
        st_x, st_y = self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2
        angle = math.atan2((fin_y - st_y), (fin_x - st_x))
        return Bullet(
            self.bitmap,
            (self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2),
            self.get_weapon(),
            angle,
            power
        )


class Team:
    def __init__(self, bitmap, team_name, team_color, positions, names):
        self.gooks = list()
        print(positions, names)
        for i in range(TEAM_LEN):
            self.gooks.append(Gook(bitmap, positions[i], team_color, names[i], GOOK_RES, GOOK_IMG))
        self.team_name = team_name

    def get_gook(self, n):
        return self.gooks[n % len(self.gooks)] if self.gooks else None

    def get_gooks(self):
        return self.gooks


def main():
    is_working = True
    fullscreen = True
    is_shot = False
    is_mouse_down = False
    is_jumped = False

    pygame.init()
    window: pygame.Surface = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
    pygame.display.set_caption('Gooks')

    clock = pygame.time.Clock()

    map1 = Map('map.txt', (0, 255, 0), (0, 0, 0))
    map1.draw(window)

    for team in TEAMS:
        teams.append(Team(map1, *team))

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
                    is_jumped = True
                    cur_gook.jump()
                    moved_gooks.append(cur_gook)

            if not is_mouse_down and event.type == MOUSEBUTTONDOWN:
                start_ticks = pygame.time.get_ticks()
                is_mouse_down = True
            if is_mouse_down and event.type == MOUSEBUTTONUP:
                time = pygame.time.get_ticks() - start_ticks
                if time > 2700:
                    time = 2700
                power = time / 3000 + 0.1
                bullets.append(cur_gook.shoot(event.pos, power))
                print(power)
                is_mouse_down = False

        if not is_jumped:
            keys = pygame.key.get_pressed()
            if keys[K_a]:
                cur_gook.key_move('A')
                moved_gooks.append(cur_gook)
            if keys[K_d]:
                cur_gook.key_move('D')
                moved_gooks.append(cur_gook)
        if cur_gook.collision('down'):
            is_jumped = False

        for team in teams:
            for gook in team.get_gooks():
                if gook.passive_move():
                    moved_gooks.append(gook)

        for bullet in bullets:
            bullet.move()
            state = bullet.check_boom()
            if state == 'BOOM':
                bullet.boom(window)
            if state:
                map1.draw_part(window, bullet.get_last_pos(), bullet.get_size())
                bullets.remove(bullet)

        optimised_draw(moved_gooks, bullets, map1, window)
        cur_gook.draw(window)
        moved_gooks.clear()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()