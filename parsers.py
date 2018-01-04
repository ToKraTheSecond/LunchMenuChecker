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
        menu = soup.findAll("div", {"class", "nabidka-in tab_container"})
        menu_extracted = sub(r'[\t\n\r]', '', str(menu))
        print(menu_extracted)
        menu_extracted = findall(r"id=\"tab2(.*?)class=\"cle", menu_extracted, DOTALL)
        print(menu_extracted[0])

        menu_courses = findall(r"content\">(.*?)</", menu_extracted_day[0], DOTALL)
        menu_prices = findall(r"price\">(.*?)</", menu_extracted_day[0], DOTALL)

        kanasJidelnaTemp["Polévka 1"] = menu_courses[0] + " " + menu_prices[0]
        kanasJidelnaTemp["Polévka 2"] = menu_courses[0] + " " + menu_prices[0]

        kanasJidelnaTemp["Menu 1"] = dict()
        kanasJidelnaTemp["Menu 1"]["menu"] = menu_courses[1]
        kanasJidelnaTemp["Menu 1"]["cena"] = menu_prices[1]

        kanasJidelna = kanasJidelnaTemp
    except:
        print("KanasJidelna parser failed!")

    return kanasJidelna
