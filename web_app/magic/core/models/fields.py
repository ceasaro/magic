import sys
from django.db import models
from django.utils.translation import ugettext_lazy as _

from magic.core.exception import ManaValidationError, NoManaException

EXCEPTIONAL_MANA = [
    'XYZRR',  # The Ultimate Nightmare of Wizards of the Coast® Customer Service
    'hw',  # Little Girl
]


class Mana(str):
    ANY = ''
    WHITE = 'W'
    BLUE = 'U'
    BLACK = 'B'
    RED = 'R'
    GREEN = 'G'
    COLOURLESS = 'C'

    def __init__(self, *args, any=0, white=0, blue=0, black=0, red=0, green=0, colourless=0):
        self.any = any
        self.white = white
        self.blue = blue
        self.black = black
        self.red = red
        self.green = green
        self.colourless = colourless
        self.X = ''
        str_repr = args[0] if args else None
        if str_repr:
            self.from_str(str_repr)

    def from_str(self, str_repr):
        # todo: allow mana of the form '{B/R}' (black or red)
        # todo: allow mana of the form 'C'
        any = ''
        if str_repr in EXCEPTIONAL_MANA:
            self.any = 2**31  # not implement make cost to high to pay.
            return
        for i, char in enumerate(str_repr):
            if char in '0123456789' and len(any) == (i - len(self.X)):
                any += char
            elif char == self.WHITE:
                self.white += 1
            elif char == self.BLUE:
                self.blue += 1
            elif char == self.BLACK:
                self.black += 1
            elif char == self.RED:
                self.red += 1
            elif char == self.GREEN:
                self.green += 1
            elif char == self.COLOURLESS:
                self.colourless += 1
            elif char == 'X':
                self.X += 'X'
            elif char == '/':
                # todo: allow mana of the form '{B/R}' (black or red)
                any = str(2**31)  # not implement make cost to high to pay.
                break
            else:
                raise ManaValidationError(_("Illegal string representation for mana: {}".format(str_repr)))
        if any:
            self.any = int(any)

    def val(self):
        return self.__str__()

    def __str__(self, *args, **kwargs):
        return "{}{}{}{}{}{}{}{}".format(
            self.X,
            self.any if self.any else '0' if self.white + self.blue + self.black + self.red + self.green == 0 and not self.X else '',
            self.WHITE * self.white,
            self.BLUE * self.blue,
            self.BLACK * self.black,
            self.RED * self.red,
            self.GREEN * self.green,
            self.COLOURLESS * self.colourless)

    def __repr__(self):
        return self.__str__()


class ManaPool(Mana):

    def can_pay(self, mana):
        return self.any >= mana.any \
        and self.white >= mana.white \
        and self.blue >= mana.blue \
        and self.black >= mana.black \
        and self.red >= mana.red \
        and self.green >= mana.green \
        and self.colourless >= mana.colourless

    def pay(self, mana):
        if self.can_pay(mana):
            self.any -= mana.any
            self.white -= mana.white
            self.blue -= mana.blue
            self.black -= mana.black
            self.red -= mana.red
            self.green -= mana.green
            self.colourless -= mana.colourless

        else:
            raise NoManaException("can't pay mana, needed '{}', available '{}'".format(mana, self))

    def add(self, mana):
        self.any += mana.any
        self.white += mana.white
        self.blue += mana.blue
        self.black += mana.black
        self.red += mana.red
        self.green += mana.green
        self.colourless += mana.colourless

    def substract(self, mana):
        self.any -= mana.any
        self.white -= mana.white
        self.blue -= mana.blue
        self.black -= mana.black
        self.red -= mana.red
        self.green -= mana.green
        self.colourless -= mana.colourless


class ManaField(models.CharField):
    def __init__(self, *args, **kwargs):
        if not 'max_length' in kwargs:
            kwargs['max_length'] = 32
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return super().db_type(connection)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return Mana(value)

    def to_python(self, value):
        if isinstance(value, Mana):
            return value
        if value is None:
            return value
        return Mana(value)

    def get_prep_value(self, value):
        return str(value)
