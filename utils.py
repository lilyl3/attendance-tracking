from datetime import date, timedelta

# Iso formats date as YYYY-MM-DD
def format_date(date, iso):
    if iso:
        return date.today().isoformat()
    else:
        return date.today()
    
def today(iso = True):
    return format_date(date.today(), iso)

def most_recent_sunday(iso = True):
    # Return the most recent Sunday
    today = date.today()
    most_recent_sunday = today - timedelta(days=(today.weekday() + 1) % 7) # sunday = 6
    return format_date(most_recent_sunday, iso)

def get_date_months_ago(delta_month = 3, iso = True):
    today = date.today()
    date_months_ago = today - timedelta(months=delta_month)
    return format_date(date_months_ago, iso)