import pytest

from magic.core.models import Card
from magic.core.models.fields import Mana


@pytest.mark.django_db
def test_card():
    card = Card.objects.create(
        external_id="1435987",
        name="my card",
        mana_cost=Mana(red=1, blue=12),
        _power="1",
        _toughness="2",
    )
    assert card.name == "my card"
    assert card.external_id, "id should have been generated"
    assert str(card.mana_cost) == "UUUUUUUUUUUUR"


@pytest.mark.django_db
def test_search_cards(card_library, card_library_set_2):
    assert (
        Card.objects.get(name="Braingeyser")
        == Card.objects.search(u="UU", q="brain")[0]
    )
    assert Card.objects.search(g="GG").count() == 2
    assert (
        Card.objects.search(b="GG").count() == 0
    ), "b is black not green mana no results expected"
    assert Card.objects.search(g="gg").count() == Card.objects.search(g="GG").count()
    assert (
        Card.objects.search(sets="Limited Edition Alpha 2").count() == 2
    ), "set LEA_2 should have 2 cards, bout found {}.".format(
        Card.objects.search(sets="LEA_2").count()
    )


@pytest.mark.django_db
def test_search_cards_by_type(card_library):
    assert Card.objects.search(card_types="Land").count() == 4
    assert (
        Card.objects.search(
            card_types=[
                "Forest",
            ]
        ).count()
        == 2
    )
    assert Card.objects.search(card_types=["Land", "Forest"]).count() == 2
    assert Card.objects.search(card_types=["Basic", "Forest"]).count() == 1
    assert (
        Card.objects.search(card_types=["Atog", "Legendary", "Creature"]).count() == 1
    )
