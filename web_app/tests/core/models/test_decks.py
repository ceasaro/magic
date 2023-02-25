import pytest

from magic.core.models import Deck


@pytest.mark.parametrize(
    ("search_query", "found_cards"),
    [
        (None, 3),
        ("", 3),
        ("test", 2),
        ("test deck2", 1),
    ],
)
@pytest.mark.django_db
def test_search_deck(decks, search_query, found_cards):
    assert (
        Deck.objects.search(search_query).count() == found_cards
    ), "search query '{}' search should return {} cards".format(
        search_query, found_cards
    )


@pytest.mark.django_db
def test_create_deck_with_same_cards(card_library):
    deck = Deck.objects.create(name="deck with same cards")
    card = card_library.cards[0].card
    deck.add_card(card)
    deck.add_card(card)
    deck.save()

    deck.refresh_from_db()
    assert len(deck.cards.all()) == 2, "Deck should contain two cards"
