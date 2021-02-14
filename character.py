class Character:
    def __init__(self, pos, image, speed):
        self.pos = pos
        self.image = image
        self.speed = speed


class Tiger(Character):
    def __init__(self, n):
        super().__init__(pos=n, image="🐅", speed=1)


class Hero(Character):
    def __init__(self, n):
        super().__init__(pos=n, image="🤠", speed=0)
        self.number_of_actions = 0
