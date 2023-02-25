import logging
from urllib.parse import urlencode
from urllib.request import urlopen

from bs4 import BeautifulSoup

from magic.core.exception import MagicCardImageImportException

log = logging.getLogger(__name__)


def import_card_image(card):
    types = "(type:{})".format(" OR type:".join(card.types)) if card.types else ""
    query = "{name} {types}".format(name=card.name, types=types)
    params = urlencode({"as": "grid", "order": "name", "q": query})
    magiccards_domain = "https://scryfall.com"
    url = "{domain}/search?{params}".format(domain=magiccards_domain, params=params)
    page = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(page, "html.parser")
    card_imgs = soup.find_all("img", {"class": "card"})
    img_urls = [url.get("src") for url in card_imgs]
    img_urls = [c for c in img_urls if c is not None]  # clean None's
    if len(img_urls) == 0:
        raise MagicCardImageImportException(
            "Could not download image from: {}. May be the card name doesn't match exactly".format(
                url
            )
        )
    elif len(img_urls) == 1:
        img_url = img_urls[0]
        return img_url
    else:
        raise MagicCardImageImportException(
            "Could not download image from: {}. To many results!".format(url),
            found_img_urls=img_urls,
        )
