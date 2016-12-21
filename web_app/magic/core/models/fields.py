from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Mana(object):
    COLOURLESS = ''
    WHITE = 'W'
    BLUE = 'U'
    GREEN = 'G'
    RED = 'R'
    BLACK = 'B'

    def __init__(self, *args, colourless=0, white=0, blue=0, black=0, red=0, green=0):
        self.colourless = colourless
        self.white = white
        self.blue = blue
        self.black = black
        self.red = red
        self.green = green
        str_repr = args[0] if args else None
        if str_repr:
            self.from_str(str_repr)

    def from_str(self, str_repr):
        colourless = ''
        for i, char in enumerate(str_repr):
            if char in '0123456789' and len(colourless) == i:
                colourless += char
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
            else:
                raise ValidationError(_("Illegal string representation for mana: {}".format(str_repr)))
        if colourless:
            self.colourless = int(colourless)

    def __str__(self, *args, **kwargs):
        return "{}{}{}{}{}{}".format(self.colourless if self.colourless else
                                        '0' if self.white + self.blue + self.black + self.red + self.green == 0 else '',
                                     self.WHITE * self.white,
                                     self.BLUE * self.blue,
                                     self.BLACK * self.black,
                                     self.RED * self.red,
                                     self.GREEN * self.green)

    def __repr__(self):
        return self.__str__()

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
