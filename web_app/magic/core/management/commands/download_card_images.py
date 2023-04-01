import os
from django.core.management import BaseCommand

from magic.core.models import Card, Set


class Command(BaseCommand):
    help = "download card images of card"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.verbosity = None

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--all",
            action="store_true",
            default=False,
            help="download the images for all cards (if image is not present)",
        )
        parser.add_argument(
            "-c",
            "--card",
            help="download image for this card",
        )
        parser.add_argument(
            "-r",
            "--refresh",
            action="store_true",
            default=False,
            help="refresh image card(s) even it has already been downloaded",
        )
        parser.add_argument(
            "-s",
            "--set_name",
            help="download all images for this set",
        )

    def handle(self, all=False, card=None, refresh=False, set_name=False, *args, **kwargs):
        self.verbosity = kwargs.get("verbosity", 1)
        if card:
            self.download_images(Card.objects.filter(card), refresh=refresh)
        if set_name:
            sets = Set.objects.filter(name=set_name)
            if sets.count() == 1:
                card_set = sets.first()
                cards = Card.objects.filter(set=card_set)
                if console_confirm(f"Download all ({cards.count()}) images for set '{card_set}'?"):
                    self.download_images(cards, refresh=refresh)
        elif all:
            if console_confirm(
                "Are yo sure you want to download all missing card images, this can take a while.?"
            ):
                if refresh:
                    self.download_images(Card.objects.all(), refresh=refresh)
                else:
                    self.download_images(Card.objects.filter(image__isnull=not refresh))
            else:
                print("Downloading card images aborted")
        else:
            command_name = os.path.splitext(os.path.basename(__file__))[0]
            print(
                "No valid options specified! type './manage.py {} -h' for more info.".format(
                    command_name
                )
            )

    def download_images(self, cards, refresh=False):
        total = len(cards)
        for i, card in enumerate(cards):
            try:
                card, updated = card.download_image(refresh=refresh)
                if updated:
                    message = "downloaded image for card '{}'".format(card)
                else:
                    message = "skipped image for card '{}'".format(card)
            except Exception as e:
                message = "ERROR downloading image for card '{}'".format(card)
                if self.verbosity >= 2:
                    print(f"\n\n {e}")
            print("{}/{}: {}".format(i, total, message))


def console_confirm(msg):
    """
    Displays a message in the console that asks for confirmation.
    :param msg: The message to be displayed
    :return: True if confirmed False otherwise
    """
    if msg:
        confirmed = input("{0} (y/n)  ".format(msg))
        return confirmed in ["y", "yes", "Y", "YES"]
    else:
        return False
