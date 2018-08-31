# -*- coding: utf-8 -*-
"""Post lunch menu from chosen restaurants to Glip chat."""

from re import search, findall, DOTALL, sub
from requests import get, post
from bs4 import BeautifulSoup
from sys import exit
from parsers import GetMenuKanas, GetMenuPurkynka
import sys
import random

import json
import argparse


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, help="Type of posting conversation.")
    args = vars(ap.parse_args())

    with open('glip_links.json') as file:
        glip_links = json.load(file)

    with open('local_fortunecookies.json') as file:
        local_fortunecookies = json.load(file)

    with open('restaurant_links.json') as file:
        restaurant_links = json.load(file)

    post_url = glip_links[args["type"]]


