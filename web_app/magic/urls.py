from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from magic.api import urls as core_api_urls
from magic.game import urls as game_urls

urlpatterns = [
    # url(r'^about/$', TemplateView.as_view(template_name="about.html")),
    path(r"game/", include(game_urls)),
    path(r"api/", include(core_api_urls)),
    path(r"admin/", admin.site.urls),
    path(r"", TemplateView.as_view(template_name="home.html"), name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
