from re import findall, DOTALL, sub
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime


def get_fortune_cookie(fortune_cookie_url):
    r = get(fortune_cookie_url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, features="xml").text
    cookie = sub(r'[\t\n\r]', '', str(soup))
    fortune_cookie = findall(r"([A-Za-z][0-9a-zA-Z\b-';:,.()?]{15,100}[.!?\b])", cookie, DOTALL)[1]

    return fortune_cookie


def get_menu_nepal(urls):
    r = get(urls.nepal_brno_menu)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "xml")
    menu = soup.findAll("div", {"class", "the_content_wrapper"})
    menu = sub(r'[\t\n\r]', '', str(menu).replace("<br/>", ""))

    main_meals = findall("td>[1,2,3,4,5]\.*(.*?)\s*</td", menu, DOTALL)
    soups = findall("td>Polévka:(.*?)\s*</td", menu, DOTALL)
    prices = findall("<td><strong>(.*?)Kč</strong></td>", menu, DOTALL)

    are_all_meals_parsed = len(main_meals) == 20
    are_all_soups_parsed = len(soups) == 5
    are_all_prices_parsed = len(prices) == 25

    if False in [are_all_meals_parsed, are_all_prices_parsed, are_all_soups_parsed]:
        # ToDo: this is cool place for logger
        print(f'Nepal: are_all_meals_parsed: {are_all_meals_parsed},'
              f' are_all_prices_parsed: {are_all_prices_parsed},'
              f' are_all_soups_parsed: {are_all_soups_parsed}')
        # ToDo: quit script

    nepal = {"Name": "Indian and Nepalese Restaurant."}

    main_meal_ranges = [range(0, 4),
                        range(4, 8),
                        range(8, 12),
                        range(12, 16),
                        range(16, 20)]

    prices_ranges = [range(0, 5),
                     range(5, 10),
                     range(10, 15),
                     range(15, 20),
                     range(20, 25)]

    for day_idx, (main_meal_range, prices_range) in enumerate(zip(main_meal_ranges, prices_ranges)):
        if day_idx == datetime.today().weekday():
            soup_index = day_idx
            nepal["payload"] = _get_nepal_menu_payload(soup_index, main_meal_range, prices_range,
                                                       main_meals, soups, prices)

    return nepal


def _get_nepal_menu_payload(soup_index, main_meal_range, prices_range,
                            main_meals, soups, prices):
    nepal_payload = f"""{soups[soup_index]} {prices[prices_range[0]]},-,
                        {main_meals[main_meal_range[0]]} {prices[prices_range[1]]},-,
                        {main_meals[main_meal_range[1]]} {prices[prices_range[2]]},-,
                        {main_meals[main_meal_range[2]]} {prices[prices_range[3]]},-, 
                        {main_meals[main_meal_range[3]]} {prices[prices_range[4]]},-
                     """

    return nepal_payload
