class WindIndicator:
    def __init__(self, position):
        self.position = position
        self.positive_wind = list()
        self.negative_wind = list()
        self.zero_wind = load_image('windbox.png')
        for i in range(1, 6):
            self.positive_wind.append(load_image(f'windbox{str(i)}.png'))
        for j in range(1, 6):
            self.negative_wind.append(load_image(f'windbox{str(j * -1)}.png'))

    def get_image(self, wind_num):
        if not wind_num:
            return self.zero_wind
        elif wind_num > 0:
            return self.positive_wind[wind_num - 1]
        else:
            return self.negative_wind[wind_num * -1 - 1]

    def get_pos(self):
        return self.position