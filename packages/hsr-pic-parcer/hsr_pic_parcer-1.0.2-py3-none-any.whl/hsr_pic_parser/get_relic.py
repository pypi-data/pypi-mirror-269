from .get_picture_info import get_pic
from .picture_url import url_relic


def get_relic_icon_pic(name):
    url = f"{url_relic}{name}"
    type_pic = ""
    return get_pic(url, type_pic)