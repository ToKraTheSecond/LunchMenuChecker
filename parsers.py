from re import findall, DOTALL, sub
from requests import get
from bs4 import BeautifulSoup


def get_fortune_cookie(fortune_cookie_url):
    r = get(fortune_cookie_url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, features="xml").text
    cookie = sub(r'[\t\n\r]', '', str(soup))
    fortune_cookie = findall(r"([A-Za-z][0-9a-zA-Z\b-';:,.()?]{15,100}[.!?\b])", cookie, DOTALL)[1]

    return fortune_cookie


def get_menu_nepal(urls):
    nepal = {"Name": "Indian and Nepalese Restaurant."}

    r = get(urls.nepal_brno_menu)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "xml")
    menu = soup.findAll("div", {"class", "the_content_wrapper"})
    menu = sub(r'[\t\n\r]', '', str(menu).replace("<br/>", ""))

    main_meals = findall("td>[1,2,3,4,5]\.*(.*?)\s*</td", menu, DOTALL)
    soups = findall("td>Polévka:(.*?)\s*</td", menu, DOTALL)
    prices = findall("<td><strong>(.*?)Kč</strong></td>", menu, DOTALL)

    nepal["payload"] = f"""{soups[0]} {prices[0]},-,
                           {main_meals[0]} {prices[1]},-,
                           {main_meals[1]} {prices[2]},-,
                           {main_meals[2]} {prices[3]},-, 
                           {main_meals[3]} {prices[4]},-
                        """
    return nepal