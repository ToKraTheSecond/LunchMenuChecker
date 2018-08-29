# -*- coding: utf-8 -*-
"""Post lunch menu from chosen restaurants to Glip chat."""

from re import search, findall, DOTALL, sub
from requests import get, post
from json import dumps
from datetime import datetime
from bs4 import BeautifulSoup
from sys import exit
from czech_holidays import holidays
from parsers import GetMenuKanas, GetMenuPurkynka
import sys
import argparse
import random


if __name__ == "__main__":
    day = datetime.today().weekday()
    time = datetime.now().time()




    with open('gliplinks.txt') as f:
        url_list = f.readlines()

    with open('local_fortunecookie.txt') as ff:
        local_fortunecookie = ff.readlines()

    url_test = url_list[2][:-1]
    url_conv = url_list[4][:-1]
    url = ''

    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required = True,
	help = "Type of posting conversation t/o")
    ap.add_argument("--postfunc", required = True,
	help = "Name of posting function.")
    args = vars(ap.parse_args())

    if args["type"] == 't':
        url = url_test
    elif args["type"] == 'o':
        url = url_conv

    if args["postfunc"] in (str(x.__name__) for x in get_menu_func_list):
        try:
            if args["postfunc"] == 'PostFortuneCookie':
                PostFortuneCookie(url)
            else:
                PostMenu(getattr(sys.modules[__name__], args["postfunc"])(day), url)
        except:
            print("Posting of {} failed!".format(args["postfunc"]))
    else:
        for func in get_menu_func_list:
            try:
                if str(func.__name__) == 'PostFortuneCookie':
                    PostFortuneCookie(url)
                else:
                    PostMenu(func(day), url)
            except:
                print("{} posting failed.".format(func.__name__) )
