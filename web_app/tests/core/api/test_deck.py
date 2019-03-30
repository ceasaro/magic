import pytest

from magic.core.models import Deck


@pytest.mark.django_db
def test_create_deck(api_client_cees, card_library):
    response = api_client_cees.post('/api/decks/', {'name': 'my first deck',
                                                    'cards': [c.external_id for c in card_library.cards[:2]]})
    assert response.status_code == 201

    assert Deck.objects.count() == 1, "one deck should have been created"
    deck = Deck.objects.first()
    assert deck.name == 'my first deck'
    assert len(deck.cards.all()) == 2, "Deck should contain two cards"


@pytest.mark.django_db
def test_create_deck_no_cards(api_client_cees):
    response = api_client_cees.post('/api/decks/', {'name': 'my first deck',})
    assert response.status_code == 201

    assert Deck.objects.count() == 1, "one deck should have been created"
    deck = Deck.objects.first()
    assert deck.name == 'my first deck'
    assert len(deck.cards.all()) == 0, "Deck should contain no cards"


@pytest.mark.django_db
def test_update_deck(api_client_cees, deck):
    assert deck.name == 'test deck'
    assert len(deck.cards.all()) == 49, "Deck should contain two cards"
    response = api_client_cees.put('/api/decks/{}/'.format(deck.name),
                                   {'name': 'changed named',
                                    'cards': [c.external_id for c in deck.cards.all()[:2]]})

    assert response.status_code == 200
    deck = Deck.objects.get(id=deck.id)
    assert deck.name == 'changed named'
    assert len(deck.cards.all()) == 2, "Deck should contain two cards"
