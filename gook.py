class Gook:
    def __init__(self, position, color, name, size, start_image):
        self.name = name
        self.color = color
        self.position = position
        self.size = size  # size - кортеж из двух элементов (x, y)
        self.cur_image = start_image

        self.key_move = 5  # скорось при движении с помощью клавишь

        self.x_speed = 0  # Только для перемещения без участия игрока!
        self.y_speed = 0
        self.speed_decrease = 5  # Замедление

        self.last_pos = position  # Для оптимизации отрисовки битмапа

    def get_size(self):
        return self.size

    def get_last_pos(self):
        return self.last_pos

    def change_image(self, image):
        self.cur_image = image

    def draw(self, window):
        window.blit(self.cur_image, self.position)

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


def collision(self, direction):
    if direction == 'left':
        for i in range(self.pos[0] - 2, self.pos[0]):
            for j in range(self.pos[1], self.pos[1] + self.pl_size):
                if bitmap[j][i]:
                    return True
    elif direction == 'right':
        for i in range(self.pos[0] + self.pl_size + 1, self.pos[0] + self.pl_size + 3):
            for j in range(self.pos[1], self.pos[1] + self.pl_size):
                if bitmap[j][i]:
                    return True
    elif direction == 'up':
        for i in range(self.pos[0], self.pos[0] + self.pl_size):
            for j in range(self.pos[1] + 1, self.pos[1] + 3):
                if bitmap[j][i]:
                    return True
    else:
        for i in range(self.pos[0], self.pos[0] + self.pl_size):
            for j in range(self.pos[1] + self.pl_size + 1, self.pos[1] + self.pl_size + 3):
                if bitmap[j][i]:
                    return True
    return False
