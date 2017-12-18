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

        buddha["Polévka"] = findall("Polévka:(.*?)22,- Kč", menu_extracted_day[0], DOTALL)[0]
        buddha["Menu 1"] = dict()
        buddha["Menu 1"]["menu"] = findall("22,- Kč(.*?)95,- Kč", menu_extracted_day[0], DOTALL)[0]
        buddha["Menu 1"]["cena"] = 95

        buddha["Menu 2"] = dict()
        buddha["Menu 2"]["menu"] = findall("95,- Kč(.*?)95,- Kč", menu_extracted_day[0], DOTALL)[0]
        buddha["Menu 2"]["cena"] = 95

        buddha["Menu 3"] = dict()
        buddha["Menu 3"]["menu"] = findall("VEG(.*?)95,-.*?Kč", menu_extracted_day[0], DOTALL)[0]
        buddha["Menu 3"]["cena"] = 95

        buddha["Menu 4"] = dict()
        buddha["Menu 4"]["menu"] = findall("(150g Mix Thali.*?)130,- Kč", menu_extracted_day[0], DOTALL)[0]
        buddha["Menu 4"]["cena"] = 130
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

        osmicka["Polévka"] = findall("Polévka:(.*?)<", menu_extracted_day[0], DOTALL)[0]
        osmicka["Veg polévka"] = findall("Vegetariánské menu:(.*?)<", menu_extracted_day[0], DOTALL)[0]

        osmicka["Menu 1"] = dict()
        osmicka["Menu 2"] = dict()
        osmicka["Menu 3"] = dict()

        menu_types = findall(r"\"nabidka_1\">(.*?)<", menu_extracted_day[0], DOTALL)

        if len(menu_types) > 3:  # Bug at source web: long menu is shown as two menus
            # This can cause problems if the long menu is not the first one
            osmicka["Menu 1"]["menu"] = menu_types[0] + " " + menu_types[1]
            osmicka["Menu 2"]["menu"] = menu_types[2]
            osmicka["Menu 3"]["menu"] = menu_types[3]
        else:
            osmicka["Menu 1"]["menu"] = menu_types[0]
            osmicka["Menu 2"]["menu"] = menu_types[1]
            osmicka["Menu 3"]["menu"] = menu_types[2]

        osmicka["Menu 1"]["cena"] = findall(r"\"cena\">(.*?)<", menu_extracted_day[0], DOTALL)[0]
        osmicka["Menu 2"]["cena"] = findall(r"\"cena\">(.*?)<", menu_extracted_day[0], DOTALL)[1]
        osmicka["Menu 3"]["cena"] = findall(r"\"cena\">(.*?)<", menu_extracted_day[0], DOTALL)[2]
    except:
        print("Osmicka parser failed!")

    return osmicka


def GetMenuGoldenNepal(day):
    """Get Golden Nepal lunch menu."""
    GoldenNepal = {"url": "http://goldennepal.cz/"}
    GoldenNepal["Name"] = "Golden Nepal: Nepálská restaurace a bar"
    GoldenNepal["Info"] = "Ke každému jídlu ve všední den příloha rýže/placka/kombinace ZDARMA. Všechna jídla kromě Vindaloo, Jalfrezi, Madrasu a Falu obsahují smetanu. Všechny polévky obsahují mouku. Korma obsahuje ořechy. Chicken Tikka Masala, Butter Chicken a Vindaloo obsahují barvivo."
    GoldenNepal["Icon"] = "http://goldennepal.cz/wp-content/uploads/2016/06/logotext.png"
    GoldenNepal["CardPay"] = "Ano"

    try:
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

        GoldenNepal["Polévka"] = menu_courses[0] + " " + menu_prices[0]

        GoldenNepal["Menu 1"] = dict()
        GoldenNepal["Menu 1"]["menu"] = menu_courses[1]
        GoldenNepal["Menu 1"]["cena"] = menu_prices[1]

        GoldenNepal["Menu 2"] = dict()
        GoldenNepal["Menu 2"]["menu"] = menu_courses[2]
        GoldenNepal["Menu 2"]["cena"] = menu_prices[2]

        GoldenNepal["Menu 3"] = dict()
        GoldenNepal["Menu 3"]["menu"] = menu_courses[3]
        GoldenNepal["Menu 3"]["cena"] = menu_prices[3]

        GoldenNepal["Menu 4"] = dict()
        GoldenNepal["Menu 4"]["menu"] = menu_courses[4]
        GoldenNepal["Menu 4"]["cena"] = menu_prices[4]
    except:
        print("GoldenNepal parser failed!")

    return GoldenNepal


def GetMenuSabaidy(day):
    """Get Sabaidy lunch menu."""
    Sabaidy = {"url": "http://www.amphone.eu/restaurace"}
    Sabaidy["Name"] = "Sabaidy: Thajsko-laoská restaurace"
    Sabaidy["Info"] = "Polední menu podáváme každý všední den od 11 do 14 hodin. Polévka v ceně menu."
    Sabaidy["Icon"] = "http://goldennepal.cz/wp-content/uploads/2016/06/logotext.png"
    Sabaidy["CardPay"] = "Ano"

    try:
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

        Sabaidy["Polévka"] = findall(r"m>(.*?)</", menu_extracted_day[0], DOTALL)[0]

        Sabaidy["Menu 1"] = dict()
        Sabaidy["Menu 1"]["menu"] = menu_courses[0]
        Sabaidy["Menu 1"]["cena"] = menu_prices[0]

        Sabaidy["Menu 2"] = dict()
        Sabaidy["Menu 2"]["menu"] = menu_courses[1]
        Sabaidy["Menu 2"]["cena"] = menu_prices[1]

        Sabaidy["Menu 3"] = dict()
        Sabaidy["Menu 3"]["menu"] = menu_courses[2]
        Sabaidy["Menu 3"]["cena"] = menu_prices[2]

        Sabaidy["Menu 4"] = dict()
        Sabaidy["Menu 4"]["menu"] = menu_courses[3]
        Sabaidy["Menu 4"]["cena"] = menu_prices[3]
    except:
        print("Sabaidy parser failed!")

    return Sabaidy

def GetMenuTriOcasci(day):
    """Get TriOcasci lunch menu."""
    TriOcasci = {"url": "https://triocasci.cz/jidlo/"}
    TriOcasci["Name"] = "Tři ocásci: Veganská restaurace"
    TriOcasci["Info"] = "Polévka není v ceně menu. Je možné ji objednat samostatně."
    TriOcasci["Icon"] = "https://triocasci.cz/favicon.png"
    TriOcasci["CardPay"] = "??"

    try:
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

        TriOcasci["Polévka"] = menu_courses[0] + " " + menu_prices[0]

        TriOcasci["Menu 1"] = dict()
        TriOcasci["Menu 1"]["menu"] = menu_courses[1]
        TriOcasci["Menu 1"]["cena"] = menu_prices[1]

        if len(menu_courses) > 2:
            TriOcasci["Menu 2"] = dict()
            TriOcasci["Menu 2"]["menu"] = menu_courses[2]
            TriOcasci["Menu 2"]["cena"] = menu_prices[2]
        else:
            print("TriOcasci does not have second menu!")
    except:
        print("TriOcasci parser failed!")

    return TriOcasci


def GetMenuPonava(day):
    """Get Ponava lunch menu."""
    Ponava = {"url": "http://ponava.cafe/"}
    Ponava["Name"] = "Ponava: Kavárna a restaurace"
    Ponava["Info"] = "Polévka je v ceně menu."
    Ponava["Icon"] = "http://ponava.cafe/wp-content/uploads/2017/06/logo.png"
    Ponava["CardPay"] = "??"

    try:
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

        Ponava["Polévka"] = menu_soup[0]

        Ponava["Menu 1"] = dict()
        Ponava["Menu 1"]["menu"] = menu_courses[0]
        Ponava["Menu 1"]["cena"] = menu1_prices[0]

        Ponava["Menu 2"] = dict()
        Ponava["Menu 2"]["menu"] = menu_courses[1]
        Ponava["Menu 2"]["cena"] = menu2_prices[0]
    except:
        print("Ponava parser failed!")

    return Ponava


def GetMenuDoubravnicka(day):
    """Get Doubravnicka lunch menu."""
    Doubravnicka = {"url": "https://www.zomato.com/cs/brno/1-doubravnick%C3%A1-restaurace-%C4%8Dern%C3%A1-pole-brno-st%C5%99ed/denn%C3%AD-menu"}
    Doubravnicka["Name"] = "Restaurace Doubravnická"
    Doubravnicka["Info"] = "Polévka v ceně menu"
    Doubravnicka["Icon"] = "https://scontent.fprg1-1.fna.fbcdn.net/v/t31.0-8/15972450_379599622398428_669626150077024214_o.jpg?oh=b3e0be7e028033a077bf49679323543d&oe=596C2776"
    Doubravnicka["CardPay"] = "Ano"

    return Doubravnicka

def GetMenuBishesGurkha(day):
    """Get Bishes Gurkha lunch menu."""
    BishesGurkha = {"url": "https://www.zomato.com/cs/brno/bishes-gurkha-1-brno-m%C4%9Bsto-brno-st%C5%99ed/menu"}
    BishesGurkha["Name"] = "Nepálská restaurace Bishes Gurkha"
    BishesGurkha["Info"] = "Polévka v ceně menu"
    BishesGurkha["Icon"] = "https://b.zmtcdn.com/data/pictures/8/18580968/c99dab2587bff230603ef94afdd7b48e.jpg?output-format=webp"
    BishesGurkha["CardPay"] = "Ano"

    return BishesGurkha
