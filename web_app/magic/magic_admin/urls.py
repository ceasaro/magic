from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^deck/', include([
        url(r'^create/$', TemplateView.as_view(template_name='magic_admin/create_deck.html'), name='create'),
    ], namespace='deck')),
]
