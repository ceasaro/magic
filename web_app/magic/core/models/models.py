import re
import uuid

from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models

from magic.core.models import land_types
from magic.core.models.fields import ManaField, Mana
from magic.core.models.types import CardTypes


class Set(models.Model):
    name = models.CharField(max_length=256, unique=True)
    code = models.CharField(max_length=16)
    type = models.CharField(max_length=64)
    gathererCode = models.CharField(max_length=16, null=True, blank=True)
    releaseDate = models.DateField()

    def __repr__(self):
        return self.name


class Card(models.Model, CardTypes):
    name = models.CharField(max_length=256)
    external_id = models.CharField(primary_key=True, max_length=50, editable=False)
    set = models.ForeignKey(Set, blank=False, null=True, related_name='cards')
    _types = models.CharField(max_length=1024)
    type_line = models.CharField(max_length=256, null=True, blank=True)
    text = models.CharField(max_length=1024, null=True, blank=True)
    collector_number = models.CharField(max_length=64, null=True, blank=True)
    mana_cost = ManaField(default='', null=True, blank=True)
    _power = models.CharField(max_length=4)
    _toughness = models.CharField(max_length=4)

    unique_together = (("name", "set"),)

    @property
    def power(self):
        if self._power == '*':
            return self._power
        return Decimal(self._power)

    @property
    def toughness(self):
        if self._toughness == '*':
            return self._toughness
        return Decimal(self._toughness)

    @property
    def types(self):
        return self._types.split(',')

    @property
    def text_codes(self):
        if self.text:
            return re.findall('\{(.?)\}', self.text)

    @property
    def mana_source(self):
        codes = self.text_codes
        total_mana = colourless_mana = white_mana = blue_mana = black_mana = red_mana = green_mana = 0
        if codes:
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

        # card has no ability to add mana check if it's a land card
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

    def __repr__(self):
        return "{} ({})".format(self.name, self.set)


class Player(models.Model):
    user = models.OneToOneField(User)
    live = models.IntegerField(default=20)
    poison_counters = models.IntegerField(default=0)
    mana_pool = ManaField()


class Deck(models.Model):
    name = models.CharField(max_length=64)
    cards = models.ManyToManyField(Card, related_name='deck')


