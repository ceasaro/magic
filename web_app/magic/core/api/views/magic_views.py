from PIL import Image
from django.http import HttpResponse
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from magic.core.api.serializers.magic_serializers import CardSerializer, SetSerializer, DeckSerializer
from magic.core.api.views.BaseViews import MagicViewSet, MagicModelViewSet
from magic.core.models import Card, Set, Deck


class SetViewSet(MagicModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Set.objects.all()
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        o = self.request.query_params.get('o', 'name')
        if o:
            queryset = queryset.order_by(o)
        return queryset


class CardViewSet(MagicModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.all()
        params = self.request.query_params
        set_name = params.get('s')
        if set_name:
            queryset = queryset.filter(set__name=set_name)
        queryset = queryset.search(
            q=self.request.query_params.get('q'),  # search query
            w=self.request.query_params.get('w'),  # white mana
            u=self.request.query_params.get('u'),  # blue mana
            b=self.request.query_params.get('b'),  # black mana
            r=self.request.query_params.get('r'),  # read mana
            g=self.request.query_params.get('g'),  # green mana
            c=self.request.query_params.get('c'),  # colorless mana
            card_types=self.request.query_params.get('ct')
        )

        return queryset

    @detail_route()
    def image(self, request, pk):
        card = self.get_object()
        image_data = card.image
        if image_data:
            return HttpResponse(image_data, content_type="image/png")
        else:
            red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
            response = HttpResponse(content_type="image/png")
            red.save(response, "PNG")
            return response

    @detail_route()
    def download_img(self, request, pk):
        card = self.get_object()
        card.download_image()
        serializer = self.serializer_class(card)
        return Response(serializer.data)


class DeckViewSet(MagicModelViewSet):
    serializer_class = DeckSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Deck.objects.all()

    def get_object(self):
        return super().get_object()


class CardTypeViewSet(MagicViewSet):
    permission_classes = []

    def list(self, request):
        return Response(Card.ALL_TYPES)

    def get(self, request, *args, **kwargs):
        return Response(Card.ALL_TYPES)