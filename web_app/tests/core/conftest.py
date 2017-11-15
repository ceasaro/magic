import pytest
from django.contrib.auth.models import User

from magic.core.models import Player, Deck


@pytest.fixture
def player_cees():
    user = User.objects.create(username='cees', email='cees@magic.com')
    return Player.objects.create(user=user)


@pytest.fixture
def deck(card_library):
    deck = Deck.objects.create(name='test deck')
    for card in card_library.cards:
        deck.cards.add(card.card)
    return deck