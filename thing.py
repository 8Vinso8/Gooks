from functions import *


class Thing:
    def __init__(self, bitmap, pos, image, size):
        self.bitmap = bitmap
        self.position = pos
        self.size = size
        self.image_name = image
        self.image = load_image(image, colorkey=-1)
        self.x_speed = 0
        self.y_speed = 0

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.position

    def get_image_name(self):
        return self.image_name

    def change_speed(self, change):  # change - кортеж изменения скорости (x, y)
        self.x_speed += change[0]
        self.y_speed += change[1]

    def change_image(self, image):
        self.image = load_image(image, colorkey=-1)
        self.image_name = image

    def change_size(self, size):
        self.size = size

    def get_rect(self):
        return pygame.Rect(self.get_x(), self.get_y(), self.get_size()[0], self.get_size()[1])

    def check_state(self):
        if self.get_x() >= RESOLUTION[0] or \
                self.get_y() >= RESOLUTION[1] or \
                self.get_x() + self.get_size()[0] < 0:
            return 'delete'

    def flip_x(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, window):
        self.rect = self.image.get_rect(
            bottomright=(self.get_pos()[0] + self.get_size()[0],
                         self.get_pos()[1] + self.get_size()[1])
        )
        window.blit(self.image, self.rect)

    def move(self, x, y):
        self.position = (self.get_x() + x, self.get_y() + y)

    def passive_move(self):
        changed = False
        last_pos = self.position
        self.change_speed((0, G))
        if self.x_speed > 0:
            collision_check = self.collision('right', self.x_speed)
            if collision_check:
                self.x_speed = collision_check - self.get_x() - self.size[0]
        elif self.x_speed < 0:
            collision_check = self.collision('left', self.x_speed)
            if collision_check:
                self.x_speed = collision_check - self.get_x()
        if self.y_speed > 0:
            collision_check = self.collision('down', self.y_speed)
            if collision_check:
                self.y_speed = collision_check - self.get_y() - self.size[1]
        elif self.y_speed < 0:
            collision_check = self.collision('up', self.y_speed)
            if collision_check:
                self.y_speed = self.get_y() - collision_check - 1
        if self.x_speed or self.y_speed:
            self.move(self.x_speed, self.y_speed)
            changed = True
        if self.x_speed > 0:
            self.x_speed -= self.speed_decrease
            if self.x_speed < 0:
                self.x_speed = 0
        if self.x_speed < 0:
            self.x_speed += self.speed_decrease
            if self.x_speed > 0:
                self.x_speed = 0
        if changed:
            return last_pos

    def collision(self, direction, speed=1, kx=0, ky=0):
        if direction == 'left':
            for i in range(round(self.get_pos()[0]) - kx, round(self.get_pos()[0] - speed) - kx):
                for j in range(round(self.get_pos()[1]) - ky, round(self.get_pos()[1] + self.get_size()[1]) - ky):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return i
                    except IndexError:
                        continue
        if direction == 'right':
            for i in range(round(self.get_pos()[0] + self.get_size()[0]) + kx,
                           round(self.get_pos()[0] + self.get_size()[0] + speed) + kx):
                for j in range(round(self.get_pos()[1]) - ky, round(self.get_pos()[1] + self.get_size()[1]) - ky):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return i
                    except IndexError:
                        continue
        if direction == 'up':
            for j in range(round(self.get_pos()[1]) - 1, round(self.get_pos()[1] - speed) - 1):
                for i in range(round(self.get_pos()[0]), round(self.get_pos()[0] + self.get_size()[0])):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return j
                    except IndexError:
                        continue
        if direction == 'down':
            for j in range(round(self.get_pos()[1] + self.get_size()[1]),
                           round(self.get_pos()[1] + self.get_size()[1] + speed)):
                for i in range(round(self.get_pos()[0]), round(self.get_pos()[0] + self.get_size()[0])):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return j
                    except IndexError:
                        continue
