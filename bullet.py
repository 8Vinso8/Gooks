import math
import pygame
from thing import Thing
from locals import *


class Bullet(Thing):
    def __init__(self, bitmap, pos, weapon, angle, power, direction):
        super().__init__(bitmap, pos, PROJECTILES[weapon][0], PROJECTILES[weapon][1])
        if direction == 'left':
            self.flip_x()
        self.g = PROJECTILES[weapon][2] * G
        speed = PROJECTILES[weapon][3] * power
        self.wind = 0
        self.x_speed = speed * math.cos(angle)
        self.y_speed = speed * math.sin(angle)
        self.explosion = PROJECTILES[weapon][4]
        self.dmg = PROJECTILES[weapon][5]
        self.direction = direction
        self.timer = pygame.time.get_ticks()

    def move(self):
        last_pos = self.get_pos()
        super().move(round(self.x_speed), round(self.y_speed))
        self.y_speed += self.g
        return last_pos

    def get_dmg(self):
        return self.dmg

    def check_state(self, teams, cur_gook):
        if super().check_state():
            return super().check_state()
        if self.collision('left', self.x_speed) or self.collision('right', self.x_speed) \
                or self.collision('down', self.y_speed) or self.collision('up', self.y_speed):
            return 'BOOM'
        for team in teams:
            for gook in team.get_gooks():
                if pygame.Rect(
                        gook.get_pos(), gook.get_size()
                ).colliderect(
                        pygame.Rect(self.get_pos(), self.get_size())
                ) and gook != cur_gook:
                    return 'BOOM'
        # Проверка столкновения

    def boom(self, window):
        self.bitmap.explode(
            window,
            (self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2),
            self.explosion
        )
        return pygame.Rect(
            (self.get_x() + self.get_size()[0] // 2 - self.explosion,
             self.get_y() + self.get_size()[1] // 2 - self.explosion),
            (2 * self.explosion, 2 * self.explosion)
        )

    def change_wind(self, wind):
        self.x_speed = self.x_speed - self.wind + wind
        self.wind = wind
