import json
import os

import pytest

from magic.core.models import Card, land_types
from magic.core.models import creature_types
from magic.im_export import mtgjson

@pytest.mark.django_db
def test_import_mtgjson():
    file_path = os.path.join(os.path.dirname(__file__), './data/mtgjson_com.json')
    mtgjson.import_cards(json.load(open(file_path,  'r')))
    assert len(Card.objects.all()) == 5

    plateau_card = Card.objects.get(name='Plateau')
    assert plateau_card.name == 'Plateau'
    assert land_types.MOUNTAIN in plateau_card.types
    assert land_types.PLAINS in plateau_card.types
    assert plateau_card.type_line == "Land — Mountain Plains"
    assert plateau_card.text == "({T}: Add {R} or {W} to your mana pool.)"
    assert str(plateau_card.mana_cost) == '0'
    assert str(plateau_card.mana_source) == 'WR'
    assert plateau_card.power == 0
    assert plateau_card.toughness == 0

    atogatog_card = Card.objects.get(name='Atogatog')
    assert atogatog_card.name == 'Atogatog'
    assert creature_types.ATOG in atogatog_card.types
    assert atogatog_card.type_line == "Legendary Creature — Atog"
    assert atogatog_card.text == "Sacrifice an Atog creature: Atogatog gets +X/+X until end of turn, where X is the sacrificed creature's power."
    assert str(atogatog_card.mana_cost) == 'WUBRG'
    assert str(atogatog_card.mana_source) == '0'
    assert atogatog_card.power == 5
    assert atogatog_card.toughness == 5
