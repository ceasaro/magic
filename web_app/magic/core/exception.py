from django.core.exceptions import ValidationError


class MagicException(Exception):
    pass


class MagicGameException(Exception):
    pass


class NoManaException(Exception):
    pass


class ManaValidationError(MagicException, ValidationError):
    pass


class MagicImportException(Exception):
    pass


class MagicCardImageImportException(Exception):

    def __init__(self, msg, found_img_urls=None) -> None:
        super().__init__(msg)
        self.found_img_urls = found_img_urls if found_img_urls is not None else []
