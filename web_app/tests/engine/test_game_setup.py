import pytest


@pytest.mark.django_db
def test_game_setup_2_players(game):
    assert len(game.players) == 2
    assert (
        game.players[0].library.count() == 42
    ), "library start with 48 but 7 cards are drawn."
    assert game.players[0].hand.count() == 7
    assert game.players[0].live == 20
    assert game.players[1].hand.count() == 7
    assert game.players[1].live == 20
