from rest_framework import serializers

from magic.core.models import Card, Set, Deck


class MagicModelSerializer(serializers.ModelSerializer):
    pass


class SetSerializer(MagicModelSerializer):

    class Meta:
        model = Set
        fields = ('name', 'code', 'type', 'releaseDate')


class CardSerializer(MagicModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ('name', 'external_id', 'mana_cost', 'image_url')

    def get_image_url(self, card):
        return card.image.url if card.image else ''


class DeckSerializer(MagicModelSerializer):

    class Meta:
        model = Deck
        fields = ('name', 'cards')