from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from magic.core.models import Set, Deck as StoredDeck
from magic.engine.game import Game, Player, Library


class NewGameView(TemplateView):
    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        starter_2000_set = Set.objects.get(name="Starter 2000")
        deck_a = Library()
        deck_b = Library()
        for card in starter_2000_set.cards.all():
            mana_source = card.mana_source
            if (
                card.mana_cost.white > 0
                or card.mana_cost.blue > 0
                or mana_source.white > 0
                or mana_source.blue > 0
            ):
                deck_b.add(card)
            else:
                deck_a.add(card)
        player_a = Player("Player A", deck_a)
        player_b = Player("Player B", deck_b)
        content["game"] = Game([player_a, player_b])
        return content
