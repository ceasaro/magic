from django.conf.urls import url, include
from rest_framework import routers

from magic.core.api.views.magic_views import CardViewSet, SetViewSet, CardTypeViewSet

router = routers.DefaultRouter()
router.register(r'cards', CardViewSet, 'Card')
router.register(r'sets', SetViewSet, 'Set')
router.register(r'card_types', CardTypeViewSet, 'CardTypes')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]