from django.urls import path

from magic.game.views import NewGameView

app_name = "game"
urlpatterns = [
    path(r"new/", NewGameView.as_view(template_name="game/board.html"), name="new"),
]
