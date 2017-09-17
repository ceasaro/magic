from django.conf.urls import url, include
from rest_framework import routers

from magic.core.api.views import CardViewSet, SetViewSet

router = routers.DefaultRouter()
router.register(r'cards', CardViewSet, 'Card')
router.register(r'sets', SetViewSet, 'Set')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]