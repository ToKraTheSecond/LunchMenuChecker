"""
from re import search, findall, DOTALL, sub
from requests import get, post
from sys import exit
from parsers import GetMenuKanas, GetMenuPurkynka
import sys
"""

import json
import argparse

from posters import post_fortune_cookie


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, help="Type of posting conversation.")
    args = vars(ap.parse_args())

    with open('glip_links.json') as file:
        glip_links = json.load(file)

    with open('local_fortunecookies.json') as file:
        local_fortunecookies = json.load(file)

    with open('urls.json') as file:
        urls = json.load(file)

    post_url = glip_links[args["type"]]

    post_fortune_cookie(urls["fortune_cookie"],
                        urls["fortune_cookie_icon"],
                        post_url,
                        local_fortunecookies["local_fortune_cookies"])




