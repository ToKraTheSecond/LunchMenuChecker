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
