import logging
from urllib.parse import urlencode
from urllib.request import urlopen

from bs4 import BeautifulSoup

from magic.core.exception import MagicImportException

log = logging.getLogger(__name__)


def import_card_image(card_name):
    params = urlencode({'q': card_name})
    magiccards_domain = 'https://magiccards.info'
    url = '{}/query?{}'.format(magiccards_domain, params)
    try:
        page = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(page, "html.parser")
        card_img = soup.find('img', {'class': 'card'})
        if card_img:
            img_url = card_img.get('src')
            return img_url
        else:
            raise MagicImportException("Could not download image from: {}. May be the card name doesn't match exactly".format(url))
    except Exception as e:
        log.exception(e)
        raise MagicImportException("Could not download image from: {}. Cause: {} ".format(url, e))
