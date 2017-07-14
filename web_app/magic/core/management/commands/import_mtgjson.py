import json
import os

from django.conf import settings
from django.core.management import BaseCommand

from magic.im_export import mtgjson


class Command(BaseCommand):
    all_cards_json = os.path.join(settings.PROJECT_DIR, 'data/mtgjson.com/AllCards.json')
    all_sets_json = os.path.join(settings.PROJECT_DIR, 'data/mtgjson.com/AllSets.json')
    help = 'import magic the gathering data from the [PROJECT]/data/*.json (mtgjson.com)'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--cards',
            action='store_true',
            dest='cards',
            default=False,
            help='Import cards from {}'.format(self.all_cards_json),
        )
        parser.add_argument(
            '--sets',
            action='store_true',
            dest='sets',
            default=False,
            help='Import set from {}'.format(self.all_sets_json),
        )

    def handle(self, *args, **options):
        if options['cards']:
            mtgjson.import_cards(json.load(open(self.all_cards_json, 'r')), verbosity=options['verbosity'])
        elif options['sets']:
            mtgjson.import_sets(json.load(open(self.all_sets_json, 'r')), verbosity=options['verbosity'])
        else:
            print ('No valid options specified! type ./manage import_mtgjson -h for more info.')
