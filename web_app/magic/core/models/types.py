from . import creature_types


class LandTypes(object):
    PLAINS = "Plains"
    ISLAND = "Island"
    SWAMP = "Swamp"
    MOUNTAIN = "Mountain"
    FOREST = "Forest"
    DESERT = "Desert"
    GATE = "Gate"
    LAIR = "Lair"
    LOCUS = "Locus"
    MINE = "Mine"
    POWER_PLANT = "Power-Plant"
    TOWER = "Tower"
    URZA_S = "Urza's"

    ALL = [
        PLAINS,
        ISLAND,
        SWAMP,
        MOUNTAIN,
        FOREST,
        DESERT,
        GATE,
        LAIR,
        LOCUS,
        MINE,
        POWER_PLANT,
        TOWER,
        URZA_S,
    ]


class CardTypes(object):
    # Supertypes
    BASIC = "Basic"
    LEGENDARY = "Legendary"
    SNOW = "Snow"
    WORLD = "World"
    SUPERTYPES = [BASIC, LEGENDARY, SNOW, WORLD]

    # Permanents
    CLUE = "Clue"
    CONTRAPTION = "Contraption"
    EQUIPMENT = "Equipment"
    FORTIFICATION = "Fortification"
    ARTIFACT = [CLUE, CONTRAPTION, EQUIPMENT, FORTIFICATION]

    CREATURE = "Creature"
    CREATURES = [
        creature for creature in dir(creature_types) if not creature.startswith("__")
    ]

    AURA = "Aura"
    CURSE = "Curse"
    SHRINE = "Shrine"
    ENCHANTMENT = [AURA, CURSE, SHRINE]

    LAND = "Land"
    LANDS = LandTypes.ALL

    PLANESWALKER = "Planeswalker"  # subtypes
    # import pdb; pdb.set_trace()
    PERMANENTS = ARTIFACT + [CREATURE] + ENCHANTMENT + LANDS + [PLANESWALKER]

    # Nonpermanents
    INSTANT = "Instant"
    SORCERY = "Sorcery"
    ARCANE = "Arcane"
    TRAP = "Trap"
    NON_PERMANENTS = [INSTANT, SORCERY, ARCANE, TRAP]

    ALL_TYPES = SUPERTYPES + PERMANENTS + NON_PERMANENTS

    type_choises = [(t, t) for t in ALL_TYPES]
