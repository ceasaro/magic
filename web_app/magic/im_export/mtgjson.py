from magic.core.models import Card


def import_cards(json_data):
    for card_name, card in json_data.items():
        # import pdb; pdb.set_trace()
        new_card, created = Card.objects.update_or_create(name=card['name'],
                                                          defaults={
                                                              '_types': ','.join(card.get('subtypes', [])),
                                                              'type_line': card.get('type', None),
                                                              'text': card.get('text', None),
                                                              'mana_cost': card.get('manaCost', '').translate(
                                                                  {ord(c): None for c in '{}'}),
                                                              'power': int(card.get('power', 0)),
                                                              'toughness': int(card.get('toughness', 0)),
                                                          })
