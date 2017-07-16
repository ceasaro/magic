import pytest

from magic.core.exception import MagicGameException


@pytest.mark.django_db
def test_tap_land_card(player, lea_forest_land):
    forest_card_1 = player.hand.get_by_name("Forest")
    player.play(forest_card_1)
    player.tap(forest_card_1)
    assert player.hand.count() == 4
    assert player.played_cards.count() == 1
    assert str(player.mana_pool) == 'G'

    assert player.hand.get_by_name("Forest") is None, "no forest card should be found"

    # extra forest card
    player.hand.add(lea_forest_land)
    forest_2 = player.hand.get_by_name("Forest")
    player.play(forest_2)
    player.tap(forest_2)

    assert player.hand.count() == 4
    assert player.played_cards.count() == 2
    assert str(player.mana_pool) == 'GG'

    player.tap(forest_2)
    assert str(player.mana_pool) == 'GG', 'tapping again should not add extra mana'


@pytest.mark.django_db
def test_tap_creature_card(player):
    birds_of_paradise = player.hand.get_by_name("Birds of Paradise")
    forest = player.hand.get_by_name("Forest")
    player.play(forest)
    player.tap(forest)
    player.play(birds_of_paradise)
    player.tap(birds_of_paradise)
    assert birds_of_paradise in player.attacking_creatures, "expected 'Birds of Paradise' in attacking cards"
