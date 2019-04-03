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
        deck.add_card(card.card)
    return deck


@pytest.fixture
def decks(deck, card_library):
    deck2 = Deck.objects.create(name='test deck2')
    deck3 = Deck.objects.create(name='my special set')
    return [deck, deck2, deck3]
