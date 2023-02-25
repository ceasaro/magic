import pytest
from django.core.exceptions import ValidationError

from magic.core.models.fields import Mana


@pytest.mark.parametrize(
    ("mana_str", "expected_mana_str", "expected"),
    [
        ("3WUBBGGGCCCC", "3WUBBGGGCCCC", (3, "", 1, 1, 2, 0, 3, 4)),
        # 7 tuple 3 any mana, optional 'X', 1 white, 1 bleu, 2 black, 0 red, 3 green, 4 colourless
        ("6UU", "6UU", (6, "", 0, 2, 0, 0, 0, 0)),
        ("GG", "GG", (0, "", 0, 0, 0, 0, 2, 0)),
        ("WBBRRRR", "WBBRRRR", (0, "", 1, 0, 2, 4, 0, 0)),
        ("12R", "12R", (12, "", 0, 0, 0, 1, 0, 0)),
        (
            "WWWWWWWWWWWWBBBBBBBBBBBBBBBB",
            "WWWWWWWWWWWWBBBBBBBBBBBBBBBB",
            (0, "", 12, 0, 16, 0, 0, 0),
        ),
        ("0", "0", (0, "", 0, 0, 0, 0, 0, 0)),
        ("", "0", (0, "", 0, 0, 0, 0, 0, 0)),
        ("X", "X", (0, "X", 0, 0, 0, 0, 0, 0)),
        ("X1U", "X1U", (1, "X", 0, 1, 0, 0, 0, 0)),
        ("XWWUUR", "XWWUUR", (0, "X", 2, 2, 0, 1, 0, 0)),
        ("XX2WW", "XX2WW", (2, "XX", 2, 0, 0, 0, 0, 0)),
        ("6C", "6C", (6, "", 0, 0, 0, 0, 0, 1)),  # can pay 2 any or 1 plain (3 times)
        (
            "2/W2/W2/W",
            "N",
            (0, "", 0, 0, 0, 0, 0, 0),
        ),  # can pay 2 any or 1 plain (3 times)
        (None, "0", (0, "", 0, 0, 0, 0, 0, 0)),
        ("1W3G", "exception", "exception"),
        ("XYZRR", "N", (0, "", 0, 0, 0, 0, 0, 0)),  # Exception mana skip for now
    ],
)
def test_mana(mana_str, expected_mana_str, expected):
    if expected == "exception":
        try:
            Mana(mana_str)
            assert False, "expected {} to throw a validation exception".format(mana_str)
        except ValidationError:
            assert True
    else:
        mana = Mana(mana_str)
        assert mana.any == expected[0], "expected {} any mana for {}".format(
            expected[0], mana_str
        )
        assert mana.X == expected[1], "expected {} mana for {}".format(
            expected[1], mana_str
        )
        assert mana.white == expected[2], "expected {} white mana for {}".format(
            expected[2], mana_str
        )
        assert mana.blue == expected[3], "expected {} bleu mana for {}".format(
            expected[3], mana_str
        )
        assert mana.black == expected[4], "expected {} black mana for {}".format(
            expected[4], mana_str
        )
        assert mana.red == expected[5], "expected {} red mana for {}".format(
            expected[5], mana_str
        )
        assert mana.green == expected[6], "expected {} green mana for {}".format(
            expected[6], mana_str
        )
        assert (
            mana.colourless == expected[7]
        ), "expected {} colourless mana for {}".format(expected[7], mana_str)
        assert str(mana) == expected_mana_str
