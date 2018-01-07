from re import findall, DOTALL, sub
from requests import get
from json import dumps
from bs4 import BeautifulSoup

def GetMenuKanas(day):
    kanas = {"url": "http://www.kanas.cz/stranka/jidelna"}
    kanas["Name"] = "Kanas" + '\n'
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

        kanasTemp["Restaurace"] = '\n' +"**Restaurace**" + '\n'

        for x in range(0,17):
            kanasTemp[x] = mealAmount[x] + ' ' + mealName[x] + ' ' + mealPrice[x] + ',-' + '\n'
            if(x == 4):
                kanasTemp["Jidelna"] = '\n' + "**Jidelna**" + '\n'

        kanas = kanasTemp
    except:
        print("Kanas parser failed!")

    return kanas
