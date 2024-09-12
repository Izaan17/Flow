import datetime


def days_between_dates(date1_str, date2_str, date_format='%m-%d-%Y'):
    # Convert date strings to datetime objects
    date1 = datetime.datetime.strptime(date1_str, '%m-%d-%Y-%H-%M')
    date2 = datetime.datetime.strptime(date2_str, '%m-%d-%Y-%H-%M')
    # Convert strings to not include hours
    date1 = date1.strftime('%m-%d-%Y')
    date2 = date2.strftime('%m-%d-%Y')
    # Convert them back into datetime objects
    date1 = datetime.datetime.strptime(date1, date_format)
    date2 = datetime.datetime.strptime(date2, date_format)

    # Calculate the difference in days
    delta = date2 - date1
    return delta.days


def parse_days_difference(days_difference):
    # Parse the days between
    if days_difference == 0:
        return "Today"
    elif days_difference == -1:
        return "Yesterday"
    elif days_difference == 1:
        return "Tomorrow"
    elif days_difference < 0:
        return f"Due {-days_difference} days ago"
    else:
        return f"Due in {days_difference} days"


def convert_str_to_datetime(date_str):
    return datetime.datetime.strptime(date_str, '%m-%d-%Y-%H-%M')


def get_abbreviated_day_of_week_string(date_str):
    return convert_str_to_datetime(date_str).strftime("%a")


def get_day_of_week_string(date_str):
    return convert_str_to_datetime(date_str).strftime("%A")


def get_day_string(date_str):
    return convert_str_to_datetime(date_str).day


def get_month_abbreviation_string(date_str):
    return convert_str_to_datetime(date_str).strftime("%b")


def get_month_string(date_str):
    return convert_str_to_datetime(date_str).strftime("%B")


def get_time_suffix_string(date_str):
    if isinstance(date_str, datetime.datetime):
        return date_str.strftime("%I:%M %p")

    return convert_str_to_datetime(date_str).strftime("%I:%M %p")
