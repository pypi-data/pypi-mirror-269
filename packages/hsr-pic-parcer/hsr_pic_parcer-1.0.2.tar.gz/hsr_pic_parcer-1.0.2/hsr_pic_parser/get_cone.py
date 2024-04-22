from .get_picture_info import get_pic
from .picture_url import url_light_cone


def get_cone_pic(name):
    url = f"{url_light_cone}{name}"
    type_pic = 'Character Primary Image'
    return get_pic(url, type_pic)


def get_cone_icon_pic(name):
    url = f"{url_light_cone}{name}"
    type_pic = ""
    return get_pic(url, type_pic)