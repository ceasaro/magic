import pytest

from magic.core.exception import MagicGameException, NoManaException


@pytest.mark.django_db
def test_play_land_card(player):
    assert player.hand.count() == 5
    assert player.played_cards.count() == 0
    assert str(player.mana_pool) == "0"
    forest = player.hand.get_by_name("Forest")
    player.play(forest)
    assert player.hand.count() == 4
    assert player.played_cards.count() == 1
    assert str(player.mana_pool) == "0"

    # no forest card already played can play it again
    with pytest.raises(MagicGameException):
        player.play(forest)
        assert (
            player.hand.count() == 3
        ), "no changes expectd casuse card was not in hand"
        assert (
            player.played_cards.count() == 1
        ), "no changes expectd casuse card was not in hand"
        assert (
            str(player.mana_pool) == "0"
        ), "no changes expectd casuse card was not in hand"


@pytest.mark.django_db
def test_play_creature_card(player):
    birds_of_paradise = player.hand.get_by_name("Birds of Paradise")
    with pytest.raises(NoManaException):
        player.play(birds_of_paradise)

    forest = player.hand.get_by_name("Forest")
    player.play(forest)
    with pytest.raises(NoManaException):
        # land card played but not tapped for mane
        player.play(birds_of_paradise)

    player.tap(forest)
    player.play(birds_of_paradise)
    assert forest in player.played_cards
    assert birds_of_paradise in player.played_cards
    assert str(player.mana_pool) == "0"
