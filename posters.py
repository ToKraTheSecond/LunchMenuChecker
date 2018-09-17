import random
from requests import post
from json import dumps

from parsers import get_fortune_cookie


def post_fortune_cookie(fortune_cookie_url,
                        fortune_cookie_icon_url,
                        glip_conv_url,
                        local_fortunecookies):

    if random.randint(1, 3) != 1:
        cookie_extracted = get_fortune_cookie(fortune_cookie_url)
    else:
        cookie_extracted = local_fortunecookies[random.randint(1, len(local_fortunecookies))][:-1]

    payload = \
        {
            "icon": fortune_cookie_icon_url,
            "activity": "Fortune Cookie of the Day",
            "body": cookie_extracted
        }
    headers = {'content-type': 'application/json'}
    response = post(glip_conv_url, data=dumps(payload), headers=headers)


def post_menu(post_url,
              restaurant_icon_url,
              restaurant_name,
              parsed_menu):

    payload = \
        {
            "icon": restaurant_icon_url,
            "activity": restaurant_name,
            "body": parsed_menu
        }

    headers = {'content-type': 'application/json'}
    response = post(post_url, data=dumps(payload), headers=headers)
