text = "_x________"


class Game():
    cat = "🐈"
    hero = "🐸"
    n = 10
    cat_pos = n-1
    hero_pos = 0
    field = []

    def start(self):
        self.field = ["_"]*self.n

    def update(self):
        self.cat_pos -= 1

    def draw(self):
        current_field = self.field.copy()
        current_field[self.cat_pos] = self.cat
        current_field[self.hero_pos] = self.hero
        msg = "".join(current_field)
        return msg


g = Game()

g.start()
print(g.draw())
g.update()
print(g.draw())
g.update()
print(g.draw())
//todo https: // github.com/Rapptz/discord.py/blob/async/examples/background_task.py
