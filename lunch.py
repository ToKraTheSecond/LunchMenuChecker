# -*- coding: utf-8 -*-


''''import requests


url = 'https://hooks.glip.com/webhook/e9065968-a3b2-463e-9065-c5fc20508597'
payload = {
	'icon':'http://icons.iconarchive.com/icons/sensibleworld/starwars/512/Darth-Vader-icon.png',
	'body':'Come To The Dark Side'
}
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)
'''

import json
import re
import requests
import datetime
import PyPDF2
import pdfminer

from bs4 import BeautifulSoup




day = datetime.datetime.today().weekday()

time = datetime.datetime.now().time()

#we are looking for next day menu after 14:30
if time.hour > 15:
    day += 1

#we will look for monday if it is saturday or sunday
if day == 5 or day == 6:
    day = 0

days_of_week = ['pondělí','úterý','středa','čtvrtek','pátek']


def GetMenuVarna():
    '''Returns dictionary with menu from Varna'''

    varna = dict()
    varna["Menu 1"] = dict()
    varna["Menu 2"] = dict()
    varna["Menu 3"] = dict()
    varna["Menu 4"] = dict()

    varna["url"] = "http://www.restauracevarna.cz/denni-menu/"
    varna["Name"] = "Varna Pivní Restaurace"
    varna["Info"] = "Polévka a bonaqua 0,25l v ceně, Menu 4 je bonusové menu"
    varna["Icon"] = "http://www.restauracevarna.cz/images/layout/logo.png"

    r = requests.get(varna["url"])
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text) #gets html code

    for date in soup.findAll('h2'):
        if days_of_week[day] in date.get_text():
            varna["Polévka"] = date.findNext("td").get_text().strip()

            varna["Menu 1"]["menu"] = date.findAllNext("td", {'class':'nazev'})[0].get_text().strip()
            varna["Menu 1"]["cena"] = date.findAllNext("td", {'class':'cena'})[0].get_text().strip()
            varna["Menu 2"]["menu"] = date.findAllNext("td", {'class':'nazev'})[1].get_text().strip()
            varna["Menu 2"]["cena"] = date.findAllNext("td", {'class':'cena'})[1].get_text().strip()
            varna["Menu 3"]["menu"] = date.findAllNext("td", {'class':'nazev'})[2].get_text().strip()
            varna["Menu 3"]["cena"] = date.findAllNext("td", {'class':'cena'})[2].get_text().strip()
            varna["Menu 4"]["menu"] = date.findAllNext("td", {'class':'nazev'})[3].get_text().strip()
            varna["Menu 4"]["cena"] = date.findAllNext("td", {'class':'cena'})[3].get_text().strip()

            #get numbers from Kč string
            varna["Menu 1"]["cena"] = int(re.search(r'\d+', varna["Menu 1"]["cena"]).group())
            varna["Menu 2"]["cena"] = int(re.search(r'\d+', varna["Menu 2"]["cena"]).group())
            varna["Menu 3"]["cena"] = int(re.search(r'\d+', varna["Menu 3"]["cena"]).group())
            varna["Menu 4"]["cena"] = int(re.search(r'\d+', varna["Menu 4"]["cena"]).group())
            break; #so we cant find more days

    return varna
def GetMenuBuddha():
    buddha = {"url":"http://buddhabrno.cz/index.html"}
    buddha["Name"] = "Buddha Indická a Nepálská Restaurace"
    buddha["Info"] = "Příloha ke každému jídlu (v ceně): Tandoori Nan (indický chléb) / indická rýže Basmati / kombinace obou příloh. Polévka se podává zvlášť/soup is served separately from menu. (17 Kč)"
    buddha["Icon"] = "https://www.jidloted.cz/images/logos/11721.png"

    r = requests.get(buddha["url"])
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text) #gets html code
    menu = soup.findAll("p",{"class","textmenu"})



    soups = re.findall("</span>(.*)17,",str(menu[:2])) #looks for soups for all week
    first_meals = re.findall("17,- Kč(.*?)84",str(menu[:2]),re.DOTALL) #looks for all meals
    menu_extracted = re.sub(r'[\t\n\r]','',str(menu[:2]))

    if(day == 0):
        menu_extracted_day =  re.findall("PONDĚLÍ(.*?)ÚTERÝ",menu_extracted,re.DOTALL) #onlz monday text
    elif(day == 1):
        menu_extracted_day =  re.findall("ÚTERÝ(.*?)STŘEDA",menu_extracted,re.DOTALL) #onlz monday text
    elif(day == 2):
         menu_extracted_day =  re.findall("STŘEDA(.*?)ČTVRTEK",menu_extracted,re.DOTALL) #onlz monday text
    elif(day == 3):
        menu_extracted_day = re.findall("ČTVRTEK(.*?)PÁTEK",menu_extracted,re.DOTALL) #onlz monday text

    buddha["Polévka"] = soups[day].strip() #picks soup by day
    buddha["Menu 1"] = dict()
    buddha["Menu 1"]["menu"] = re.sub(r'[\t\n\r]', '',first_meals[day].strip())
    buddha["Menu 1"]["cena"] = 84

    buddha["Menu 2"] = dict()
    buddha["Menu 2"]["menu"] = re.findall("84,-.*?Kč (.*?)84,-.*?Kč",menu_extracted_day[0],re.DOTALL)[0]
    buddha["Menu 2"]["cena"] = 84

    buddha["Menu 3"] = dict()
    buddha["Menu 3"]["menu"] = re.findall("VEG(.*?)84,-.*?Kč", menu_extracted_day[0], re.DOTALL)[0]
    buddha["Menu 3"]["cena"] = 84

    buddha["Menu 4"] = dict()
    buddha["Menu 4"]["menu"] = re.findall("(Mix Thali.*?)120,-.*?Kč", menu_extracted_day[0], re.DOTALL)[0]
    buddha["Menu 4"]["cena"] = 120

    return buddha


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

def GetOsmicka():
    osmicka = {"url":"http://www.naosmicce.cz/Menu.pdf"}
    osmicka["Name"] = "Bistro na Osmičce - Burger and Pasta"
    osmicka["Info"] = "Polévka dle denní nabídky je během doby poledního menu zahrnuta v ceně!"
    osmicka["Icon"] = "http://www.naosmicce.cz/img/logo.png"
    whole_text = convert_pdf_to_txt("Menu.pdf")
    #print(whole_text)
    soups = re.findall("Polévka:(.*?).1",whole_text,re.DOTALL)
    first_meals = re.findall(r"\s1.(.*?)Vegetariánské",whole_text,re.DOTALL)


    osmicka["Polévka"] = soups[day]
    osmicka["Menu 1"] = dict()
    osmicka["Menu 1"]["menu"] = first_meals[day].rstrip()
    osmicka["Menu 1"]["cena"] = 99

    print(osmicka["Polévka"])
    return osmicka



def PostMenu(menu_dict):


    body = menu_dict["url"] + "\n"
    body += menu_dict["Info"] + "\n"

    if "Polévka" in menu_dict.keys():
        body += "**Polévka:** " + menu_dict["Polévka"] + "\n"
    if "Menu 1" in menu_dict.keys():
        body += "**Menu 1:** " + menu_dict["Menu 1"]["menu"] + " - " + str(menu_dict["Menu 1"]["cena"]) + " Kč" + "\n"
    if "Menu 2" in menu_dict.keys():
        body += "**Menu 2:** " + menu_dict["Menu 2"]["menu"] + " - " + str(menu_dict["Menu 2"]["cena"]) + " Kč" + "\n"
    if "Menu 3" in menu_dict.keys():
        body += "**Menu 3:** " + menu_dict["Menu 3"]["menu"] + " - " + str(menu_dict["Menu 3"]["cena"]) + " Kč" + "\n"
    if "Menu 4" in menu_dict.keys():
        body += "**Menu 4:** " + menu_dict["Menu 4"]["menu"] + " - " + str(menu_dict["Menu 4"]["cena"]) + " Kč" + "\n"
    if "Menu 5" in menu_dict.keys():
        body += "**Menu 5:** " + menu_dict["Menu 5"]["menu"] + " - " + str(menu_dict["Menu 5"]["cena"]) + " Kč" + "\n"

    url = 'https://hooks.glip.com/webhook/e9065968-a3b2-463e-9065-c5fc20508597' #test
    payload = \
    {
    'activity':menu_dict["Name"],
	'icon':menu_dict["Icon"],
	'body':body
    }

    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

#GetMenuBuddha()
#PostMenu(GetOsmicka())
PostMenu(GetMenuVarna())
#PostMenu(GetMenuBuddha())
