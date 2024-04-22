from .get_picture_info import get_pic
from .picture_url import url_character


def get_char_pic(name):
    url = f"{url_character}{name}"
    type_pic = 'Background Image - Main'
    return get_pic(url, type_pic)


def get_char_icon_pic(name):
    url = f"{url_character}{name}"
    type_pic = ""
    return get_pic(url, type_pic)

