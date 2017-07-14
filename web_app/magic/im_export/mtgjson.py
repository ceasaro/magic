import json
from datetime import datetime

from magic.core.exception import ManaValidationError
from magic.core.models import Card, Set


def import_cards(json_data, verbosity=0):
    for card_name, card in json_data.items():
        try:
            new_card, created = create_or_update_card(card)
            if verbosity >= 2:
                print("{}: {}".format("ADDED" if created else "UPDATED", card_name))
        except Exception as e:
            print("ERROR import card: {}. Cause {}".format(card_name, e))
            raise e


def create_or_update_card(card, set):
    new_card, created = Card.objects.update_or_create(name=card.get('name'),
                                                      set=set,
                                                      defaults={
                                                          '_types': ','.join(card.get('subtypes', [])),
                                                          'type_line': card.get('type', None),
                                                          'text': card.get('text', None),
                                                          'mana_cost': card.get('manaCost', '').translate(
                                                              {ord(c): None for c in '{}'}),
                                                          '_power': card.get('power', 0),
                                                          '_toughness': card.get('toughness', 0),
                                                      })
    return new_card, created


def import_sets(json_data, verbosity=0):
    for set_name, set_data in json_data.items():
        try:
            set, set_created = Set.objects.update_or_create(name=set_data['name'],
                                                            code=set_data['code'],
                                                            type=set_data['type'],
                                                            gathererCode=set_data.get('gathererCode'),
                                                            releaseDate=datetime.strptime(set_data['releaseDate'],
                                                                                          '%Y-%m-%d')
                                                            )
        except Exception as e:
            print("ERROR creating set: {}. Cause {}".format(set_name, e))
            raise e
        for card in set_data['cards']:
            try:
                new_card, created = create_or_update_card(card, set)
            except ManaValidationError as mana_e:
                print("Unknown mana for card: {}".format(card))
            except Exception as e:
                print("ERROR import card: {}. Cause {}".format(json.dumps(card), e))
                raise e
            if verbosity >= 2:
                print("{}: {}".format("ADDED" if created else "UPDATED", card['name']))
