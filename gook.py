import pygame
from thing import Thing
import math
from locals import *
from graveyard import Graveyard
from bullet import Bullet


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
        self.hp = 100
        self.angle = 0
        self.move_img_delay = 0
        self.is_weapon = False
        self.holding = False

    def __str__(self):
        return self.name

    def draw(self, window):
        super().draw(window)
        font = pygame.font.Font(None, 30)
        hp_text = font.render(str(self.get_hp()), True, pygame.Color('green'))
        name_text = font.render(self.name, True, pygame.Color(self.color))
        window.blit(hp_text, [self.position[0], self.position[1] - 10])
        window.blit(name_text, [self.position[0], self.position[1] - 20])
        '''if self.is_weapon:
            self.weapon.draw()'''
        if self.holding:
            time = pygame.time.get_ticks() - self.start_ticks
            if time > 2700:
                time = 2700
            power = time / 2700
            pygame.draw.rect(window, (round(255 * power), round(255 * (1 - power)), 0),
                             pygame.Rect((self.position[0] + 1, self.position[1]), (self.size[0] * power - 1, 10)))

    def get_weapon(self):
        return self.weapon

    def get_hp(self):
        return self.hp

    def change_holding_status(self):
        self.holding = not self.holding
        if self.holding:
            self.start_ticks = pygame.time.get_ticks()

    def key_move(self, move):
        last_direction = self.direction
        last_pos = self.get_pos()
        if self.collision('down'):
            if move == 'D':
                self.x_speed = MOVEMENT_SPEED
                self.direction = 'right'
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
                self.direction = 'left'
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

        if self.direction != last_direction:
            self.flip_x()
        return last_pos

    def jump1(self):
        last_pos = self.get_pos()
        if self.collision('down'):
            if self.direction == 'left':
                self.change_speed((10, -20))
            else:
                self.change_speed((-10, -20))
        return last_pos

    def jump2(self):
        last_pos = self.get_pos()
        if self.collision('down'):
            if self.direction == 'left':
                self.change_speed((-20, -15))
            else:
                self.change_speed((20, -15))
        return last_pos

    def change_get_angle(self, final_cords):
        fin_x, fin_y = final_cords
        st_x, st_y = self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2
        self.angle = math.atan2((fin_y - st_y), (fin_x - st_x))
        return self.angle

    def shoot(self, final_cords, power):
        print(self.change_get_angle(final_cords))

        return Bullet(
            self.bitmap,
            (self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2),
            self.get_weapon(),
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
        return Graveyard(self.bitmap, self.get_pos(), GRAVEYARD_IMG, GRAVEYARD_RES)
