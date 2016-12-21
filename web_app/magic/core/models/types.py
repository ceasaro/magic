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

    CREATURE = [creature for creature in dir(creature_types) if not creature.startswith('__')]

    AURA = 'Aura'
    CURSE = 'Curse'
    SHRINE = 'Shrine'
    ENCHANTMENT = [AURA, CURSE, SHRINE]

    LAND = [land_type for land_type in dir(land_types) if not land_type.startswith('__')]

    PLANESWALKER = 'Planeswalker'  # subtypes
    # import pdb; pdb.set_trace()
    PERMANENTS = ARTIFACT + CREATURE + ENCHANTMENT + LAND + [PLANESWALKER]

    # Nonpermanents
    INSTANT = 'Instant'
    SORCERY = 'Sorcery'
    ARCANE = 'Arcane'
    TRAP = 'Trap'
    NON_PERMANENTS = [INSTANT, SORCERY, ARCANE, TRAP]

    ALL_TYPES = SUPERTYPES + PERMANENTS + NON_PERMANENTS

    type_choises = [(t, t) for t in ALL_TYPES]

    def is_supertype(self, card_type):
        return card_type in self.SUPERTYPES

    def is_permanent(self, card_type):
        return card_type in self.PERMANENTS

    def is_non_permanent(self, card_type):
        return card_type in self.NON_PERMANENTS

    def is_artifact(self, card_type):
        return card_type in self.ARTIFACT

    def is_creature(self, card_type):
        return card_type in self.CREATURE

    def is_enchantment(self, card_type):
        return card_type in self.ENCHANTMENT

    def is_land(self, card_type):
        return card_type in self.LAND

    def is_planes_walker(self, card_type):
        return card_type in self.PLANESWALKER
