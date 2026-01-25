from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Iso formats date as YYYY-MM-DD
def format_date(date_to_format, iso):
    if iso:
        return date_to_format.isoformat()
    else:
        return date_to_format
    
def today(iso = True):
    return format_date(date.today(), iso)

def most_recent_sunday(iso = True):
    # Return the most recent Sunday
    today = date.today()
    most_recent_sunday = today - timedelta(days=(today.weekday() + 1) % 7) # sunday = 6
    return format_date(most_recent_sunday, iso)

def get_date_months_ago(delta_month = 3, iso = True):
    date_months_ago = most_recent_sunday(iso=False) - relativedelta(months=delta_month)
    return format_date(date_months_ago, iso)