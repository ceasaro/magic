import json
import os

import pytest

from magic.core.models import Card
from magic.engine.game import Player, Game, Deck, Cards
from magic.im_export import mtgjson


@pytest.fixture()
def card_library():
    file_path = os.path.join(os.path.dirname(__file__), './data/mtgjson_set_1_com.json')
    mtgjson.import_sets(json.load(open(file_path, 'r')))
    library = Deck()
    [library.add(card) for card in Card.objects.all()]
    return library


@pytest.fixture()
def card_library_2():
    file_path = os.path.join(os.path.dirname(__file__), './data/mtgjson_set_1_com.json')
    mtgjson.import_sets(json.load(open(file_path, 'r')))
    library = Deck()
    [library.add(card) for card in Card.objects.all()]
    return library


@pytest.fixture()
def card_library_set_2():
    file_path = os.path.join(os.path.dirname(__file__), './data/mtgjson_set_2_com.json')
    mtgjson.import_sets(json.load(open(file_path, 'r')))
    library = Deck()
    [library.add(card) for card in Card.objects.all()]
    return library


@pytest.fixture()
def lea_forest_land(card_library):
    return Card.objects.get(set__code='LEA', name='Forest')


@pytest.fixture()
def lea_badlands_land(card_library):
    return Card.objects.get(set__code='LEA', name='Badlands')


@pytest.fixture()
def lea_birds_of_paradise_creature(card_library):
    return Card.objects.get(set__code='LEA', name='Birds of Paradise')


@pytest.fixture()
def lea_bad_moon_enchantment(card_library):
    return Card.objects.get(set__code='LEA', name='Bad Moon')


@pytest.fixture()
def lea_berserk_instance(card_library):
    return Card.objects.get(set__code='LEA', name='Berserk')


@pytest.fixture()
def player(card_library, lea_forest_land, lea_badlands_land, lea_birds_of_paradise_creature,
           lea_bad_moon_enchantment, lea_berserk_instance,
           ):
    player = Player("fixed", card_library)
    player.hand = Cards()
    player.hand.add(lea_forest_land)
    player.hand.add(lea_badlands_land)
    player.hand.add(lea_birds_of_paradise_creature)
    player.hand.add(lea_bad_moon_enchantment)
    player.hand.add(lea_berserk_instance)
    return player


@pytest.fixture()
def player_cees(card_library):
    return Player("cees", card_library)


@pytest.fixture()
def player_wes_lee(card_library_2):
    return Player("wes lee", card_library_2)


@pytest.fixture()
def game(player_wes_lee, player_cees):
    return Game([player_wes_lee, player_cees])
