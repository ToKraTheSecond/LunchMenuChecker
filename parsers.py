from re import search, findall, DOTALL, sub
from requests import get, post
from json import dumps
from datetime import datetime
from bs4 import BeautifulSoup
from sys import exit
import sys
import argparse

def GetMenuBuddha(day):
    """Get Buddha lunch menu."""
    buddha = {"url": "http://www.indian-restaurant-buddha.cz/index.html"}
    buddha["Name"] = "Buddha: Indická a Nepálská Restaurace"
    buddha["Info"] = "Příloha ke každému jídlu (v ceně): Tandoori Nan (indický chléb) / indická rýže Basmati / kombinace obou příloh. Polévka se podává zvlášť/soup is served separately from menu. (22 Kč)"
    buddha["Icon"] = "http://www.brnorozvoz.cz/restaurace-brno-v/indicka-a-nepalska-restaurace-buddha-brno.png"
    buddha["CardPay"] = "Ano"

    try:
        buddhaTemp = buddha
        r = get(buddha["url"])
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html5lib")
        menu = soup.findAll("p", {"class", "textmenu"})
        menu_extracted = sub(r'[\t\n\r]', '', str(menu).replace("<br/>", "")
                                                       .replace("&amp;", " a "))

        if(day == 0):
            menu_extracted_day = findall("PONDĚLÍ(.*?)ÚTERÝ", menu_extracted, DOTALL)
        elif(day == 1):
            menu_extracted_day = findall("ÚTERÝ(.*?)STŘEDA", menu_extracted, DOTALL)
        elif(day == 2):
            menu_extracted_day = findall("STŘEDA(.*?)ČTVRTEK", menu_extracted, DOTALL)
        elif(day == 3):
            menu_extracted_day = findall("ČTVRTEK(.*?)PÁTEK", menu_extracted, DOTALL)
        elif(day == 4):
            menu_extracted_day = findall("PÁTEK(.*?)ALERGENY", menu_extracted, DOTALL)

        buddhaTemp["Polévka"] = findall("Polévka:(.*?)22,- Kč", menu_extracted_day[0], DOTALL)[0]
        buddhaTemp["Menu 1"] = dict()
        buddhaTemp["Menu 1"]["menu"] = findall("22,- Kč(.*?)95,- Kč", menu_extracted_day[0], DOTALL)[0]
        buddhaTemp["Menu 1"]["cena"] = 95

        buddhaTemp["Menu 2"] = dict()
        buddhaTemp["Menu 2"]["menu"] = findall("95,- Kč(.*?)95,- Kč", menu_extracted_day[0], DOTALL)[0]
        buddhaTemp["Menu 2"]["cena"] = 95

        buddhaTemp["Menu 3"] = dict()
        buddhaTemp["Menu 3"]["menu"] = findall("VEG(.*?)95,-.*?Kč", menu_extracted_day[0], DOTALL)[0]
        buddhaTemp["Menu 3"]["cena"] = 95

        buddhaTemp["Menu 4"] = dict()
        buddhaTemp["Menu 4"]["menu"] = findall("(150g Mix Thali.*?)130,- Kč", menu_extracted_day[0], DOTALL)[0]
        buddhaTemp["Menu 4"]["cena"] = 130

        buddha = buddhaTemp
    except:
        print("Buddha parser failed!")

    return buddha


def GetMenuOsmicka(day):
    """Get Osmicka lunch menu."""
    osmicka = {"url": "http://www.naosmicce.cz/Menu.pdf"}
    osmicka["Name"] = "Bistro na Osmičce: Burger and Pasta"
    osmicka["Info"] = "Polévka dle denní nabídky je během doby poledního menu zahrnuta v ceně!"
    osmicka["Icon"] = "http://www.naosmicce.cz/img/logo.png"
    osmicka["CardPay"] = "Ne"

    try:
        osmickaTemp = osmicka
        r = get("https://www.menicka.cz/3840-bistro-na-osmicce.html")
        r.encoding = 'windows-1250'

        soup = BeautifulSoup(r.text, "html5lib")  # Get html code
        menu = soup.findAll("div", {"class", "menicka"})
        menu_extracted = sub(r'[\t\n\r]', '', str(menu))

        if(day == 0):
            menu_extracted_day = findall("Pondělí(.*?)Úterý", menu_extracted, DOTALL)
        elif(day == 1):
            menu_extracted_day = findall("Úterý(.*?)Středa", menu_extracted, DOTALL)
        elif(day == 2):
            menu_extracted_day = findall("Středa(.*?)Čtvrtek", menu_extracted, DOTALL)
        elif(day == 3):
            menu_extracted_day = findall("Čtvrtek(.*?)Pátek", menu_extracted, DOTALL)
        elif(day == 4):
            menu_extracted_day = findall("Pátek(.*?)Sobota", menu_extracted, DOTALL)

        osmickaTemp["Polévka"] = findall("Polévka:(.*?)<", menu_extracted_day[0], DOTALL)[0]
        osmickaTemp["Veg polévka"] = findall("Vegetariánské menu:(.*?)<", menu_extracted_day[0], DOTALL)[0]

        osmickaTemp["Menu 1"] = dict()
        osmickaTemp["Menu 2"] = dict()
        osmickaTemp["Menu 3"] = dict()

        menu_types = findall(r"\"nabidka_1\">(.*?)<", menu_extracted_day[0], DOTALL)

        if len(menu_types) > 3:  # Bug at source web: long menu is shown as two menus
            # This can cause problems if the long menu is not the first one
            osmickaTemp["Menu 1"]["menu"] = menu_types[0] + " " + menu_types[1]
            osmickaTemp["Menu 2"]["menu"] = menu_types[2]
            osmickaTemp["Menu 3"]["menu"] = menu_types[3]
        else:
            osmickaTemp["Menu 1"]["menu"] = menu_types[0]
            osmickaTemp["Menu 2"]["menu"] = menu_types[1]
            osmickaTemp["Menu 3"]["menu"] = menu_types[2]

        osmickaTemp["Menu 1"]["cena"] = findall(r"\"cena\">(.*?)<", menu_extracted_day[0], DOTALL)[0]
        osmickaTemp["Menu 2"]["cena"] = findall(r"\"cena\">(.*?)<", menu_extracted_day[0], DOTALL)[1]
        osmickaTemp["Menu 3"]["cena"] = findall(r"\"cena\">(.*?)<", menu_extracted_day[0], DOTALL)[2]

        osmicka = osmickaTemp
    except:
        print("Osmicka parser failed!")

    return osmicka


def GetMenuGoldenNepal(day):
    """Get Golden Nepal lunch menu."""
    goldenNepal = {"url": "http://goldennepal.cz/"}
    goldenNepal["Name"] = "Golden Nepal: Nepálská restaurace a bar"
    goldenNepal["Info"] = "Ke každému jídlu ve všední den příloha rýže/placka/kombinace ZDARMA. Všechna jídla kromě Vindaloo, Jalfrezi, Madrasu a Falu obsahují smetanu. Všechny polévky obsahují mouku. Korma obsahuje ořechy. Chicken Tikka Masala, Butter Chicken a Vindaloo obsahují barvivo."
    goldenNepal["Icon"] = "http://goldennepal.cz/wp-content/uploads/2016/06/logotext.png"
    goldenNepal["CardPay"] = "Ano"

    try:
        goldenNepalTemp = goldenNepal

        r = get("http://goldennepal.cz/denni-menu/")
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html5lib")  # Gets html code
        menu = soup.findAll("div", {"class", "menu-list menu-list__dotted"})
        menu_extracted = sub(r'[\t\n\r]', '', str(menu))

        if(day == 0):
            menu_extracted_day = findall("Pondělí(.*?)Úterý", menu_extracted, DOTALL)
        elif(day == 1):
            menu_extracted_day = findall("Úterý(.*?)Středa", menu_extracted, DOTALL)
        elif(day == 2):
            menu_extracted_day = findall("Středa(.*?)Čtvrtek", menu_extracted, DOTALL)
        elif(day == 3):
            menu_extracted_day = findall("Čtvrtek(.*?)Pátek", menu_extracted, DOTALL)
        elif(day == 4):
            menu_extracted_day = findall("Pátek(.*?)Sobota", menu_extracted, DOTALL)

        menu_courses_czech = findall(r"content\">(.*?)</", menu_extracted_day[0], DOTALL)
        menu_courses_orig = findall(r"_title\">(.*?)</", menu_extracted_day[0], DOTALL)
        menu_courses = menu_courses_orig
        for i in range(len(menu_courses_orig)):
            menu_courses[i] = menu_courses_orig[i] + " - " + menu_courses_czech[i]
        menu_prices = findall(r"price\">(.*?)</", menu_extracted_day[0], DOTALL)

        goldenNepalTemp["Polévka"] = menu_courses[0] + " " + menu_prices[0]

        goldenNepalTemp["Menu 1"] = dict()
        goldenNepalTemp["Menu 1"]["menu"] = menu_courses[1]
        goldenNepalTemp["Menu 1"]["cena"] = menu_prices[1]

        goldenNepalTemp["Menu 2"] = dict()
        goldenNepalTemp["Menu 2"]["menu"] = menu_courses[2]
        goldenNepalTemp["Menu 2"]["cena"] = menu_prices[2]

        goldenNepalTemp["Menu 3"] = dict()
        goldenNepalTemp["Menu 3"]["menu"] = menu_courses[3]
        goldenNepalTemp["Menu 3"]["cena"] = menu_prices[3]

        goldenNepalTemp["Menu 4"] = dict()
        goldenNepalTemp["Menu 4"]["menu"] = menu_courses[4]
        goldenNepalTemp["Menu 4"]["cena"] = menu_prices[4]

        goldenNepal = goldenNepalTemp
    except:
        print("GoldenNepal parser failed!")

    return goldenNepal


def GetMenuSabaidy(day):
    """Get Sabaidy lunch menu."""
    sabaidy = {"url": "http://www.amphone.eu/restaurace"}
    sabaidy["Name"] = "Sabaidy: Thajsko-laoská restaurace"
    sabaidy["Info"] = "Polední menu podáváme každý všední den od 11 do 14 hodin. Polévka v ceně menu."
    sabaidy["Icon"] = "http://goldennepal.cz/wp-content/uploads/2016/06/logotext.png"
    sabaidy["CardPay"] = "Ano"

    try:
        sabaidyTemp = sabaidy
        r = get("http://www.amphone.eu/restaurace")
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html5lib")  # Gets html code
        menu = soup.findAll("div", {"class", "uk-width-medium-1-2 uk-container-center"})
        menu_extracted = sub(r'[\t\n\r]','',str(menu))

        if(day == 0):
            menu_extracted_day = findall("Pondělí(.*?)Úterý", menu_extracted, DOTALL)
        elif(day == 1):
            menu_extracted_day = findall("Úterý(.*?)Středa", menu_extracted, DOTALL)
        elif(day == 2):
            menu_extracted_day = findall("Středa(.*?)Čtvrtek", menu_extracted, DOTALL)
        elif(day == 3):
            menu_extracted_day = findall("Čtvrtek(.*?)Pátek", menu_extracted, DOTALL)
        elif(day == 4):
            menu_extracted_day = findall("Pátek(.*?)ubytovani", menu_extracted, DOTALL)

        menu_courses = findall(r"<li>([^<>].*?)\b[0-9]", menu_extracted_day[0], DOTALL)
        menu_prices = findall(r"\b([0-9]{2,3}?),-", menu_extracted_day[0], DOTALL)

        sabaidyTemp["Polévka"] = findall(r"m>(.*?)</", menu_extracted_day[0], DOTALL)[0]

        sabaidyTemp["Menu 1"] = dict()
        sabaidyTemp["Menu 1"]["menu"] = menu_courses[0]
        sabaidyTemp["Menu 1"]["cena"] = menu_prices[0]

        sabaidyTemp["Menu 2"] = dict()
        sabaidyTemp["Menu 2"]["menu"] = menu_courses[1]
        sabaidyTemp["Menu 2"]["cena"] = menu_prices[1]

        sabaidyTemp["Menu 3"] = dict()
        sabaidyTemp["Menu 3"]["menu"] = menu_courses[2]
        sabaidyTemp["Menu 3"]["cena"] = menu_prices[2]

        sabaidyTemp["Menu 4"] = dict()
        sabaidyTemp["Menu 4"]["menu"] = menu_courses[3]
        sabaidyTemp["Menu 4"]["cena"] = menu_prices[3]

        sabaidy = sabaidyTemp
    except:
        print("Sabaidy parser failed!")

    return sabaidy

def GetMenuTriOcasci(day):
    """Get TriOcasci lunch menu."""
    triOcasci = {"url": "https://triocasci.cz/jidlo/"}
    triOcasci["Name"] = "Tři ocásci: Veganská restaurace"
    triOcasci["Info"] = "Polévka není v ceně menu. Je možné ji objednat samostatně."
    triOcasci["Icon"] = "https://triocasci.cz/favicon.png"
    triOcasci["CardPay"] = "??"

    try:
        triOcasciTemp = triOcasci
        r = get("https://triocasci.cz/jidlo/")
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html5lib")  # Gets html code
        menu_extracted = sub(r'[\t\n\r]', '', str(soup)).replace('\xa0', '')

        if(day == 0):
            menu_extracted_day = findall("Po(.*?)Út", menu_extracted, DOTALL)
        elif(day == 1):
            menu_extracted_day = findall("Út(.*?)St", menu_extracted, DOTALL)
        elif(day == 2):
            menu_extracted_day = findall("St(.*?)Čt", menu_extracted, DOTALL)
        elif(day == 3):
            menu_extracted_day = findall("Čt(.*?)Pá", menu_extracted, DOTALL)
        elif(day == 4):
            menu_extracted_day = findall("Pá(.*?)script", menu_extracted, DOTALL)

        menu_courses = findall(r"li>([A-Z,Č,Ď,Ř,Š,Ť,Ž].*?)<span", menu_extracted_day[0], DOTALL)
        menu_prices = findall(r"price\">([1-9].*?)</span", menu_extracted_day[0], DOTALL)

        triOcasciTemp["Polévka"] = menu_courses[0] + " " + menu_prices[0]

        triOcasciTemp["Menu 1"] = dict()
        triOcasciTemp["Menu 1"]["menu"] = menu_courses[1]
        triOcasciTemp["Menu 1"]["cena"] = menu_prices[1]

        if len(menu_courses) > 2:
            triOcasciTemp["Menu 2"] = dict()
            triOcasciTemp["Menu 2"]["menu"] = menu_courses[2]
            triOcasciTemp["Menu 2"]["cena"] = menu_prices[2]
        else:
            print("TriOcasci does not have second menu!")

        triOcasci = triOcasciTemp
    except:
        print("TriOcasci parser failed!")

    return triOcasci


def GetMenuPonava(day):
    """Get Ponava lunch menu."""
    ponava = {"url": "http://ponava.cafe/"}
    ponava["Name"] = "Ponava: Kavárna a restaurace"
    ponava["Info"] = "Polévka je v ceně menu."
    ponava["Icon"] = "http://ponava.cafe/wp-content/uploads/2017/06/logo.png"
    ponava["CardPay"] = "??"

    try:
        ponavaTemp = ponava
        r = get("http://ponava.cafe/")
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html5lib")  # Gets html code
        menu_extracted = sub(r'[\t\n\r]', '', str(soup)).replace('\xa0', '')

        if(day == 0):
            menu_extracted_day = findall("Pondělí(.*?)Úterý", menu_extracted, DOTALL)
        elif(day == 1):
            menu_extracted_day = findall("Úterý(.*?)Středa", menu_extracted, DOTALL)
        elif(day == 2):
            menu_extracted_day = findall("Středa(.*?)Čtvrtek", menu_extracted, DOTALL)
        elif(day == 3):
            menu_extracted_day = findall("Čtvrtek(.*?)Pátek", menu_extracted, DOTALL)
        elif(day == 4):
            menu_extracted_day = findall("Pátek(.*?)</p><span class", menu_extracted, DOTALL)

        menu_courses = findall(r"<p>M([A-Z,Č,Ď,Ř,Š,Ť,Ž,0-9,(,),-].*?)</p>", menu_extracted_day[0], DOTALL)
        menu_soup = findall(r"<p>([A-Z,Č,Ď,Ř,Š,Ť,Ž,0-9,(,),-].*?)</p>", menu_extracted_day[0], DOTALL)
        menu1_prices = findall(r"Menu 1: ([1-9].*?)<br", menu_extracted, DOTALL)
        menu2_prices = findall(r"Menu 2: ([1-9].*?)</h4>", menu_extracted, DOTALL)

        ponavaTemp["Polévka"] = menu_soup[0]

        ponavaTemp["Menu 1"] = dict()
        ponavaTemp["Menu 1"]["menu"] = menu_courses[0]
        ponavaTemp["Menu 1"]["cena"] = menu1_prices[0]

        ponavaTemp["Menu 2"] = dict()
        ponavaTemp["Menu 2"]["menu"] = menu_courses[1]
        ponavaTemp["Menu 2"]["cena"] = menu2_prices[0]

        ponava = ponavaTemp
    except:
        print("Ponava parser failed!")

    return ponava


def GetMenuDoubravnicka(day):
    """Get Doubravnicka lunch menu."""
    doubravnicka = {"url": "https://www.zomato.com/cs/brno/1-doubravnick%C3%A1-restaurace-%C4%8Dern%C3%A1-pole-brno-st%C5%99ed/denn%C3%AD-menu"}
    doubravnicka["Name"] = "Restaurace Doubravnická"
    doubravnicka["Info"] = "Polévka v ceně menu"
    doubravnicka["Icon"] = "https://scontent.fprg1-1.fna.fbcdn.net/v/t31.0-8/15972450_379599622398428_669626150077024214_o.jpg?oh=b3e0be7e028033a077bf49679323543d&oe=596C2776"
    doubravnicka["CardPay"] = "Ano"

    return doubravnicka

def GetMenuBishesGurkha(day):
    """Get Bishes Gurkha lunch menu."""
    bishesGurkha = {"url": "https://www.zomato.com/cs/brno/bishes-gurkha-1-brno-m%C4%9Bsto-brno-st%C5%99ed/menu"}
    bishesGurkha["Name"] = "Nepálská restaurace Bishes Gurkha"
    bishesGurkha["Info"] = "Polévka v ceně menu"
    bishesGurkha["Icon"] = "https://b.zmtcdn.com/data/pictures/8/18580968/c99dab2587bff230603ef94afdd7b48e.jpg?output-format=webp"
    bishesGurkha["CardPay"] = "Ano"

    return bishesGurkha
