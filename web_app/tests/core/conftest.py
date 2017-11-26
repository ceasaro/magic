import pytest
from django.contrib.auth.models import User

from magic.core.models import Player, Deck


@pytest.fixture
def user_admin():
    user = User.objects.create(username='admin', email='admin@magic.com')
    user.set_password('secret')
    user.is_superuser=True
    user.save()
    return user


@pytest.fixture
def player_cees():
    user = User.objects.create(username='cees', email='cees@magic.com')
    user.set_password('pwd')
    return Player.objects.create(user=user)


@pytest.fixture
def deck(card_library):
    deck = Deck.objects.create(name='test deck')
    for card in card_library.cards:
        deck.cards.add(card.card)
    return deck