import pytest

from magic.core.models import Card
from magic.engine.game import Player

@pytest.fixture()
def land_cards():
    Card

@pytest.fixture()
def player_1():
    return Player()