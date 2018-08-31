import random
from bs4 import BeautifulSoup
from requests import get, post
from re import sub, findall, DOTALL
from json import dumps


def post_fortune_cookie(fortune_cookie_url,
                        fortune_cookie_icon_url,
                        glip_conv_url,
                        local_fortunecookies):

    if random.randint(1, 3) != 1:
        r = get(fortune_cookie_url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, features="xml").text
        cookie = sub(r'[\t\n\r]', '', str(soup))
        cookie_extracted = findall(r"([A-Za-z][0-9a-zA-Z\b-';:,.()?]{15,100}[.!?\b])", cookie, DOTALL)[1]
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
