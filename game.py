from enum import Enum
import character


class Game():
    active = False
    skull = "☠️"
    MAX_TURNS_HIDDEN = 3
    n = 16
    inputs = []
    MEAT_KEY = 'meat'

    def start(self):
        self.characters = dict()
        self.hero = character.Hero(4)
        self.cat = character.Tiger(self.n-1)
        self.state = State.HUNT
        self.active = True
        self.gamefield = self.get_game_field()
        self.turns_hidden = 0
        self.characters["hero"] = self.hero
        self.characters["cat"] = self.cat
        self.header = "\n"
        self.header2 = "\n"
        self.state_dict = {State.HUNT: self.handle_state_HUNT,
                           State.HIDE: self.handle_state_HIDE,
                           State.VICTORY_HIDE: self.handle_state_VICTORY_HIDE,
                           State.RUN: self.handle_state_RUN,
                           State.DEAD: self.handle_state_DEAD,
                           State.VICTORY_RUN: self.handle_state_VICTORY_RUN,
                           State.GUN: self.handle_state_GUN,
                           State.FEED: self.handle_state_FEED,
                           State.WELLFED: self.handle_state_WELLFED,
                           }
        self.handle_state_HUNT()
        self.update_game_field()

    def get_game_field(self):
        # field = ["🌴"]*self.n
        field = ["⠀"]*self.n
        field.append("⁢⛰️")
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
        self.gamefield = self.get_game_field()
        self.handle_input()

        for char in self.characters.values():
            if char is not None:
                char.update()

        self.handle_state()
        self.update_game_field()

    def update_game_field(self):
        sorted_chars = sorted(self.characters.values(),
                              key=lambda x: x.priority, reverse=True)
        for char in sorted_chars:
            if char is not None:
                if char.pos >= 0:
                    self.gamefield[char.pos] = char.image

    def handle_state_VICTORY_RUN(self):
        self.header = "You outran the cat"
        self.header2 = "You survive. Do you always run away from your fears?"

    def handle_state_VICTORY_HIDE(self):
        self.header = "The cat has run past you"
        self.header2 = "You survive. But a coward you remain"

    def handle_state_RUN(self):
        self.header = "The cat is still running towards you"
        self.header2 = "You try to outrun it"

    def handle_state_HIDE(self):
        if self.turns_hidden > self.MAX_TURNS_HIDDEN:
            self.hero.image = self.hero.base_image
            self.header = "Your disguise breaks."
            self.header2 = "You are now visible"
        else:
            self.turns_hidden += 1
            self.header = "The cat is coming closer."
            self.header2 = "You hide behind a tree. But for how long?"
            self.hero.image = "🌴"

    def handle_state_DEAD(self):
        self.header = "The cat ate you"
        self.header2 = "You are now dead. Too bad"

    def handle_state_WELLFED(self):
        self.header = "The cat eats the meat."
        self.header2 = "It is now your friend forever"
        self.gamefield = ["💖" for x in self.gamefield]

    def handle_state_GUN(self):
        self.header = "You shot the cat. It stops breathing"
        self.header2 = "The majestic animal is dead. Why did you do this?"
        self.cat.image = "️💀"

    def is_hiding(self):
        return (self.state == State.HIDE and
                self.turns_hidden <= self.MAX_TURNS_HIDDEN)

    def handle_state(self):
        if self.cat.pos == self.hero.pos:
            if not self.is_hiding():
                self.hero.image = self.skull
                self.state = State.DEAD
                self.active = False
        if self.cat.pos < 0:
            self.state = State.VICTORY_HIDE
            self.active = False
        if self.hero.pos < 0:
            self.state = State.VICTORY_RUN
            self.active = False
        self.state_dict[self.state]()

    def handle_state_FEED(self):
        meat = self.characters.get(self.MEAT_KEY)
        if meat is not None and meat.pos == self.cat.pos:
            self.state = State.WELLFED
            self.characters.pop(self.MEAT_KEY)
            self.active = False
            self.handle_state()
            return
        self.header = "The fierce cat is coming closer."
        self.header2 = "You lay out a chunk of meat."

    def handle_state_HUNT(self):
        self.header = "The fierce cat is coming closer." \
            "What are you going to do? You can only choose one action"
        self.header2 = "Feed him, hide or use brutal violence (gun)"

    def handle_input(self):
        if self.hero.number_of_actions > 0:
            return
        if len(self.inputs) > 0:
            inp = self.inputs[0]
            if inp == State.HIDE:
                self.state = State.HIDE
            elif inp == State.RUN:
                self.hero.speed = 1
                self.state = State.RUN
            elif inp == State.GUN:
                self.state = State.GUN
                self.active = False
            elif inp == State.FEED:
                self.characters[self.MEAT_KEY] = character.Meat(
                    self.hero.pos+1)
                self.state = State.FEED
            self.hero.number_of_actions += 1
            self.inputs.clear()

    def draw(self):
        msg = "".join(self.gamefield)
        return f'{self.header}\n{self.header2}\n{msg}'


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
