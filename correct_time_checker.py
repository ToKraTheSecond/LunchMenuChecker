from czech_holidays import holidays


def check_if_menu_can_be_posted(day_index, date):
    today_is_not_holiday = date not in holidays
    today_is_working_day = day_index not in [5, 6]
    menu_can_be_posted = today_is_not_holiday and today_is_working_day
    
    return menu_can_be_posted
