from enum import Enum
import character


class Game():
    active = False
    skull = "☠️"
    MAX_TURNS_HIDDEN = 4
    n = 25
    inputs = []

    def start(self):
        self.characters = []
        self.hero = character.Hero(7)
        self.cat = character.Tiger(self.n-1)
        self.meat = None
        self.state = State.HUNT
        self.active = True
        self.field = self.get_game_field()
        self.turns_hidden = 0
        self.characters.append(self.hero)
        self.characters.append(self.cat)

    def get_game_field(self):
        field = [" "]*self.n
        field[0] = "⁢"
        field.append("⁢")
        return field

    def hide(self):
        self.inputs.append(State.HIDE)

    def run(self):
        self.inputs.append(State.RUN)

    def gun(self):
        self.inputs.append(State.GUN)

    def feed(self):
        self.inputs.append(State.FEED)

    def update(self):
        if not self.active:
            return
        self.handle_input()

        if self.state == State.HIDE:
            if self.turns_hidden < self.MAX_TURNS_HIDDEN:
                self.turns_hidden += 1
            else:
                self.state = State.HUNT
        for char in self.characters:
            char.update()

        if self.meat and self.meat.pos == self.cat.pos:
            self.state = State.WELLFED
            self.meat = None
            self.active = False
            return

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
        if len(self.inputs) > 0:
            inp = self.inputs[0]
            if inp == State.HIDE and self.turns_hidden < self.MAX_TURNS_HIDDEN:
                self.state = State.HIDE
            elif inp == State.RUN:
                self.hero.speed = 1
            elif inp == State.GUN:
                self.state = State.GUN
                self.active = False
            elif inp == State.FEED:
                self.meat = character.Meat(self.hero.pos+1)
            self.hero.number_of_actions += 1
            self.inputs.clear()

    def draw(self):
        header = "\n"
        header2 = "\n"
        msg = ""
        if self.state == State.HUNT:
            header = "The fierce cat is coming closer." \
                "What are you going to do? Choose carefully"
            header2 = "Feed him, hide or use brutal violence (gun)"
        if self.state == State.GUN:
            header = "You shot the cat. It stops breathing"
            header2 = "The majestic animal is dead. Why did you do this?"
            self.cat.image = "️💀"
        if self.state == State.WELLFED:
            header = "The cat eats the meat."
            header2 = "It is now your friend forever"
        if self.state == State.DEAD:
            header = "The cat ate you"
            header2 = "You are now dead. Too bad"
        if self.state == State.HIDE:
            header = "The cat is coming closer. What are you going to do?"
            header2 = "You hide. But for how long?"
        if self.state == State.VICTORY_HIDE:
            header = "The cat has run past you"
            header2 = "You survive. But a coward you remain"
        if self.state == State.VICTORY_RUN:
            header = "You outran the cat"
            header2 = "You survive. Will you always outrun your fears?"

        current_field = self.field.copy()
        if self.state == State.WELLFED:
            current_field = ["💖" for x in current_field]
        if self.meat:
            current_field[self.meat.pos] = self.meat.image

        if self.state == State.HIDE:
            if self.cat.pos != self.hero.pos:
                current_field[self.hero.pos] = "🌴"
        else:
            current_field[self.hero.pos] = self.hero.image

        if (self.cat.pos >= 0):
            current_field[self.cat.pos] = self.cat.image

        msg = "".join(current_field)
        return f'{header}\n{header2}\n{msg}'


class State(Enum):
    HUNT = 0,
    HIDE = 1,
    VICTORY_HIDE = 2,
    RUN = 3,
    DEAD = 4,
    VICTORY_RUN = 5,
    GUN = 6,
    FEED = 7,
    WELLFED = 8,
