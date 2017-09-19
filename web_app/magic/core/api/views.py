from PIL import Image
from django.http import HttpResponse
from rest_framework.decorators import detail_route
from rest_framework.viewsets import ModelViewSet

from magic.core.api.serializers import CardSerializer, SetSerializer
from magic.core.models import Card, Set


class SetViewSet(ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer

    def get_queryset(self):
        queryset = Set.objects.all()
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        o = self.request.query_params.get('o', 'name')
        if o:
            queryset = queryset.order_by(o)
        return queryset


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.all()
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(name__icontains=q)
        set_name = self.request.query_params.get('s', None)
        if set_name:
            queryset = queryset.filter(set__name=set_name)
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
