FROM python:3

ADD LunchMenuChecker .

RUN pip install requests
RUN pip install beautifulsoup4
RUN pip install czech-holidays
RUN pip install lxml

CMD [ "python", "lunch_menu_checker.py --type test_conv" ]
