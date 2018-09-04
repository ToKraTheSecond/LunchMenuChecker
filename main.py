"""
from re import search, findall, DOTALL, sub
from requests import get, post
from sys import exit
from parsers import GetMenuKanas, GetMenuPurkynka
import sys
"""

import os
import json
import argparse

from posters import post_fortune_cookie, post_menu
from parsers import get_menu_nepal


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, help="Type of posting conversation.")
    args = vars(ap.parse_args())

    with open(os.path.join('json_files', 'glip_links.json')) as file:
        glip_links = json.load(file)

    with open(os.path.join('json_files', 'local_fortunecookies.json')) as file:
        local_fortunecookies = json.load(file)

    with open(os.path.join('json_files', 'urls.json')) as file:
        urls = json.load(file)

    post_url = glip_links[args["type"]]

    post_fortune_cookie(urls["fortune_cookie"],
                        urls["fortune_cookie_icon"],
                        post_url,
                        local_fortunecookies["local_fortune_cookies"])

    nepal = get_menu_nepal(urls)

    post_menu(post_url,
              urls["nepal_brno_icon"],
              nepal["Name"],
              nepal["payload"])
