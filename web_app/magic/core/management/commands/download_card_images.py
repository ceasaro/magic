import os
from django.core.management import BaseCommand

from magic.core.models import Card


class Command(BaseCommand):
    help = 'download card images of card'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='download the images for all cards (if image is not present)',
        )
        parser.add_argument(
            '-c', '--card',
            dest='card',
            help='download image for this card',
        )
        parser.add_argument(
            '-r', '--refresh',
            action='store_true',
            dest='refresh',
            default=False,
            help='refresh image card(s) even it has already been downloaded',
        )

    def handle(self, *args, **options):
        refresh = options['refresh']
        if options['card']:
            self.download_image(Card.objects.filter(name=options['card']), refresh=refresh)
        elif options['all']:
            if console_confirm('Are yo sure you want to download all missing card images, this can take a while.?'):
                self.download_image(Card.objects.all(), refresh=refresh)
            else:
                print ("Downloading card images aborted")
        else:
            command_name = os.path.splitext(os.path.basename(__file__))[0]
            print ("No valid options specified! type './manage.py {} -h' for more info.".format(command_name))

    def download_image(self, cards, refresh=False):
        for card in cards:
            try:
                card.download_image(refresh=refresh)
                print("downloaded image for card '{}'".format(card))
            except:
                print("ERROR downloading image for card '{}'".format(card))


def console_confirm(msg):
    """
    Displays a message in the console that asks for confirmation.
    :param msg: The message to be displayed
    :return: True if confirmed False otherwise
    """
    if msg:
        confirmed = input("{0} (y/n)  ".format(msg))
        return confirmed in ['y', 'yes', 'Y', 'YES']
    else:
        return False
