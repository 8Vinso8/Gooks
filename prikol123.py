def collision(self, direction):
    if direction == 'left':
        for i in range(self.pos[0] - 2, self.pos[0]):
            for j in range(self.pos[1], self.pos[1] + self.pl_size):
                if map[j][i]:
                    return True
    elif direction == 'right':
        for i in range(self.pos[0] + self.pl_size + 1, self.pos[0] + self.pl_size + 3):
            for j in range(self.pos[1], self.pos[1] + self.pl_size):
                if map[j][i]:
                    return True
    elif direction == 'up':
        for i in range(self.pos[0], self.pos[0] + self.pl_size):
            for j in range(self.pos[1] + 1, self.pos[1] + 3):
                if map[j][i]:
                    return True
    else:
        for i in range(self.pos[0], self.pos[0] + self.pl_size):
            for j in range(self.pos[1] + self.pl_size + 1, self.pos[1] + self.pl_size + 3):
                if map[j][i]:
                    return True
