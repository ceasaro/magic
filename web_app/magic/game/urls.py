from django.conf.urls import url

from magic.game.views import NewGameView

app_name = "game"
urlpatterns = [
    url(r"^new/$", NewGameView.as_view(template_name="game/board.html"), name="new"),
]
