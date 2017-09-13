from urllib.parse import urlencode
from urllib.request import urlopen

from bs4 import BeautifulSoup


def import_card_image(card_name):
    params = urlencode({'q': card_name})
    magiccards_url = 'https://magiccards.info'
    page = urlopen('{}/query?{}'.format(magiccards_url, params)).read().decode('utf-8')
    soup = BeautifulSoup(page, "html.parser")
    card_img = soup.find('img', {'alt': card_name})
    if card_img:
        img_url = card_img.get('src')
        return magiccards_url+img_url
