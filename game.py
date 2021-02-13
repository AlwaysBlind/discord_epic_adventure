
class Game():
    active = False
    cat = "🐈"
    hero = "🤠"
    n = 15
    cat_pos = n-1
    hero_pos = 0
    field = []

    def start(self):
        self.active = True
        self.field = [" "]*self.n

    def update(self):
        self.cat_pos -= 1

    def draw(self):
        current_field = self.field.copy()
        current_field[self.cat_pos] = self.cat
        current_field[self.hero_pos] = self.hero
        msg = "".join(current_field)
        return msg


# g = Game()

# g.start()
# print(g.draw())
# g.update()
# print(g.draw())
# g.update()
# print(g.draw())
