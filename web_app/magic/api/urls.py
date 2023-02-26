from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from magic.api.views.auth_views import UserViewSet
from magic.api.views.magic_views import (
    CardViewSet,
    SetViewSet,
    CardTypeViewSet,
    DeckViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, "User")
router.register(r"cards", CardViewSet, "Card")
router.register(r"sets", SetViewSet, "Set")
router.register(r"card_types", CardTypeViewSet, "CardTypes")
router.register(r"decks", DeckViewSet, "Deck")

app_name = "api"
urlpatterns = [
    path(r"", include(router.urls)),
    path(r"token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(r"token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # url(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    path(r"api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
