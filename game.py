
from enum import Enum


class Game():
    active = False
    cat = "🐅"
    hero = "🤠"
    skull = "☠"
    MAX_TURNS_HIDDEN = 4
    n = 25
    inputs = []

    def start(self):
        self.state = State.HUNT
        self.active = True
        self.field = [" "]*self.n
        self.cat_pos = self.n - 1
        self.hero_pos = 7
        self.hero = "🤠"
        self.turns_hidden = 0

    def hide(self):
        self.inputs.append(State.HIDE)

    def update(self):
        if not self.active:
            return
        for inp in self.inputs:
            if inp == State.HIDE and self.turns_hidden < self.MAX_TURNS_HIDDEN:
                self.state = State.HIDE

        self.inputs.clear()
        if self.state == State.HIDE:
            if self.turns_hidden < self.MAX_TURNS_HIDDEN:
                self.turns_hidden += 1
            else:
                self.state = State.HUNT
        self.cat_pos -= 1
        if self.cat_pos == self.hero_pos and not self.state == State.HIDE:
            self.hero = self.skull
            self.state = State.DEAD
            self.active = False
        if self.cat_pos < 0:
            self.state = State.VICTORY
            self.active = False

    def draw(self):
        header = "\n"
        header2 = "\n"
        msg = ""
        if self.state == State.HUNT:
            header = "The fierce cat is coming closer." \
                "What are you going to do?"
            header2 = "Feed him, hide or use brutal violence (gun)"
        if self.state == State.DEAD:
            header = "Too bad. You died"
        if self.state == State.HIDE:
            header = "The cat is coming closer. What are you going to do?"
            header2 = "You hide. But for how long?"
        if self.state == State.VICTORY:
            header = "The cat has run past you"
            header2 = "You survive. But what have you gained?"

        current_field = self.field.copy()
        if (self.cat_pos >= 0):
            current_field[self.cat_pos] = self.cat

        if self.state == State.HIDE and self.cat_pos != self.hero_pos:
            current_field[self.hero_pos] = "🌴"
        else:
            current_field[self.hero_pos] = self.hero

        msg = "".join(current_field)
        return f'{header}\n{header2}\n{msg}'


class State(Enum):
    HUNT = 0,
    HIDE = 1,
    VICTORY = 2,
    RUN = 3,
    DEAD = 4,


# g = Game()

# g.start()
# print(g.draw())
# g.update()
# print(g.draw())
# g.update()
# print(g.draw())
