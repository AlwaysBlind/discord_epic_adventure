import random


class Character:
    def __init__(self, pos, image, speed, priority):
        self.pos = pos
        self.image = image
        self.speed = speed
        self.priority = priority


class Tiger(Character):
    def __init__(self, n):
        super().__init__(pos=n, image="🐅", speed=1, priority=1)

    def update(self):
        self.pos -= self.speed


class Hero(Character):
    base_image = "🤠"

    def __init__(self, n):
        super().__init__(pos=n, image=self.base_image, speed=0, priority=2)
        self.number_of_actions = 0

    def update(self):
        if (random.uniform(0, 1) > 0.6):
            self.pos -= self.speed


class Meat(Character):
    def __init__(self, n):
        super().__init__(pos=n, image="🍖", speed=0, priority=3)

    def update(self):
        pass
