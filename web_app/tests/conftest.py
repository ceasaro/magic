import json
import os

import pytest

from magic.core.models import Card, Set
from magic.engine.game import Player, Game, Deck, Cards
from magic.im_export import mtgjson


@pytest.fixture()
def card_library():
    file_path = os.path.join(os.path.dirname(__file__), './data/mtgjson_sets_com.json')
    mtgjson.import_sets(json.load(open(file_path, 'r')))
    library = Deck()
    [library.add(card) for card in Card.objects.all()]
    return library


@pytest.fixture()
def card_library_2():
    file_path = os.path.join(os.path.dirname(__file__), './data/mtgjson_sets_com.json')
    mtgjson.import_sets(json.load(open(file_path, 'r')))
    library = Deck()
    [library.add(card) for card in Card.objects.all()]
    return library


@pytest.fixture()
def lea_forest_card(card_library):
    return Card.objects.get(set__code='LEA', name='Forest')


@pytest.fixture()
def lea_badlands_card(card_library):
    return Card.objects.get(set__code='LEA', name='Badlands')


@pytest.fixture()
def lea_bad_moon_card(card_library):
    return Card.objects.get(set__code='LEA', name='Bad Moon')


@pytest.fixture()
def lea_berserk_card(card_library):
    return Card.objects.get(set__code='LEA', name='Berserk')


@pytest.fixture()
def player_fixed(card_library, lea_forest_card, lea_badlands_card, lea_bad_moon_card, lea_berserk_card):
    player = Player("fixed", card_library)
    player.hand = Cards()
    player.hand.add(lea_forest_card)
    player.hand.add(lea_badlands_card)
    player.hand.add(lea_bad_moon_card)
    player.hand.add(lea_berserk_card)
    return player


@pytest.fixture()
def player_cees(card_library):
    return Player("cees", card_library)


@pytest.fixture()
def player_wes_lee(card_library_2):
    return Player("wes lee", card_library_2)


@pytest.fixture()
def game(player_wes_lee, player_cees    ):
    return Game([player_wes_lee, player_cees])