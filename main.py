"""
from re import search, findall, DOTALL, sub
from requests import get, post
from sys import exit
from parsers import GetMenuKanas, GetMenuPurkynka
import sys
"""

import os
import argparse

from posters import post_fortune_cookie, post_menu
from parsers import get_menu_nepal
from json_files_handlers import load_data_from_json_files


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, help="Type of posting conversation.")
    args = vars(ap.parse_args())

    paths = {'glip_links_path': os.path.join('json_files', 'glip_links.json'),
             'local_fortunecookies_path': os.path.join('json_files', 'local_fortunecookies.json'),
             'urls_path': os.path.join('json_files', 'urls.json')}

    data_from_json_files = load_data_from_json_files(paths)

    glip_links = data_from_json_files['glip_links']
    local_fortunecookies = data_from_json_files['local_fortunecookies']
    urls = data_from_json_files['urls']

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
