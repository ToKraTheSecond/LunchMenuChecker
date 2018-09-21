from czech_holidays import holidays
from datetime import datetime


def check_if_menu_can_be_posted():
    today_is_not_holiday = datetime.date(datetime.now()) not in holidays
    today_is_working_day = datetime.today().weekday() not in [5, 6]
    menu_can_be_posted = today_is_not_holiday and today_is_working_day
    
    return menu_can_be_posted
