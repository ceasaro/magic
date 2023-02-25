import pytest

from magic.core.models import Card, CardTypes, LandTypes
from magic.core.models import creature_types


@pytest.mark.django_db
def test_import_mtgjson(card_library):
    assert card_library.count() == 49

    plateau_card = Card.objects.get(name="Plateau")
    assert plateau_card.name == "Plateau"
    assert CardTypes.LAND in plateau_card.types
    assert LandTypes.MOUNTAIN in plateau_card.subtypes
    assert LandTypes.PLAINS in plateau_card.subtypes
    assert plateau_card.type_line == "Land — Mountain Plains"
    assert plateau_card.text == "({T}: Add {R} or {W} to your mana pool.)"
    assert str(plateau_card.mana_cost) == "0"
    assert str(plateau_card.mana_source) == "WR"
    assert plateau_card.power == 0
    assert plateau_card.toughness == 0

    atogatog_card = Card.objects.get(name="Atogatog")
    assert atogatog_card.name == "Atogatog"
    assert CardTypes.CREATURE in atogatog_card.types
    assert creature_types.ATOG in atogatog_card.subtypes
    assert CardTypes.LEGENDARY in atogatog_card._supertypes
    assert atogatog_card.type_line == "Legendary Creature — Atog"
    assert (
        atogatog_card.text
        == "Sacrifice an Atog creature: Atogatog gets +X/+X until end of turn, where X is the sacrificed creature's power."
    )
    assert str(atogatog_card.mana_cost) == "WUBRG"
    assert str(atogatog_card.mana_source) == "0"
    assert atogatog_card.power == 5
    assert atogatog_card.toughness == 5
    assert atogatog_card.cmc == 5

    assquatch_card = Card.objects.get(name="Assquatch")
    assert assquatch_card.power == 3.5
    assert assquatch_card.toughness == 3.5

    vile_aggregate_card = Card.objects.get(name="Vile Aggregate")
    assert vile_aggregate_card.power == "*"
    assert vile_aggregate_card.toughness == 5
