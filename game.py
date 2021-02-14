from enum import Enum
import character


class Game():
    active = False
    skull = "☠"
    MAX_TURNS_HIDDEN = 4
    n = 25
    inputs = []

    def start(self):
        self.hero = character.Hero(7)
        self.cat = character.Tiger(self.n-1)
        self.state = State.HUNT
        self.active = True
        self.field = self.get_game_field()
        self.turns_hidden = 0

    def get_game_field(self):
        self.field = [" "]*self.n
        self.field[0] = "⁢"
        self.field.append("⁢")

    def hide(self):
        self.inputs.append(State.HIDE)

    def update(self):
        if not self.active:
            return
        self.handle_input()

        if self.state == State.HIDE:
            if self.turns_hidden < self.MAX_TURNS_HIDDEN:
                self.turns_hidden += 1
            else:
                self.state = State.HUNT
        self.cat.pos -= self.cat.speed
        self.hero.pos -= self.hero.speed
        if self.cat.pos == self.hero.pos and not self.state == State.HIDE:
            self.hero.image = self.skull
            self.state = State.DEAD
            self.active = False
        if self.cat.pos < 0:
            self.state = State.VICTORY_HIDE
            self.active = False
        if self.hero.pos < 0:
            self.state = State.VICTORY_RUN
            self.active = False

    def handle_input(self):
        if self.hero.number_of_actions > 0:
            return
        for inp in self.inputs:
            if inp == State.HIDE and self.turns_hidden < self.MAX_TURNS_HIDDEN:
                self.state = State.HIDE
            elif inp == State.HUNT:
                self.state = State.HIDE
        self.inputs.clear()

    def draw(self):
        header = "\n"
        header2 = "\n"
        msg = ""
        if self.state == State.HUNT:
            header = "The fierce cat is coming closer." \
                "What are you going to do?"
            header2 = "Feed him, hide or use brutal violence (gun)"
        if self.state == State.DEAD:
            header = "The cat ate you"
            header2 = "You are now dead. Too bad"
        if self.state == State.HIDE:
            header = "The cat is coming closer. What are you going to do?"
            header2 = "You hide. But for how long?"
        if self.state == State.VICTORY_HIDE:
            header = "The cat has run past you"
            header2 = "You survive. But a coward you remain?"
        if self.state == State.VICTORY_RUN:
            header = "You outran the cat"
            header2 = "You survive. Will you always outrun your fears?"

        current_field = self.field.copy()
        if (self.cat.pos >= 0):
            current_field[self.cat.pos] = self.cat.image

        if self.state == State.HIDE and self.cat.pos != self.hero.pos:
            current_field[self.hero.pos] = "🌴"
        else:
            current_field[self.hero.pos] = self.hero.image

        msg = "".join(current_field)
        return f'{header}\n{header2}\n{msg}'


class State(Enum):
    HUNT = 0,
    HIDE = 1,
    VICTORY_HIDE = 2,
    RUN = 3,
    DEAD = 4,
    VICTORY_RUN = 5,


# g = Game()

# g.start()
# print(g.draw())
# g.update()
# print(g.draw())
# g.update()
# print(g.draw())
