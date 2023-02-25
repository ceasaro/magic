import json
import os

import pytest

from magic.core.models import Card
from magic.engine.game import Library
from magic.im_export import mtgjson


@pytest.fixture()
def card_library():
    file_path = os.path.join(
        os.path.dirname(__file__), "../data/mtgjson_set_1_com.json"
    )
    mtgjson.import_sets(json.load(open(file_path, "r")))
    library = Library()
    [library.add(card) for card in Card.objects.all()]
    return library


@pytest.fixture()
def card_library_2():
    file_path = os.path.join(os.path.dirname(__file__), "./data/mtgjson_set_1_com.json")
    mtgjson.import_sets(json.load(open(file_path, "r")))
    library = Library()
    [library.add(card) for card in Card.objects.all()]
    return library


@pytest.fixture()
def card_library_set_2():
    file_path = os.path.join(os.path.dirname(__file__), "./data/mtgjson_set_2_com.json")
    mtgjson.import_sets(json.load(open(file_path, "r")))
    library = Library()
    [library.add(card) for card in Card.objects.all()]
    return library


@pytest.fixture()
def lea_forest_land(card_library):
    return Card.objects.get(set__code="LEA", name="Forest")


@pytest.fixture()
def lea_badlands_land(card_library):
    return Card.objects.get(set__code="LEA", name="Badlands")


@pytest.fixture()
def lea_birds_of_paradise_creature(card_library):
    return Card.objects.get(set__code="LEA", name="Birds of Paradise")


@pytest.fixture()
def lea_bad_moon_enchantment(card_library):
    return Card.objects.get(set__code="LEA", name="Bad Moon")


@pytest.fixture()
def lea_berserk_instance(card_library):
    return Card.objects.get(set__code="LEA", name="Berserk")
