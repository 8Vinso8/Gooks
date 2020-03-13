import pygame
from thing import Thing
import math
from locals import *
from gravestone import Gravestone
from bullet import Bullet
from weapon import Weapon
import itertools


class Gook(Thing):
    def __init__(self, bitmap, position, color, name, size, start_image, weapon='cannon'):
        super().__init__(bitmap, position, start_image, size)
        self.name = name
        self.color = color
        self.direction = 'right'
        self.x_speed = 0  # Только для перемещения без участия игрока!
        self.y_speed = 0
        self.speed_decrease = 0.5  # Замедление
        self.hp = 100
        self.angle = 0
        self.move_img_delay = 0
        self.is_weapon = False
        self.holding = False
        self.weapon = Weapon(bitmap, position, *WEAPONS[weapon], self.direction, self.angle)
        self.weapon_gen = itertools.cycle(self.get_next_weapon())
        self.weapon_name = next(self.weapon_gen)

    def __str__(self):
        return self.name

    def draw(self, window):
        super().draw(window)
        font = pygame.font.Font(None, 30)
        hp_text = font.render(str(self.get_hp()), True, pygame.Color('green'))
        name_text = font.render(self.name, True, pygame.Color(self.color))
        window.blit(hp_text, [self.position[0], self.position[1] - 10])
        window.blit(name_text, [self.position[0], self.position[1] - 25])
        if self.is_weapon:
            self.weapon.draw(window)

    def get_weapon(self):
        return self.weapon

    def get_weapon_name(self):
        return self.weapon_name

    def get_hp(self):
        return self.hp

    def get_next_weapon(self):
        for weapon_now in WEAPONS:
            yield weapon_now

    def get_place_for_filling(self, pos, res):
        return ((pos[0], pos[1] - 20),
                (res[0] + 30, res[1] + 20))

    def change_direction(self, direction):
        if self.direction != direction:
            self.flip_x()
            self.weapon.flip_x()
        self.direction = direction
        self.get_weapon().direction = direction

    def change_weapon(self):
        self.weapon_name = next(self.weapon_gen)
        self.weapon = Weapon(self.bitmap, self.position, *WEAPONS[self.weapon_name], self.direction, self.angle)

    def key_move(self, move):
        last_pos = self.get_pos()
        if self.collision('down'):
            if move == 'D':
                self.x_speed = MOVEMENT_SPEED
                self.change_direction('right')
                collision_check = self.collision('right', self.x_speed)
                if collision_check:
                    self.x_speed = collision_check - self.get_x() - self.size[0]
                    if self.x_speed == 0:
                        for i in range(1, 20):
                            collision_check = self.collision('right', kx=1, ky=i)
                            if not collision_check:
                                self.move(1, -i)
                                break
            else:
                self.x_speed = -MOVEMENT_SPEED
                self.change_direction('left')
                collision_check = self.collision('left', self.x_speed)
                if collision_check:
                    self.x_speed = collision_check - self.get_x()
                    if self.x_speed == 0:
                        for i in range(1, 20):
                            collision_check = self.collision('left', kx=1, ky=i, speed=-1)
                            if not collision_check:
                                self.move(-1, -i)
                                break

        self.move(self.x_speed, 0)

        self.x_speed = 0

        return last_pos

    def jump1(self):
        last_pos = self.get_pos()
        if self.collision('down'):
            self.move(-10, -20)
            if self.direction == 'left':
                self.change_speed((10, -20))
            else:
                self.change_speed((-10, -20))
        return last_pos

    def jump2(self):
        last_pos = self.get_pos()
        if self.collision('down'):
            self.move(15, -15)
            if self.direction == 'left':
                self.change_speed((-20, -15))
            else:
                self.change_speed((20, -15))
        return last_pos

    def change_get_angle(self, final_cords):
        fin_x, fin_y = final_cords
        st_x, st_y = self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2
        self.angle = math.atan2((fin_y - st_y), (fin_x - st_x))
        '''self.weapon.rotate(self.angle)'''
        return self.angle

    def shoot(self, final_cords, power):
        self.change_get_angle(final_cords)
        return Bullet(
            self.bitmap,
            (self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2),
            self.weapon_name,
            self.angle,
            power,
            self.direction
        )

    def change_image_state(self, image):
        super().change_image(image)
        if self.direction == 'left':
            self.flip_x()

    def change_move_image(self):
        if self.move_img_delay > 5:
            if self.image_name == MOVE2_IMG:
                self.change_image_state(MOVE1_IMG)
            else:
                self.change_image_state(MOVE2_IMG)
            self.move_img_delay = 0
        else:
            self.move_img_delay += 1

    def make_damage(self, dmg):
        self.hp -= dmg

    def check_state(self):
        if super().check_state() or not self.check_is_alive():
            return 'del'

    def check_is_alive(self):
        return self.get_hp() > 0

    def make_graveyard(self):
        return Gravestone(self.bitmap, self.get_pos(), GRAVESTONE_IMG, GRAVESTONE_RES)
