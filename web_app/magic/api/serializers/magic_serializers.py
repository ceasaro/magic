from rest_framework import serializers

from magic.core.models import Card, Set, Deck


class MagicModelSerializer(serializers.ModelSerializer):
    pass


class SetSerializer(MagicModelSerializer):
    class Meta:
        model = Set
        fields = ("name", "code", "type", "releaseDate")


class CardSerializer(MagicModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ("name", "external_id", "mana_cost", "image_url")

    def get_image_url(self, card):
        return card.image.url if card.image else ""

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        image_url = self.initial_data.get("image_url")
        if image_url:
            instance.download_image(url=image_url)
        return instance


class DeckSerializer(MagicModelSerializer):
    cards = serializers.SerializerMethodField()

    class Meta:
        model = Deck
        fields = ("name", "cards")

    def get_cards(self, deck):
        return [c.card.external_id for c in deck.cards.all()]

    def create(self, validated_data):
        deck = super().create(validated_data)
        self._set_cards(deck)
        return deck

    def update(self, instance, validated_data):
        deck = super().update(instance, validated_data)
        self._set_cards(deck)
        return deck

    def _set_cards(self, deck):
        card_ids = self.initial_data.get("cards")
        if not isinstance(
            card_ids, list
        ):  # when running pytest .get('cards') returns only first id not a list
            # for pytest use the .getlist('cards') method.
            # Has probably something to do with request headers (content type??)
            card_ids = self.initial_data.getlist("cards")
        deck.cards.all().delete()  # delete all existing cards before adding new ones.
        for card_id in card_ids:
            deck.add_card(card_id)


class DeckDetailSerializer(DeckSerializer):
    def save(self, **kwargs):
        return super().save(**kwargs)

    def get_cards(self, deck):
        return [CardSerializer(instance=c.card).data for c in deck.cards.all()]
