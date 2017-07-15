import pytest


@pytest.mark.django_db
def test_game_setup_2_players(game):
    assert len(game.players) == 2
    assert game.players[0].library.count() == 42, "library start with 48 but 7 cards are drawn."
    assert game.players[0].hand.count() == 7
    assert game.players[0].live == 20
    assert game.players[1].hand.count() == 7
    assert game.players[1].live == 20


@pytest.mark.django_db
def test_play_land_card(player_fixed, lea_forest_card):
    assert player_fixed.hand.count() == 4
    assert player_fixed.played_cards.count() == 0
    assert str(player_fixed.mana_pool) == '0'
    player_fixed.play(lea_forest_card)
    assert player_fixed.hand.count() == 3
    assert player_fixed.played_cards.count() == 1
    assert str(player_fixed.mana_pool) == 'G'

    # no forest card in had nothing should happen
    player_fixed.play(lea_forest_card)
    assert player_fixed.hand.count() == 3, "no changes expectd casuse card was not in hand"
    assert player_fixed.played_cards.count() == 1, "no changes expectd casuse card was not in hand"
    assert str(player_fixed.mana_pool) == 'G', "no changes expectd casuse card was not in hand"

    # add extra forest cards to the hand
    player_fixed.hand.add(lea_forest_card)
    player_fixed.hand.add(lea_forest_card)
    # play extra cards
    player_fixed.play(lea_forest_card)
    player_fixed.play(lea_forest_card)
    assert player_fixed.hand.count() == 3
    assert player_fixed.played_cards.count() == 3
    assert str(player_fixed.mana_pool) == 'GGG'

