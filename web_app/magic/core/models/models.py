import re
from django.contrib.auth.models import User
from django.db import models

from magic.core.models import land_types
from magic.core.models.fields import ManaField, Mana
from magic.core.models.types import CardTypes


class Card(models.Model, CardTypes):

    name = models.CharField(max_length=64, unique=True)
    _types = models.CharField(max_length=1024)
    type_line = models.CharField(max_length=64, null=True, blank=True)
    text = models.CharField(max_length=1024, null=True, blank=True)
    collector_number = models.CharField(max_length=64, null=True, blank=True)
    mana_cost = ManaField(default='', null=True, blank=True)
    power = models.IntegerField(default=0)
    toughness = models.IntegerField(default=0)

    @property
    def types(self):
        return self._types.split(',')

    @property
    def text_codes(self):
        return re.findall('\{(.?)\}', self.text)

    @property
    def mana_source(self):
        codes = self.text_codes
        total_mana = 0
        colourless_mana = codes.count(Mana.COLOURLESS)
        total_mana += colourless_mana
        white_mana = codes.count(Mana.WHITE)
        total_mana += white_mana
        blue_mana = codes.count(Mana.BLUE)
        total_mana += blue_mana
        black_mana = codes.count(Mana.BLACK)
        total_mana += black_mana
        red_mana = codes.count(Mana.RED)
        total_mana += red_mana
        green_mana = codes.count(Mana.GREEN)
        total_mana += green_mana

        # card has no ability to add mana check if it's a land
        card_types = self.types
        if total_mana == 0:
            if land_types.PLAINS in card_types:
                white_mana += 1
            elif land_types.ISLAND in card_types:
                blue_mana += 1
            elif land_types.SWAMP in card_types:
                black_mana += 1
            elif land_types.MOUNTAIN in card_types:
                red_mana += 1
            elif land_types.FOREST in card_types:
                green_mana += 1

        return Mana(colourless=colourless_mana,
                    white=white_mana,
                    blue=blue_mana,
                    black=black_mana,
                    red=red_mana,
                    green=green_mana)


class Player(models.Model):
    user = models.OneToOneField(User)
    live = models.IntegerField(default=20)
    poison_counters = models.IntegerField(default=0)
    mana_pool = ManaField()


class Deck(models.Model):
    name = models.CharField(max_length=64)
    cards = models.ManyToManyField(Card, related_name='deck')


