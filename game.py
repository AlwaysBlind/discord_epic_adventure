
class Game():
    active = False
    cat = "🐅"
    hero = "🤠"
    skull = "☠" 
    MAX_TURNS_HIDDEN = 4
    n = 15
    inputs = []

    def start(self):
        self.state = "hunt"
        self.active = True
        self.field = [" "]*self.n
        self.cat_pos = self.n - 1
        self.hero_pos = 0
        self.hero = "🤠"
        self.turns_hidden = 0
    def hide(self):
        self.inputs.append("hide")

    def update(self):
        if self.active == False:
            return
        for inp in self.inputs:
            if inp == "hide" and self.turns_hidden < self.MAX_TURNS_HIDDEN:
                self.state = "hide"
        self.inputs.clear()
        if self.state == "hide":
            if self.turns_hidden < self.MAX_TURNS_HIDDEN:
                self.turns_hidden += 1
            else:
                self.state = "hunt"
        self.cat_pos -= 1
        if self.cat_pos == self.hero_pos and not self.state == "hide" :
            self.hero = self.skull
            self.state = "dead"
            self.active = False
        if self.cat_pos < 0:
            self.state = "victory"
            self.active = False

    def draw(self):
        header = "\n"
        header2 = "\n"
        msg = ""
        if self.state == "hunt":
            header = "The fierce cat is coming closer. What are you going to do?"
            header2 = "Feed him, hide or use brutal violence (gun)"
        if self.state == "dead":
            header = "Too bad. You died"
        if self.state == "hide":
            header = "The cat is coming closer. What are you going to do?"
            header2 = "You hide. But for how long?"
        if self.state == "victory":
            header = "The cat has run past you"
            header2 = "You survive, but what have you gained?"

        current_field = self.field.copy()
        if (self.cat_pos >= 0):
            current_field[self.cat_pos] = self.cat
        if self.state == "hide":
            if self.cat_pos != self.hero_pos:
                current_field[self.hero_pos] = "🌴"
        else:
            current_field[self.hero_pos] = self.hero
        msg = "".join(current_field)
        return f'{header}\n{header2}\n{msg}'

# g = Game()

# g.start()
# print(g.draw())
# g.update()
# print(g.draw())
# g.update()
# print(g.draw())
