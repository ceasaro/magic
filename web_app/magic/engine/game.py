from random import shuffle

from magic.core.models.fields import ManaPool
from magic.engine.steps import cleanup
from magic.engine.steps import combat
from magic.engine.steps import draw
from magic.engine.steps import main_phase
from magic.engine.steps import untap
from magic.engine.steps import upkeep
from magic.core.models import Card


class Cards():

    def __init__(self, cards=None):
        super().__init__()
        self.cards = cards if cards else []

    def next(self):
        if self.cards:
            return self.cards[0]

    def add(self, card):
        assert isinstance(card, Card)
        self.cards.append(card)

    def remove(self, card):
        assert isinstance(card, Card)
        self.cards.remove(card)

    def count(self):
        return len(self.cards)

    def __contains__(self, card):
        return card in self.cards


class Deck(Cards):

    def shuffle(self):
        shuffle(self.cards)

    def add(self, card):
        super().add(card)
        self.shuffle()

    def draw(self):
        if self.cards:
            return self.cards.pop(0)


class Player():

    def __init__(self, name, library):
        super().__init__()
        self.name = name
        self.live = 20
        self.library = library if library else Deck()
        self.hand = Cards()
        for i in range(7):
            self.hand.add(library.draw())
        self.played_cards = Cards()
        self.graveyard = Deck()
        self.exiled = Deck()
        self.mana_pool = ManaPool()

    def turn(self):
        # Beginning Phase
        untap.step(self)
        upkeep.step()
        draw.step()

        # First Main Phase
        main_phase.step()

        # Combat Phase
        combat.start_combat_step()
        combat.declare_attackers_step()
        combat.declare_blockers_step()
        combat.combat_damage_step()
        combat.end_combat_step()

        # Second Main Phase
        main_phase.step()

        # End Phase
        cleanup.step()

    def play(self, card):
        if card in self.hand and self.mana_pool.pay(card.mana_cost):
            self.hand.remove(card)
            self.played_cards.add(card)
            self.mana_pool.add(card.mana_source)



# 1 The current player chooses the order that triggered abilities go on the stack.
# 2 Whenever a player recieves priority, the game checks for state-based effects first.


class Game(object):

    def __init__(self, players):
        super().__init__()
        self.players = players

    def round(self):
        for player in self.players:
            player.turn()