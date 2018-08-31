from czech_holidays import holidays
from datetime import datetime


def check_if_menu_can_be_posted():
    today_is_holiday = datetime.date(datetime.now()) in holidays
    today_is_working_day = datetime.today().weekday() == 5 or datetime.today().weekday() == 6
    menu_can_be_posted = today_is_holiday and today_is_working_day
    
    return menu_can_be_posted
