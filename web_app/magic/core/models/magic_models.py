import operator
import re

from decimal import Decimal

import os
from urllib.request import urlretrieve

import errno

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from functools import reduce

from magic.core.models.fields import ManaField, Mana
from magic.core.models.types import CardTypes, LandTypes
from magic.im_export.magiccards import import_card_image

CARD_IMAGES_ROOT = os.path.join(settings.MEDIA_ROOT, "CARD_IMAGES")


class Set(models.Model):
    name = models.CharField(max_length=256, unique=True)
    code = models.CharField(max_length=16)
    type = models.CharField(max_length=64)
    gathererCode = models.CharField(max_length=16, null=True, blank=True)
    releaseDate = models.DateField()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


def card_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if filename:
        path_name, img_ext = os.path.splitext(filename)
        return "CARD_IMAGES/{0}/{1}{2}".format(
            slugify(instance.set.name), slugify(instance.name), img_ext
        )


class CardQuerySet(models.QuerySet):
    def valid_mana(self):
        return self.exclude(mana_cost__contains=Mana.NOT_IMPLEMENTED)

    def search(
        self,
        q=None,
        w=None,
        u=None,
        b=None,
        r=None,
        g=None,
        c=None,
        sets=None,
        card_types=None,
    ):
        query_set = self.valid_mana()

        def filter_mana(mana, mana_value):
            if mana_value:
                if isinstance(mana_value, int) or (
                    isinstance(mana_value, str) and mana_value.isdigit()
                ):
                    mana_query = mana * int(mana_value)
                elif (
                    isinstance(mana_value, str)
                    and mana_value.upper().replace(mana, "") == ""
                ):
                    mana_query = mana_value.upper()
                else:
                    mana_query = None
                if mana_query:
                    return query_set.filter(mana_cost__contains=mana_query)
                else:
                    return query_set.none()
            return query_set

        if q:
            query_set = query_set.filter(name__icontains=q)
        query_set = filter_mana(Mana.WHITE, w)
        query_set = filter_mana(Mana.BLUE, u)
        query_set = filter_mana(Mana.BLACK, b)
        query_set = filter_mana(Mana.RED, r)
        query_set = filter_mana(Mana.GREEN, g)
        query_set = filter_mana(Mana.COLOURLESS, c)
        if sets:
            sets = [sets] if isinstance(sets, str) else sets
            query_set = query_set.filter(set__name__in=sets)

        if card_types:
            card_types = [card_types] if isinstance(card_types, str) else card_types
            query_set = query_set.filter(
                reduce(
                    operator.and_,
                    (
                        Q(_types__contains=ct)
                        | Q(_subtypes__contains=ct)
                        | Q(_supertypes__contains=ct)
                        for ct in card_types
                    ),
                )
            )
        return query_set


class Card(models.Model, CardTypes):
    name = models.CharField(max_length=256)
    image = models.FileField(upload_to=card_image_path, null=True, blank=True)
    external_id = models.CharField(primary_key=True, max_length=50, editable=False)
    set = models.ForeignKey(
        Set, blank=False, null=True, related_name="cards", on_delete=models.SET_NULL
    )
    _types = models.CharField(max_length=1024)
    _subtypes = models.CharField(max_length=1024, null=True)
    _supertypes = models.CharField(max_length=1024, null=True)
    type_line = models.CharField(max_length=256, null=True, blank=True)
    text = models.CharField(max_length=1024, null=True, blank=True)
    collector_number = models.CharField(max_length=64, null=True, blank=True)
    mana_cost = ManaField(default="", null=True, blank=True)
    cmc = models.IntegerField(default=0)
    _power = models.CharField(max_length=4)
    _toughness = models.CharField(max_length=4)

    unique_together = (("name", "set"),)

    objects = CardQuerySet.as_manager()

    class Meta:
        ordering = [
            "name",
        ]

    def download_image(self, refresh=False, url=None):
        if not self.image or refresh or url:
            img_url = url or import_card_image(self)
            if img_url:
                img_model_name = card_image_path(self, img_url)
                img_file_name = os.path.join(settings.MEDIA_ROOT, img_model_name)
                if not os.path.exists(os.path.dirname(img_file_name)):
                    try:
                        os.makedirs(os.path.dirname(img_file_name))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                urlretrieve(img_url, img_file_name)
                self.image = img_model_name
                self.save()
        return self.image

    @property
    def power(self):
        if self._power == "*":
            return self._power
        return Decimal(self._power)

    @property
    def toughness(self):
        if self._toughness == "*":
            return self._toughness
        return Decimal(self._toughness)

    @property
    def types(self):
        return self._types.split(",")

    @property
    def subtypes(self):
        return self._subtypes.split(",")

    @property
    def text_codes(self):
        if self.text:
            return re.findall("\{(.?)\}", self.text)

    @property
    def mana_source(self):
        codes = self.text_codes
        total_mana = (
            any_mana
        ) = white_mana = blue_mana = black_mana = red_mana = green_mana = 0
        if codes:
            any_mana = codes.count(Mana.ANY)
            total_mana += any_mana
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
        card_types = self.subtypes
        if total_mana == 0:
            if LandTypes.PLAINS in card_types:
                white_mana += 1
            elif LandTypes.ISLAND in card_types:
                blue_mana += 1
            elif LandTypes.SWAMP in card_types:
                black_mana += 1
            elif LandTypes.MOUNTAIN in card_types:
                red_mana += 1
            elif LandTypes.FOREST in card_types:
                green_mana += 1

        return Mana(
            any=any_mana,
            white=white_mana,
            blue=blue_mana,
            black=black_mana,
            red=red_mana,
            green=green_mana,
        )

    def is_supertype(self):
        return any(x in self.types for x in self.SUPERTYPES)

    def is_permanent(self):
        return any(x in self.types for x in self.PERMANENTS)

    def is_non_permanent(self):
        return any(x in self.types for x in self.NON_PERMANENTS)

    def is_artifact(self):
        return any(x in self.types for x in self.ARTIFACT)

    def is_creature(self):
        return self.CREATURE in self.types

    def is_enchantment(self):
        return any(x in self.types for x in self.ENCHANTMENT)

    def is_land(self):
        return any(x in self.types for x in self.LANDS)

    def is_planes_walker(self):
        return any(x in self.types for x in self.PLANESWALKER)

    def __repr__(self):
        return "{} ({}): Card".format(self.name, self.set)

    def __str__(self):
        return self.__repr__()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    live = models.IntegerField(default=20)
    poison_counters = models.IntegerField(default=0)
    mana_pool = ManaField()


class DeckQuerySet(models.QuerySet):
    def search(self, query):
        if query is None:
            return self.all()
        return self.filter(name__icontains=query)


class Deck(models.Model):
    name = models.CharField(max_length=64, unique=True)
    set = models.ForeignKey(Set, null=True, blank=True, on_delete=models.SET_NULL)

    objects = DeckQuerySet.as_manager()

    class Meta:
        ordering = [
            "name",
        ]

    def add_card(self, card):
        if isinstance(card, str):
            card = Card.objects.get(external_id=card)
        DeckCard.objects.create(card=card, deck=self)

    def __str__(self):
        return self.name


class DeckCard(models.Model):
    card = models.ForeignKey(Card, related_name="decks", on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, related_name="cards", on_delete=models.CASCADE)

    class Meta:
        ordering = [
            "card__name",
        ]


#
#   Model signals
#
@receiver(post_save, sender=Player, dispatch_uid="add_player_to_group")
def add_player_to_group(sender, instance, **kwargs):
    user = instance.user
    user.groups.add(Group.objects.get(name="player"))
    user.save()
