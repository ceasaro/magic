from django import template
from django.utils.safestring import mark_safe

from magic.engine.game import CardState

register = template.Library()


@register.filter(name="card_img")
def card_img(card, args=None):
    """

    :param card: a CardState instance
    :param args: In the form of "
    :return: html img-tag with the image of the card
    """
    assert isinstance(
        card, CardState
    ), "can only handle instances of {}, but received {}".format(
        CardState, card.__class__
    )
    h = w = 0
    if isinstance(args, int):
        h = args
    elif isinstance(args, str):
        arg_list = [arg.strip() for arg in args.split(",")] if args else []
        h = int(arg_list[0]) if len(arg_list) > 0 and arg_list[0].isdigit() else 0
        w = int(arg_list[1]) if len(arg_list) > 1 and arg_list[1].isdigit() else 0

    height = "height={}".format(h) if h > 0 else ""
    width = "width={}".format(w) if w > 0 else ""
    return mark_safe(
        "<div class='card-img-wrapper' ><img src='{}' alt='{}' {} {} class='hover-enlarge' id={}/></div>".format(
            card.image.url, card.name, height, width, card.external_id
        )
    )
