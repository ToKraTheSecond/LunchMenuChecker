from re import findall, DOTALL, sub
from requests import get
from json import dumps
from bs4 import BeautifulSoup

def GetMenuKanasJidelna(day):
    kanasJidelna = {"url": "http://www.kanas.cz/stranka/jidelna"}
    kanasJidelna["Name"] = "Jídelna Kansas"
    kanasJidelna["Info"] = "5 minut"
    kanasJidelna["Icon"] = "http://www.barber-schools.org/wp-content/uploads/2013/02/state-flag-kansas.jpg"
    kanasJidelna["CardPay"] = "Ano"

    try:
        kanasJidelnaTemp = kanasJidelna

        r = get("http://www.kanas.cz/stranka/jidelna")
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html5lib")  # Gets html code
        menu = soup.findAll("div", {"class", "menu-list menu-list__dotted"})
        menu_extracted = sub(r'[\t\n\r]', '', str(menu))

        menu_courses_czech = findall(r"content\">(.*?)</", menu_extracted_day[0], DOTALL)
        menu_courses_orig = findall(r"_title\">(.*?)</", menu_extracted_day[0], DOTALL)
        menu_courses = menu_courses_orig
        for i in range(len(menu_courses_orig)):
            menu_courses[i] = menu_courses_orig[i] + " - " + menu_courses_czech[i]
        menu_prices = findall(r"price\">(.*?)</", menu_extracted_day[0], DOTALL)

        kanasJidelnaTemp["Polévka"] = menu_courses[0] + " " + menu_prices[0]

        kanasJidelnaTemp["Menu 1"] = dict()
        kanasJidelnaTemp["Menu 1"]["menu"] = menu_courses[1]
        kanasJidelnaTemp["Menu 1"]["cena"] = menu_prices[1]

        kanasJidelnaTemp["Menu 2"] = dict()
        kanasJidelnaTemp["Menu 2"]["menu"] = menu_courses[2]
        kanasJidelnaTemp["Menu 2"]["cena"] = menu_prices[2]

        kanasJidelnaTemp["Menu 3"] = dict()
        kanasJidelnaTemp["Menu 3"]["menu"] = menu_courses[3]
        kanasJidelnaTemp["Menu 3"]["cena"] = menu_prices[3]

        kanasJidelnaTemp["Menu 4"] = dict()
        kanasJidelnaTemp["Menu 4"]["menu"] = menu_courses[4]
        kanasJidelnaTemp["Menu 4"]["cena"] = menu_prices[4]

        kanasJidelna = kanasJidelnaTemp
    except:
        print("KanasJidelna parser failed!")

    return kanasJidelna
