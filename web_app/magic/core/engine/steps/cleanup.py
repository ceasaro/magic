def step():
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
