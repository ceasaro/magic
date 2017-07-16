from . import land_types, creature_types


class CardTypes(object):
    # Supertypes
    BASIC = 'Basic'
    LEGENDARY = 'Legendary'
    SNOW = 'Snow'
    WORLD = 'World'
    SUPERTYPES = [BASIC, LEGENDARY, SNOW, WORLD]

    # Permanents
    CLUE = 'Clue'
    CONTRAPTION = 'Contraption'
    EQUIPMENT = 'Equipment'
    FORTIFICATION = 'Fortification'
    ARTIFACT = [CLUE, CONTRAPTION, EQUIPMENT, FORTIFICATION]

    CREATURE = 'Creature'
    CREATURES = [creature for creature in dir(creature_types) if not creature.startswith('__')]

    AURA = 'Aura'
    CURSE = 'Curse'
    SHRINE = 'Shrine'
    ENCHANTMENT = [AURA, CURSE, SHRINE]

    LAND = 'Land'
    LANDS = [land_type for land_type in dir(land_types) if not land_type.startswith('__')]

    PLANESWALKER = 'Planeswalker'  # subtypes
    # import pdb; pdb.set_trace()
    PERMANENTS = ARTIFACT + [CREATURE] + ENCHANTMENT + LANDS + [PLANESWALKER]

    # Nonpermanents
    INSTANT = 'Instant'
    SORCERY = 'Sorcery'
    ARCANE = 'Arcane'
    TRAP = 'Trap'
    NON_PERMANENTS = [INSTANT, SORCERY, ARCANE, TRAP]

    ALL_TYPES = SUPERTYPES + PERMANENTS + NON_PERMANENTS

    type_choises = [(t, t) for t in ALL_TYPES]
