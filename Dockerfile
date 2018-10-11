FROM python:3

COPY . .

RUN pip install requests
RUN pip install beautifulsoup4
RUN pip install czech-holidays
RUN pip install lxml

CMD [ "python", "lunch_menu_checker.py --type test_conv" ]
