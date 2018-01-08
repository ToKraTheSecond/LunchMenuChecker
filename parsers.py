from re import findall, DOTALL, sub
from requests import get
from json import dumps
from bs4 import BeautifulSoup

def GetMenuKanas(day):
    kanas = {"url": "http://www.kanas.cz/stranka/jidelna" + '\n'}
    kanas["Name"] = "Jídelna/restaurace Kanas"
    kanas["Info"] = "Cesta: 5 minut" + '\n'
    kanas["Icon"] = "http://www.barber-schools.org/wp-content/uploads/2013/02/state-flag-kansas.jpg"
    kanas["CardPay"] = "Platba kartou: Ano" + '\n'

    try:
        kanasTemp = kanas

        r = get("http://www.kanas.cz/stranka/jidelna")
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html5lib")  # Gets html code
        menu = soup.findAll("div", {"class", "nabidka-in tab_container"})
        menu_extracted = sub(r'[\t\n\r]', '', str(menu))
        menu_extracted = findall(r"polozka(.*?)-</", menu_extracted, DOTALL)

        mealAmount = findall(r"stvi\">(.*?)<", ' '.join(menu_extracted), DOTALL)
        mealName = findall(r"idlo\">(.*?)<", ' '.join(menu_extracted), DOTALL)
        mealPrice = findall(r"cena\">(.*?),", ' '.join(menu_extracted), DOTALL)

        kanasTemp["Restaurace"] = '\n' + "**Restaurace**" + '\n'

        for x in range(0,17):
            kanasTemp[x] = mealAmount[x] + ' ' + mealName[x] + ' ' + mealPrice[x] + ',-' + '\n'
            if(x == 4):
                kanasTemp["Jidelna"] = '\n' + "**Jidelna**" + '\n'

        kanas = kanasTemp
    except:
        print("Kanas parser failed!")

    return kanas

def GetMenuPurkynka(day):
    purkynka = {"url": "http://www.napurkynce.cz/purkynka/denni-menu/" + '\n'}
    purkynka["Name"] = "Restaurace Na Purkyňce"
    purkynka["Info"] = "Cesta: 10 minut" + '\n'
    purkynka["Icon"] = "http://www.napurkynce.cz/ariadne/file_generators/dbfile.php?_fileId=564&_fileName=logo.png&_site=drevenaruze_purkynka"
    purkynka["CardPay"] = "Platba kartou: Ano"

    try:
        purkynkaTemp = purkynka

        r = get("http://www.napurkynce.cz/purkynka/denni-menu/")
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, "html5lib")  # Gets html code
        menu = str(soup)
        menu_extracted = sub(r'[\t\n\r]', '', str(menu))
        menu_extracted = findall(r"e>Menu(.*?),-</pre", menu_extracted, DOTALL)

        soups = findall(r": (.*?)<br", ' '.join(menu_extracted), DOTALL)
        meals = findall(r"\)(.*?),-", ' '.join(menu_extracted), DOTALL)

        purkynkaTemp["Polévka"] = '\n\n' + soups[day] + '\n'

        if day == 0:
            for x in range(0,4):
                purkynkaTemp[x] = meals[x] + ',-' + '\n'
        if day == 1:
            for x in range(4,8):
                purkynkaTemp[x] = meals[x] + ',-' + '\n'
        if day == 2:
            for x in range(8,12):
                purkynkaTemp[x] = meals[x] + ',-' + '\n'
        if day == 3:
            for x in range(12,16):
                purkynkaTemp[x] = meals[x] + ',-' + '\n'
        if day == 4:
            for x in range(16,20):
                purkynkaTemp[x] = meals[x] + ',-' + '\n'

        purkynka = purkynkaTemp
    except:
        print("Purkynka parser failed!")

    return purkynka
