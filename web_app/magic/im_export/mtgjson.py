from magic.core.models import Card


def import_cards(json_data, verbose=False):
    for card_name, card in json_data.items():
        try:
            new_card, created = Card.objects.update_or_create(name=card_name,
                                                              defaults={
                                                                  '_types': ','.join(card.get('subtypes', [])),
                                                                  'type_line': card.get('type', None),
                                                                  'text': card.get('text', None),
                                                                  'mana_cost': card.get('manaCost', '').translate(
                                                                      {ord(c): None for c in '{}'}),
                                                                  '_power': card.get('power', 0),
                                                                  '_toughness': card.get('toughness', 0),
                                                              })
            if verbose:
                print ("{}: {}".format("ADDED" if created else "UPDATED", card_name))
        except Exception as e:
            print ("ERROR import card: {}. Cause {}".format(card_name, e))
            raise e

