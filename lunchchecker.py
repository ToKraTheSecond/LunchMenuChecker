# -*- coding: utf-8 -*-
"""Post lunch menu from chosen restaurants to Glip chat."""

from re import search, findall, DOTALL, sub
from requests import get, post
from json import dumps
from datetime import datetime
from bs4 import BeautifulSoup
from sys import exit
from czech_holidays import holidays
from GetMenuGetLink import GetMenuBuddha, GetMenuGoldenNepal, GetMenuSabaidy, GetMenuBishesGurkha, GetMenuOsmicka, GetMenuDoubravnicka, GetMenuTriOcasci, GetMenuPonava
import sys
import argparse
import random



def PostFortuneCookie(url):
    """Get and post fortune cookie."""
    if random.randint(1, 3) != 1:
        r = get("http://www.fortunecookiemessage.com")
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html5lib").text
        cookie = sub(r'[\t\n\r]', '', str(soup))
        cookie_extracted = findall(r"([A-Za-z][0-9a-zA-Z\b-';:,.()?]{15,100}[.!?\b])", cookie, DOTALL)[1]
    else:
        cookie_extracted = local_fortunecookie[random.randint(1, len(local_fortunecookie))][:-1]
        print(cookie_extracted)
    body = "\nFortune Cookie of the Day\n" \
        + "\n**" + cookie_extracted + "**\n\n"
    payload = {'body': body}
    headers = {'content-type': 'application/json'}
    response = post(url, data=dumps(payload), headers=headers)


def PostMenu(menu_dict, url):
    """Send given menu to given Glip URL."""

    body = menu_dict["url"] + "\n"
    body += menu_dict["Info"] + "\n"

    if "CardPay" in menu_dict.keys():
        body += "**Platba kartou:** " + menu_dict["CardPay"] + "\n"
    if "Polévka" in menu_dict.keys():
        body += "**Polévka:** " + menu_dict["Polévka"] + "\n"
    if "Menu 1" in menu_dict.keys():
        body += "**Menu 1:** " + menu_dict["Menu 1"]["menu"] + " - " + str(menu_dict["Menu 1"]["cena"]) + "\n"
    if "Menu 2" in menu_dict.keys():
        body += "**Menu 2:** " + menu_dict["Menu 2"]["menu"] + " - " + str(menu_dict["Menu 2"]["cena"]) + "\n"
    if "Menu 3" in menu_dict.keys():
        body += "**Menu 3:** " + menu_dict["Menu 3"]["menu"] + " - " + str(menu_dict["Menu 3"]["cena"]) + "\n"
    if "Menu 4" in menu_dict.keys():
        body += "**Menu 4:** " + menu_dict["Menu 4"]["menu"] + " - " + str(menu_dict["Menu 4"]["cena"]) + "\n"
    if "Menu 5" in menu_dict.keys():
        body += "**Menu 5:** " + menu_dict["Menu 5"]["menu"] + " - " + str(menu_dict["Menu 5"]["cena"]) + "\n"

    payload = \
        {
         'activity': menu_dict["Name"],
    	 'icon': menu_dict["Icon"],
    	 'body': body
        }

    headers = {'content-type': 'application/json'}
    response = post(url, data=dumps(payload), headers=headers)

if __name__ == "__main__":
    day = datetime.today().weekday()
    time = datetime.now().time()

    get_menu_func_list = [
        GetMenuBuddha,
        GetMenuGoldenNepal,
        GetMenuSabaidy,
        GetMenuBishesGurkha,
        GetMenuOsmicka,
        GetMenuDoubravnicka,
        GetMenuTriOcasci,
        GetMenuPonava,
        PostFortuneCookie
    ]

    '''
    get_link_func_list = [
        GetLinkBuddha,
        GetLinkGoldenNepal,
        GetLinkSabaidy,
        GetLinkBishesGurkha,
        GetLinkOsmicka,
        GetLinkDoubravnicka,
        GetLinkTriOcasci,
        GetLinkPonava,
    ]
    '''
    if datetime.date(datetime.now()) in holidays:
        sys.exit()

    if day == 5 or day == 6:
        sys.exit()

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
                PostMenu(getattr(sys.modules[__name__], args["postfunc"])(), url)
        except:
            print("{} failed!".format(args["postfunc"]))
    else:
        for func in get_menu_func_list:
            try:
                if str(func.__name__) == 'PostFortuneCookie':
                    PostFortuneCookie(url)
                else:
                    PostMenu(func(), url)
            except:
                print("{} failed.".format(func.__name__) )
