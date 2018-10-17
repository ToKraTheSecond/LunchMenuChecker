FROM python:3

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "lunch_menu_checker.py", "--type", "test_conv"]
