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
