import re

from decimal import Decimal

import os
from urllib.request import urlretrieve

import errno
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from django.template.defaultfilters import slugify

from magic.core.models import land_types
from magic.core.models.fields import ManaField, Mana
from magic.core.models.types import CardTypes
from magic.im_export.magiccards import import_card_image

CARD_IMAGES_ROOT = os.path.join(settings.MEDIA_ROOT, 'CARD_IMAGES')


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
    path_name, img_ext = os.path.splitext(filename)
    return 'CARD_IMAGES/{0}/{1}{2}'.format(slugify(instance.set.name), slugify(instance.name), img_ext)


class Card(models.Model, CardTypes):
    name = models.CharField(max_length=256)
    image = models.FileField(upload_to=card_image_path, null=True, blank=True)
    external_id = models.CharField(primary_key=True, max_length=50, editable=False)
    set = models.ForeignKey(Set, blank=False, null=True, related_name='cards')
    _types = models.CharField(max_length=1024)
    _subtypes = models.CharField(max_length=1024)
    type_line = models.CharField(max_length=256, null=True, blank=True)
    text = models.CharField(max_length=1024, null=True, blank=True)
    collector_number = models.CharField(max_length=64, null=True, blank=True)
    mana_cost = ManaField(default='', null=True, blank=True)
    _power = models.CharField(max_length=4)
    _toughness = models.CharField(max_length=4)

    unique_together = (("name", "set"),)

    @property
    def download_image(self):
        if not self.image:
            img_url = import_card_image(self.name)
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
            pass
        return self.image

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
    def subtypes(self):
        return self._subtypes.split(',')

    @property
    def text_codes(self):
        if self.text:
            return re.findall('\{(.?)\}', self.text)

    @property
    def mana_source(self):
        codes = self.text_codes
        total_mana = any_mana = white_mana = blue_mana = black_mana = red_mana = green_mana = 0
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

        return Mana(any=any_mana,
                    white=white_mana,
                    blue=blue_mana,
                    black=black_mana,
                    red=red_mana,
                    green=green_mana)


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
    user = models.OneToOneField(User)
    live = models.IntegerField(default=20)
    poison_counters = models.IntegerField(default=0)
    mana_pool = ManaField()


class Deck(models.Model):
    name = models.CharField(max_length=64, unique=True)
    set = models.ForeignKey(Set, null=True, blank=True)
    cards = models.ManyToManyField(Card, related_name='deck')

