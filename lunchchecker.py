# -*- coding: utf-8 -*-
"""Post lunch menu from chosen restaurants to Glip chat."""

from re import search, findall, DOTALL, sub
from requests import get, post
from json import dumps
from datetime import datetime
from bs4 import BeautifulSoup
from sys import argv, exit
import sys

def GetMenuBuddha():
    """Get Buddha lunch menu."""
    buddha = {"url": "http://www.indian-restaurant-buddha.cz/index.html"}
    buddha["Name"] = "Buddha: Indická a Nepálská Restaurace"
    buddha["Info"] = "Příloha ke každému jídlu (v ceně): Tandoori Nan (indický chléb) / indická rýže Basmati / kombinace obou příloh. Polévka se podává zvlášť/soup is served separately from menu. (22 Kč)"
    buddha["Icon"] = "http://www.brnorozvoz.cz/restaurace-brno-v/indicka-a-nepalska-restaurace-buddha-brno.png"
    buddha["CardPay"] = "Ano"

    r = get(buddha["url"])
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html5lib")  # gets html code
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

    return buddha


def GetMenuOsmicka():
    """Get Osmicka lunch menu."""
    osmicka = {"url": "http://www.naosmicce.cz/Menu.pdf"}
    osmicka["Name"] = "Bistro na Osmičce: Burger and Pasta"
    osmicka["Info"] = "Polévka dle denní nabídky je během doby poledního menu zahrnuta v ceně!"
    osmicka["Icon"] = "http://www.naosmicce.cz/img/logo.png"
    osmicka["CardPay"] = "Ne"

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

    return osmicka


def GetMenuGoldenNepal():
    """Get Golden Nepal lunch menu."""
    GoldenNepal = {"url": "http://goldennepal.cz/"}
    GoldenNepal["Name"] = "Golden Nepal: Nepálská restaurace a bar"
    GoldenNepal["Info"] = "Ke každému jídlu ve všední den příloha rýže/placka/kombinace ZDARMA. Všechna jídla kromě Vindaloo, Jalfrezi, Madrasu a Falu obsahují smetanu. Všechny polévky obsahují mouku. Korma obsahuje ořechy. Chicken Tikka Masala, Butter Chicken a Vindaloo obsahují barvivo."
    GoldenNepal["Icon"] = "http://goldennepal.cz/wp-content/uploads/2016/06/logotext.png"
    GoldenNepal["CardPay"] = "Ano"

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

    return GoldenNepal


def GetMenuSabaidy():
    """Get Sabaidy lunch menu."""
    Sabaidy = {"url": "http://www.amphone.eu/restaurace"}
    Sabaidy["Name"] = "Sabaidy: Thajsko-laoská restaurace"
    Sabaidy["Info"] = "Polední menu podáváme každý všední den od 11 do 14 hodin. Polévka v ceně menu."
    Sabaidy["Icon"] = "http://goldennepal.cz/wp-content/uploads/2016/06/logotext.png"
    Sabaidy["CardPay"] = "Ano"

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

    return Sabaidy


def GetMenuBlackPoint():
    """Get BlackPoint lunch menu."""
    BlackPoint = {"url": "http://www.blackpointcafe.cz/denni-menu/"}
    BlackPoint["Name"] = "BlackPoint: Kavárno restaurace"
    BlackPoint["Info"] = "Polévka v ceně menu"
    BlackPoint["Icon"] = "http://files.blackpointcafe.cz/200000002-cb2aecc21b/200/black_cafe_1_black.png"
    BlackPoint["CardPay"] = "Ano"

    r = get("http://www.blackpointcafe.cz/denni-menu/")
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html5lib")  # Gets html code
    menu_extracted = sub(r'[\t\n\r]', '', str(soup)).replace('\xa0', '')

    if(day == 0):
        menu_extracted_day = findall("PONDĚLÍ(.*?)ÚTERÝ", menu_extracted, DOTALL)
    elif(day == 1):
        menu_extracted_day = findall("ÚTERÝ(.*?)STŘEDA", menu_extracted, DOTALL)
    elif(day == 2):
        menu_extracted_day = findall("STŘEDA(.*?)ČTVRTEK", menu_extracted, DOTALL)
    elif(day == 3):
        menu_extracted_day = findall("ČTVRTEK(.*?)PÁTEK", menu_extracted, DOTALL)
    elif(day == 4):
        menu_extracted_day = findall("PÁTEK(.*?)class", menu_extracted, DOTALL)

    menu_courses = findall(r"li>([A-Z,Č,Ď,Ř,Š,Ť,Ž].*?)</", menu_extracted_day[0], DOTALL)
    menu_prices = findall(r".{1}([0-9]{2,3}).{0,1}Kč", menu_extracted, DOTALL)

    BlackPoint["Polévka"] = findall(r"pol: (.*?) \(", menu_extracted_day[0], DOTALL)[0]

    BlackPoint["Menu 1"] = dict()
    BlackPoint["Menu 1"]["menu"] = menu_courses[0]
    BlackPoint["Menu 1"]["cena"] = menu_prices[0]

    BlackPoint["Menu 2"] = dict()
    BlackPoint["Menu 2"]["menu"] = menu_courses[1]
    BlackPoint["Menu 2"]["cena"] = menu_prices[1]

    BlackPoint["Menu 3"] = dict()
    BlackPoint["Menu 3"]["menu"] = menu_courses[2]
    BlackPoint["Menu 3"]["cena"] = menu_prices[2]

    BlackPoint["Menu 4"] = dict()
    BlackPoint["Menu 4"]["menu"] = menu_courses[3]
    BlackPoint["Menu 4"]["cena"] = menu_prices[3]

    return BlackPoint

def GetMenuTriOcasci():
    """Get TriOcasci lunch menu."""
    TriOcasci = {"url": "https://triocasci.cz/jidlo/"}
    TriOcasci["Name"] = "Tři ocásci: Veganská restaurace"
    TriOcasci["Info"] = "Polévka není v ceně menu. Je možné ji objednat samostatně."
    TriOcasci["Icon"] = "https://triocasci.cz/favicon.png"
    TriOcasci["CardPay"] = "??"

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

    return TriOcasci

def GetMenuPonava():
    """Get Ponava lunch menu."""
    Ponava = {"url": "http://ponava.cafe/"}
    Ponava["Name"] = "Kavárna a restaurace"
    Ponava["Info"] = "Polévka je v ceně menu."
    Ponava["Icon"] = "http://ponava.cafe/wp-content/uploads/2017/06/logo.png"
    Ponava["CardPay"] = "??"

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

    return Ponava

def GetMenuDoubravnicka():
    """Get Doubravnicka lunch menu."""
    Doubravnicka = {"url": "https://www.zomato.com/cs/brno/1-doubravnick%C3%A1-restaurace-%C4%8Dern%C3%A1-pole-brno-st%C5%99ed/denn%C3%AD-menu"}
    Doubravnicka["Name"] = "Restaurace Doubravnická"
    Doubravnicka["Info"] = "Polévka v ceně menu"
    Doubravnicka["Icon"] = "https://scontent.fprg1-1.fna.fbcdn.net/v/t31.0-8/15972450_379599622398428_669626150077024214_o.jpg?oh=b3e0be7e028033a077bf49679323543d&oe=596C2776"
    Doubravnicka["CardPay"] = "Ano"

    return Doubravnicka

def GetPostFortuneCookie(url):
    """Get and post fortune cookie."""
    r = get("http://www.fortunecookiemessage.com")
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html5lib").text
    cookie = sub(r'[\t\n\r]', '', str(soup))
    cookie_extracted = findall(r"([A-Za-z][0-9a-zA-Z\b-';:,.()?]{15,100}[.!?\b])", cookie, DOTALL)[1]

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


def PostRestaurantsLinks(url):
    """Send restaurants names and lunch menu links to given Glip URL."""
    links = {
        '**King´s Head (5 min pěšky)**': 'http://kingshead.cz/denni-menu/',
        '**Zelená Kočka - Solniční (10 min šalina+pěšky)**': 'http://www.zelenakocka.cz/index2.php',
        '**Tulip (5 min pěšky)**': 'http://tulip-restaurant.cz/cs/menu/',
        '**Annapurna (15 min šalina + pěšky)**': 'http://indicka-restaurace-annapurna.cz/index.php?option=com_content&view=article&id=2&Itemid=118',
        '**Everest (15 min šalina+pěšky)**': 'https://www.zomato.com/cs/brno/everest-veve%C5%99%C3%AD-brno-st%C5%99ed/denn%C3%AD-menu',
        '**Satyam (25 min šalina+pěšky)**': 'http://www.satyam.cz/cs/denni-menu.aspx',
        '**Stern (5 min pěšky)**': 'https://www.restu.cz/stern-1888-original-restaurant/denni-menu/',
        '**La Spernaza (10 min pěšky)**': 'http://lasperanza-bistro.cz/menu-complete/',
        '**Pivnice Pegas (10 min šalina+pěšky)**': 'http://brnorestauracepivnice.hotelpegas.cz/denni-menu/',
        '**Cattani (15 min šalina+pěšky)**': 'http://www.cattani.cz/',
        '**U Starýho Billa (5 min pěšky)**': 'https://www.zomato.com/cs/brno/u-star%C3%BDho-billa-%C4%8Dern%C3%A1-pole-brno-st%C5%99ed',
        '**Korejské bistro Doširak (25 min šalina)**': 'https://www.zomato.com/cs/brno/korejsk%C3%A9-bistro-do%C5%A1irak-kr%C3%A1lovo-pole-brno-sever',
        '**Vietnam (15 min šalina)**': 'http://vietnamskebagety.cz/',
        '**Polévkárna Schodová (15 min pěšky)**': 'https://www.polevkarnapodschody.cz/inpage/tydenni-nabidka/'
    }

    body = '**Ostatní restaurace:**\n'

    for key in links:
        body += key + ": \n"
        body += links.get(key) + "\n"

    payload = {'body': body}

    headers = {'content-type': 'application/json'}
    response = post(url, data=dumps(payload), headers=headers)

if __name__ == "__main__":
    # Import of Glip conversation links from external file
    with open('gliplinks.txt') as f:
        url_list = f.readlines()

    url_test = url_list[2][:-1]
    url_conv = url_list[4][:-1]
    url = argv[1]

    #Checks first argument
    if url == 't':
        url = url_test
    elif url == 'o':
        url = url_conv
    else:
        raise Exception('Wrong first argument!')
        exit()

    # Setting current datetime
    day = datetime.today().weekday()
    time = datetime.now().time()

    # We are looking for next day menu after 14:30.
    if time.hour > 15:
        day += 1
    # We will look for monday if it is saturday or sunday.
    if day == 5 or day == 6:
        day = 0

    #Checks second argument
    if argv[2] in {'GetMenuSabaidy', 'GetMenuOsmicka', 'GetMenuBlackPoint', 'GetMenuBuddha', 'GetMenuGoldenNepal', 'GetMenuDoubravnicka', 'GetMenuTriOcasci', 'GetMenuPonava'}:
        try:
            PostMenu(getattr(sys.modules[__name__], argv[2])(), url)
        except:
            print("{} failed!".format(argv[2]))
        exit()
    elif argv[2] == 'all':
        pass
    else:
        raise Exception('Wrong second argument!')
        exit()

    func_list = [
        GetMenuBlackPoint,
        GetMenuBuddha,
        GetMenuGoldenNepal,
        GetMenuSabaidy,
        GetMenuOsmicka,
        GetMenuDoubravnicka,
        GetMenuTriOcasci,
        GetMenuPonava
    ]

    for func in func_list:
        try:
            PostMenu(func(), url)
        except:
            print("{} failed.".format(func.__name__) )

    PostRestaurantsLinks(url)
    GetPostFortuneCookie(url)
