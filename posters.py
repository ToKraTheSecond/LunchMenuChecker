def PostFortuneCookie(url):
    """Get and post fortune cookie."""
    if random.randint(1, 3) != 1:
        r = get("http://www.fortunecookiemessage.com")
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html5lib").text
        cookie = sub(r'[\t\n\r]', '', str(soup))
        cookie_extracted = findall(r"([A-Za-z][0-9a-zA-Z\b-';:,.()?]{15,100}[.!?\b])", cookie, DOTALL)[1]
    else:
        cookie_extracted = local_fortunecookie[random.randint(1, len(local_fortunecookie))][:-1]
        print(cookie_extracted)
    body = "\nFortune Cookie of the Day\n" \
        + "\n**" + cookie_extracted + "**\n\n"
    payload = {'body': body}
    headers = {'content-type': 'application/json'}
    response = post(url, data=dumps(payload), headers=headers)


def PostMenu(parsed_menu_dict, url):
    """Send given menu to given Glip URL."""
    body = ''
    icon = parsed_menu_dict["Icon"]
    name = parsed_menu_dict["Name"]
    del parsed_menu_dict["Icon"]
    del parsed_menu_dict["Name"]
    for key in parsed_menu_dict:
        body += parsed_menu_dict[key]

    payload = \
        {
         'activity': name,
    	 'icon': icon,
    	 'body': body
        }

    headers = {'content-type': 'application/json'}
    response = post(url, data=dumps(payload), headers=headers)
