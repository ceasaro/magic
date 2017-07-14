from django.core.exceptions import ValidationError


class MagicException(Exception):
    pass

class ManaValidationError(MagicException, ValidationError):
    pass