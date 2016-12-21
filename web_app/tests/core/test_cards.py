import pytest
from django.core.exceptions import ValidationError

from magic.core.models.fields import Mana
from magic.core.models import Card


@pytest.mark.parametrize(("mana_str", "expected_mana_str", "expected"), [
        ("3WUBBGGG", "3WUBBGGG", (3,1,1,2,0,3)),  # 6 tuple 3 colourless, 1 white, 1 bleu, 2 black, 0 red, 3 green
        ("6UU", "6UU", (6,0,2,0,0,0)),
        ("GG", "GG", (0,0,0,0,0,2)),
        ("WBBRRRR", "WBBRRRR", (0,1,0,2,4,0)),
        ("12R", "12R", (12,0,0,0,1,0)),
        ("WWWWWWWWWWWWBBBBBBBBBBBBBBBB", "WWWWWWWWWWWWBBBBBBBBBBBBBBBB", (0,12,0,16,0,0)),
        ("0", "0", (0,0,0,0,0,0)),
        ("", "0", (0,0,0,0,0,0)),
        (None, "0", (0,0,0,0,0,0)),
        ("1W3G", "exception", "exception"),
    ])
def test_mana(mana_str, expected_mana_str, expected):
    if expected == 'exception':
        try:
            Mana(mana_str)
            assert False, 'expected {} to throw a validation exception'.format(mana_str)
        except ValidationError:
            assert True
    else:
        mana = Mana(mana_str)
        assert mana.colourless == expected[0], 'expected {} colourless mana for {}'.format(expected[0], mana_str)
        assert mana.white == expected[1], 'expected {} white mana for {}'.format(expected[1], mana_str)
        assert mana.blue == expected[2], 'expected {} bleu mana for {}'.format(expected[2], mana_str)
        assert mana.black == expected[3], 'expected {} black mana for {}'.format(expected[3], mana_str)
        assert mana.red == expected[4], 'expected {} red mana for {}'.format(expected[4], mana_str)
        assert mana.green == expected[5], 'expected {} green mana for {}'.format(expected[5], mana_str)
        assert str(mana) == expected_mana_str


@pytest.mark.django_db
def test_card():
    card = Card.objects.create(
        name='my card',
        mana_cost=Mana(red=1, blue=12),
        _power='1',
        _toughness='2',
    )
    assert card.name == 'my card'
    assert card.id, "id should have been generated"
    assert str(card.mana_cost) == 'UUUUUUUUUUUUR'