class Medicine(Thing):
    def __init__(self, bitmap, position, start_image, size):
        super().__init__(bitmap, position, start_image, size)
        self.heal = 40

    def get_heal(self):
        return self.heal