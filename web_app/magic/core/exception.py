from django.core.exceptions import ValidationError


class MagicException(Exception):
    pass

class MagicGameException(Exception):
    pass

class NoManaException(Exception):
    pass

class ManaValidationError(MagicException, ValidationError):
    pass