import pytest

from magic.core.models import Deck


@pytest.mark.django_db
def test_get_deck(api_client_cees, deck):
    response = api_client_cees.get("/api/decks/" + deck.name + "/").json()
    assert response["name"] == deck.name
    assert len(response["cards"]) == 49, "deck should contain 49 cards"
    keys = response["cards"][0]
    assert all(
        [key in keys for key in ["name", "external_id", "mana_cost", "image_url"]]
    )


@pytest.mark.django_db
def test_create_deck1(api_client_cees, card_library):
    card_ids = [c.external_id for c in card_library.cards[:2]]
    response = api_client_cees.post(
        "/api/decks/", {"name": "my first deck", "cards": card_ids}
    )
    assert response.status_code == 201
    assert all(
        [id in card_ids for id in response.json()["cards"]]
    ), "response must contain all card_ids"

    assert Deck.objects.count() == 1, "one deck should have been created"
    deck = Deck.objects.first()
    assert deck.name == "my first deck"
    assert len(deck.cards.all()) == 2, "Deck should contain two cards"


@pytest.mark.django_db
def test_create_deck_with_same_cards(api_client_cees, card_library):
    card_ids = [card_library.cards[0].external_id, card_library.cards[0].external_id]
    response = api_client_cees.post(
        "/api/decks/", {"name": "deck with same cards", "cards": card_ids}
    )
    assert response.status_code == 201
    deck = Deck.objects.first()
    assert len(deck.cards.all()) == 2, "Deck should contain two cards"


@pytest.mark.django_db
def test_create_deck_no_cards(api_client_cees):
    response = api_client_cees.post(
        "/api/decks/",
        {
            "name": "my first deck",
        },
    )
    assert response.status_code == 201

    assert Deck.objects.count() == 1, "one deck should have been created"
    deck = Deck.objects.first()
    assert deck.name == "my first deck"
    assert len(deck.cards.all()) == 0, "Deck should contain no cards"


@pytest.mark.django_db
def test_update_deck(api_client_cees, deck):
    assert deck.name == "test deck"
    assert len(deck.cards.all()) == 49, "Deck should contain 49 cards"
    response = api_client_cees.put(
        "/api/decks/{}/".format(deck.name),
        {
            "name": deck.name,
            "cards": [c.card.external_id for c in deck.cards.all()[:2]],
        },
    )

    assert response.status_code == 200
    deck = Deck.objects.get(id=deck.id)
    assert len(deck.cards.all()) == 2, "Deck should contain two cards"


@pytest.mark.django_db
def test_update_deck_name(api_client_cees, deck):
    assert deck.name == "test deck"
    assert len(deck.cards.all()) == 49, "Deck should contain two cards"
    response = api_client_cees.put(
        "/api/decks/{}/".format(deck.name),
        {
            "name": "changed named",
            "cards": [c.card.external_id for c in deck.cards.all()[:2]],
        },
    )

    assert response.status_code == 200
    deck = Deck.objects.get(id=deck.id)
    assert deck.name == "changed named"
    assert len(deck.cards.all()) == 2, "Deck should contain two cards"
