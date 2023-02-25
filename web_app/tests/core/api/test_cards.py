import os

import pytest
from django.template.defaultfilters import slugify


@pytest.mark.django_db
def test_update_card_img(api_client_cees, card_library):
    card_id = "5ede9781b0c5d157c28a15c3153a455d7d6180fa"
    # image_png = 'http://example.com/card_image.png'
    card_image = "file://{}".format(
        os.path.join(os.path.dirname(__file__), "../../data/card_img.jpg")
    )
    card = card_library.get(card_id)
    assert not card.image, "card should not have an image"
    response = api_client_cees.patch(
        "/api/cards/{}/".format(card_id), {"image_url": card_image}
    )
    response_data = ""
    if hasattr(response, "data"):
        response_data = "Response was: {}".format(response.data)
    assert response.status_code == 200, "status code: {}. {}".format(
        response.status_code, response_data
    )
    card.refresh_from_db()
    assert card.external_id == card_id, "sanity check if we still have the same card"
    assert card.image.name == "CARD_IMAGES/{0}/{1}{2}".format(
        slugify(card.set.name), slugify(card.name), ".jpg"
    )
