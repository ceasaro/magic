from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from magic.core.api.views.auth_views import UserViewSet
from magic.core.api.views.magic_views import CardViewSet, SetViewSet, CardTypeViewSet, DeckViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'User')
router.register(r'cards', CardViewSet, 'Card')
router.register(r'sets', SetViewSet, 'Set')
router.register(r'card_types', CardTypeViewSet, 'CardTypes')
router.register(r'decks', DeckViewSet, 'Deck')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    # url(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]