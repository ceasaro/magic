from random import shuffle

from magic.core.exception import MagicGameException
from magic.core.models import Card
from magic.core.models.fields import ManaPool
from magic.engine.steps import cleanup
from magic.engine.steps import combat
from magic.engine.steps import draw
from magic.engine.steps import main_phase
from magic.engine.steps import untap
from magic.engine.steps import upkeep


class CardState(object):
    def __init__(self, card):
        assert isinstance(card, Card)
        self.card = card
        self.tapped = False
        self._power_pm = 0  # power plus or minus
        self._toughness_pm = 0  # toughness plus or minus

    @property
    def power(self):
        return self.card.power + self._power_pm

    @property
    def toughness(self):
        return self.card.toughness + self._toughness_pm

    def __getattr__(self, name: str):
        return self.card.__getattribute__(name)

    def __repr__(self):
        return "{} ({}): CardState".format(self.name, self.set)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return isinstance(other, CardState) and other.external_id == self.external_id


class Cards():
    def __init__(self, cards=None):
        super().__init__()
        self.cards = cards if cards else []

    def next(self):
        if self.cards:
            return self.cards[0]

    def get(self, id):
        try:
            return filter(lambda x: x.external_id == id, self.cards).__next__()
        except StopIteration:
            return None

    def get_by_name(self, name, set_name=None):
        try:
            return filter(lambda x: x.name == name and set_name is None or x.set.name == set_name,
                          self.cards).__next__()
        except StopIteration:
            return None

    def add(self, card):
        assert isinstance(card, (Card, CardState))
        self.cards.append(card if isinstance(card, CardState) else CardState(card))

    def remove(self, card):
        assert isinstance(card, (Card, CardState))
        self.cards.remove(card if isinstance(card, CardState) else CardState(card))

    def count(self):
        return len(self.cards)

    def __contains__(self, card):
        card_state = card if isinstance(card, CardState) else CardState(card)
        return card_state in self.cards


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
        else:
            raise MagicGameException("can't play the card: {}".format(card))

    def tap(self, card):
        if not card.tapped:
            card.tapped = True
            self.mana_pool.add(card.mana_source)

    def untap(self, card):
        if card.tapped:
            card.tapped = False


# 1 The current player chooses the order that triggered abilities go on the stack.
# 2 Whenever a player recieves priority, the game checks for state-based effects first.


class Game(object):
    def __init__(self, players):
        super().__init__()
        self.players = players

    def round(self):
        for player in self.players:
            player.turn()
