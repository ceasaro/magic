from django import forms
from django.contrib import admin


from magic.core.models import Card, Set, Deck, Player


class CardAdminForm(forms.ModelForm):

    image_url = forms.CharField(required=False)
    _subtypes = forms.CharField(required=False)

    def save(self, commit=True):
        card = super(CardAdminForm, self).save(commit=commit)
        image_url = self.cleaned_data.get("image_url", None)
        if image_url:
            card.download_image(url=image_url)
        # ...do something with extra_field here...
        return card

    class Meta:
        model = Card
        exclude = ["image"]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    search_fields = ["name", "external_id"]
    list_filter = ("set",)
    form = CardAdminForm


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    pass


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass
