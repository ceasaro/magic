from random import shuffle

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


class CardStack(Cards):

    def shuffle(self):
        self.cards = shuffle(self.cards)

    def add(self, card):
        super().add(card)
        self.shuffle()

    def draw(self):
        if self.cards:
            return self.cards.pop(0)


class BattleField():
    pass


class Player():

    def __init__(self):
        super().__init__()
        hand = Cards()
        library = CardStack()
        played_cards = Cards()
        graveyard = CardStack()
        exiled = CardStack()


def untap_step():
    """
    1) "At Beginning of Turn" and "At Beginning of Untap Step" triggered abilities trigger, but they do not go on the
    stack until the beginning of the Upkeep Step.
    2) Phasing happens. All phased out cards phase in and all cards with Phasing which are in play phase out simultaneously.
    3) Current player untaps all permanents he controls.
    :return:
    """
    pass


def upkeep_step():
    """
    1) "At Beginning of Turn", "At Beginning of Untap Step", and "At Beginning of Upkeep" triggered abilities trigger. 1
    2) The current player gets priority to play instants and activated abilities. 2
    :return:
    """
    pass


def draw_stop():
    """
    1) The current player draws a card. This special action doesn't use the stack.
    2) "At Beginning of Draw Step" triggered abilities trigger. 1
    3) The current player gets priority to play instants and activated abilities. 2
    4) Check for Mana Burn.
    :return:
    """
    pass


def main_phase():
    """
    1) "At Beginning of Main Phase" triggered abilities trigger. 1
    2) The current player gets priority to play instants and activated abilities. 2
    3) When the stack is empty, the current player may play lands, creatures, and sorceries.
    4) Check for Mana Burn.
    :return:
    """
    pass


def start_combat_step():
    """
    1) "At Beginning of Combat" triggered abilities trigger. 1
    2) The current player gets priority to play instants and activated abilities. 2
    :return:
    """
    pass


def declare_attackers_step():
    """
    1) The current player declares his attackers. If no attackers are declared, then skip the rest of this step,
    the Declare Blockers step, and the Combat Damage step. Go directly to the End of Combat step.
    2) Triggered abilities that trigger off attackers being declared trigger at this point. 1
    3) The current player gets priority to play instants and activated abilities. 2
    :return:
    """
    pass


def declare_blockers_step():
    """
    1) The defending player declares his blockers and which attacking creatures they will block.
    2) Triggered abilities that trigger off blockers being declared trigger at this point. 1
    3) The current player gets priority to play instants and activated abilities. 2
    :return:
    """
    pass


def combat_damage_step():
    """
    ! First Strike Combat Damage !
    1) If no attacking or blocking creatures have First Strike, then skip this entire section.
    2) The current player announces how the attacking creatures that have First Strike will deal their damage.
    3) The defending player announces how the blocking creatures that have First Strike will deal their damage.
    4) All combat damage from creatures with First Strike goes on the stack as a single unit.
    5) The current player gets priority to play instants and activated abilities. 2
    6) After all spells and abilities have resolved, combat damage from creatures with First Strike resolves and is dealt simultaneously to each creature as it was originally assigned.
    7) "Deals Combat Damage" and "Is Dealt Combat Damage" triggered abilities trigger. 1
    8) The current player gets priority to play instants and activated abilities. 2

    9) The current player announces how the attacking creatures without First Strike will deal their damage.
    10) The defending player announces how the blocking creatures without First Strike will deal their damage.
    11) All combat damage from creatures without First Strike goes on the stack as a single unit.
    12) The current player gets priority to play instants and activated abilities. 2
    13) After all spells and abilities have resolved, combat damage from creatures without First Strike resolves and is dealt simultaneously to each creature as it was originally assigned.
    14) "Deals Combat Damage" and "Is Dealt Combat Damage" triggered abilities trigger. 1
    15) The current player gets priority to play instants and activated abilities. 2
    :return:
    """
    pass


def end_combat_step():
    """
    1) "Until End of Combat" effects end.
    2) "At End of Combat" triggered abilities trigger. 1
    3) The current player gets priority to play instants and activated abilities. 2
    4) Check for Mana Burn.
    :return:
    """
    pass


def cleanup_step():
    """
    1) The current player discards down to his maximum hand size (usually seven).
    2) Simultaneously remove all damage from permanents and end all "Until End of Turn" effects.
    3) Check for state-based effects.
    4) Any triggered abilities that have triggered since the beginning of the Cleanup Step are placed on the stack. 1
    5) If any state-based effects were resolved or if any triggered abilities were put on the stack, then the current player gets priority to play instants and activated abilities. If this occurs, then once the stack is empty, rather than going to the next turn, a new Cleanup Step begins. This loop continues until there is a Cleanup Step in which no state-based effects are resolved and no triggered abilities are placed on the stack.
    6) Check for Mana Burn.
    :return:
    """
    pass

# 1 The current player chooses the order that triggered abilities go on the stack.
# 2 Whenever a player recieves priority, the game checks for state-based effects first.


class Game():
    players = []

    def turn(self, player):
        # Beginning Phase
        untap_step()
        upkeep_step()
        draw_stop()

        # First Main Phase
        main_phase()

        # Combat Phase
        start_combat_step()
        declare_attackers_step()
        declare_blockers_step()
        combat_damage_step()
        end_combat_step()

        # Second Main Phase
        main_phase()

        # End Phase
        cleanup_step()